#!/usr/bin/env node
import { createServer as createHttpServer } from "node:http";
import { randomBytes, randomUUID } from "node:crypto";
import { spawn, spawnSync } from "node:child_process";
import { extname, isAbsolute, relative, resolve, sep } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { readFile, stat } from "node:fs/promises";

export const EDITOR_FILE = "lightweight-wysiwyg-html-editor-v4-footnotes.html";
const MAX_BODY_BYTES = 256 * 1024;
const MAX_OUTPUT_BYTES = 2 * 1024 * 1024;
const DEFAULT_TIMEOUT_MS = 5 * 60 * 1000;

const proposalSchema = {
  type: "object",
  additionalProperties: false,
  properties: {
    annotationId: { type: "string" },
    baseText: { type: "string" },
    replacementHtml: { type: "string" },
    rationale: { type: "string" }
  },
  required: ["annotationId", "baseText", "replacementHtml", "rationale"]
};

const mimeTypes = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8", ".svg": "image/svg+xml",
  ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
  ".gif": "image/gif", ".webp": "image/webp", ".pdf": "application/pdf"
};

export function safeRepositoryPath(root, pathname) {
  let decoded;
  try { decoded = decodeURIComponent(pathname); } catch { return null; }
  if (decoded.includes("\0")) return null;
  const requested = decoded === "/" ? "/" + EDITOR_FILE : decoded;
  const target = resolve(root, "." + requested.replaceAll("/", sep));
  const rel = relative(resolve(root), target);
  if (rel === "" || rel === ".." || rel.startsWith(".." + sep) || isAbsolute(rel)) return null;
  return target;
}

export function parseClaudeResult(stdout) {
  let outer;
  try { outer = JSON.parse(String(stdout || "").trim()); }
  catch { throw new Error("Claude returned malformed JSON."); }
  const candidates = [outer.structured_output, outer.structuredOutput, outer.result, outer];
  for (let candidate of candidates) {
    if (typeof candidate === "string") {
      try { candidate = JSON.parse(candidate); } catch { continue; }
    }
    if (candidate && typeof candidate === "object" &&
        proposalSchema.required.every(key => typeof candidate[key] === "string")) {
      return candidate;
    }
  }
  throw new Error("Claude did not return the required proposal fields.");
}

function json(response, status, body) {
  const data = Buffer.from(JSON.stringify(body));
  response.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": data.length,
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff"
  });
  response.end(data);
}

async function requestBody(request) {
  const chunks = [];
  let size = 0;
  for await (const chunk of request) {
    size += chunk.length;
    if (size > MAX_BODY_BYTES) {
      const error = new Error("Request body is too large.");
      error.statusCode = 413;
      throw error;
    }
    chunks.push(chunk);
  }
  try { return JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}"); }
  catch {
    const error = new Error("Request body must be valid JSON.");
    error.statusCode = 400;
    throw error;
  }
}

function proposalPrompt(context) {
  return `You are proposing a revision for one annotated range in an HTML editor.
Follow the instruction, replace only selectedText, and do not rewrite the containing block.
Return only the JSON object required by the supplied schema. baseText must exactly equal selectedText.
replacementHtml may use semantic inline HTML only. Do not use scripts, styles, event handlers, IDs,
editor metadata, block wrappers, markdown fences, or commentary outside the JSON.

ANNOTATION CONTEXT
${JSON.stringify(context, null, 2)}`;
}

function publicJob(job) {
  return {
    id: job.id, status: job.status, annotationId: job.annotationId,
    createdAt: job.createdAt, updatedAt: job.updatedAt,
    result: job.result || null, error: job.error || ""
  };
}

export function createAnnotationServer(options = {}) {
  const root = resolve(options.root || process.cwd());
  const host = "127.0.0.1";
  const token = options.token || randomBytes(32).toString("base64url");
  const jobs = new Map();
  const claudeCommand = options.claudeCommand || "claude";
  const claudeBaseArgs = options.claudeBaseArgs || [
    "--print", "--no-session-persistence", "--permission-mode", "plan",
    "--tools", "", "--output-format", "json", "--json-schema", JSON.stringify(proposalSchema)
  ];
  const timeoutMs = options.timeoutMs || DEFAULT_TIMEOUT_MS;
  const version = options.claudeReady === undefined
    ? spawnSync(claudeCommand, ["--version"], { encoding: "utf8", windowsHide: true, timeout: 5000 })
    : null;
  const claudeReady = options.claudeReady ?? (version?.status === 0);
  const claudeVersion = options.claudeVersion || version?.stdout?.trim() || "";
  let origin = "";

  function authorized(request) {
    const bearer = request.headers.authorization === "Bearer " + token;
    const requestOrigin = request.headers.origin;
    return bearer && (!requestOrigin || requestOrigin === origin);
  }

  function runJob(job, context) {
    job.status = "running";
    job.updatedAt = new Date().toISOString();
    const child = spawn(claudeCommand, claudeBaseArgs, {
      shell: false, windowsHide: true, stdio: ["pipe", "pipe", "pipe"]
    });
    job.child = child;
    let stdout = Buffer.alloc(0);
    let stderr = Buffer.alloc(0);
    let killedForOutput = false;
    const timer = setTimeout(() => {
      job.status = "timed_out";
      job.error = "Claude exceeded the five-minute proposal timeout.";
      job.updatedAt = new Date().toISOString();
      child.kill();
    }, timeoutMs);

    const collect = (existing, chunk) => {
      const combined = Buffer.concat([existing, chunk]);
      if (combined.length > MAX_OUTPUT_BYTES) {
        killedForOutput = true;
        child.kill();
        return combined.subarray(0, MAX_OUTPUT_BYTES);
      }
      return combined;
    };
    child.stdout.on("data", chunk => { stdout = collect(stdout, chunk); });
    child.stderr.on("data", chunk => { stderr = collect(stderr, chunk); });
    child.on("error", error => {
      clearTimeout(timer);
      if (["cancelled", "timed_out"].includes(job.status)) return;
      job.status = "failed";
      job.error = error.code === "ENOENT"
        ? "Claude CLI was not found. Install it or add claude to PATH."
        : error.message;
      job.updatedAt = new Date().toISOString();
    });
    child.on("close", code => {
      clearTimeout(timer);
      delete job.child;
      if (["cancelled", "timed_out"].includes(job.status)) return;
      if (killedForOutput) {
        job.status = "failed";
        job.error = "Claude output exceeded the safety limit.";
      } else if (code !== 0) {
        job.status = "failed";
        job.error = stderr.toString("utf8").trim() || `Claude exited with code ${code}.`;
      } else {
        try {
          const result = parseClaudeResult(stdout);
          if (result.annotationId !== job.annotationId || result.baseText !== context.selectedText) {
            throw new Error("Claude returned a mismatched annotation ID or base text.");
          }
          job.result = result;
          job.status = "completed";
        } catch (error) {
          job.status = "failed";
          job.error = error.message;
        }
      }
      job.updatedAt = new Date().toISOString();
    });
    child.stdin.end(proposalPrompt(context));
  }

  const server = createHttpServer(async (request, response) => {
    try {
      const url = new URL(request.url, origin || "http://127.0.0.1");
      if (url.pathname.startsWith("/api/")) {
        if (!authorized(request)) return json(response, 401, { error: "Invalid helper token or origin." });
        if (request.method === "GET" && url.pathname === "/api/health") {
          return json(response, 200, { ok: true, claudeReady, claudeVersion });
        }
        if (request.method === "POST" && url.pathname === "/api/claude/jobs") {
          if (!claudeReady) return json(response, 503, { error: "Claude CLI is not available on this machine." });
          const body = await requestBody(request);
          const context = body.context;
          if (!context || typeof context.annotationId !== "string" ||
              typeof context.instruction !== "string" || typeof context.selectedText !== "string" ||
              !context.selectedText.trim()) {
            return json(response, 400, { error: "A valid annotation context is required." });
          }
          const now = new Date().toISOString();
          const job = { id: randomUUID(), annotationId: context.annotationId, status: "queued",
            createdAt: now, updatedAt: now, result: null, error: "" };
          jobs.set(job.id, job);
          runJob(job, context);
          return json(response, 202, publicJob(job));
        }
        const match = url.pathname.match(/^\/api\/jobs\/([0-9a-f-]+)$/i);
        if (match) {
          const job = jobs.get(match[1]);
          if (!job) return json(response, 404, { error: "Unknown job." });
          if (request.method === "GET") return json(response, 200, publicJob(job));
          if (request.method === "DELETE") {
            if (["queued", "running"].includes(job.status)) {
              job.status = "cancelled";
              job.error = "Cancelled by the user.";
              job.updatedAt = new Date().toISOString();
              job.child?.kill();
            }
            return json(response, 200, publicJob(job));
          }
        }
        return json(response, 404, { error: "Unknown API endpoint." });
      }

      if (request.method !== "GET" && request.method !== "HEAD") {
        response.writeHead(405, { Allow: "GET, HEAD" });
        return response.end();
      }
      const target = safeRepositoryPath(root, url.pathname);
      if (!target) return json(response, 403, { error: "Path is outside the repository." });
      const info = await stat(target);
      if (!info.isFile()) return json(response, 404, { error: "File not found." });
      const data = await readFile(target);
      response.writeHead(200, {
        "Content-Type": mimeTypes[extname(target).toLowerCase()] || "application/octet-stream",
        "Content-Length": data.length, "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"
      });
      response.end(request.method === "HEAD" ? undefined : data);
    } catch (error) {
      const statusCode = error.code === "ENOENT" ? 404 : error.statusCode || 500;
      json(response, statusCode, { error: statusCode === 500 ? "Local helper error: " + error.message : error.message });
    }
  });

  return {
    server, root, host, token, jobs,
    async listen(port = 4317) {
      await new Promise((resolveListen, reject) => {
        server.once("error", reject);
        server.listen(port, host, resolveListen);
      });
      const address = server.address();
      origin = `http://${host}:${address.port}`;
      return { origin, url: `${origin}/${EDITOR_FILE}?bridgeToken=${encodeURIComponent(token)}` };
    },
    async close() {
      for (const job of jobs.values()) job.child?.kill();
      if (server.listening) await new Promise(resolveClose => server.close(resolveClose));
    }
  };
}

function cliOptions(argv) {
  const options = { root: process.cwd(), port: 4317 };
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === "--root") options.root = argv[++index];
    else if (argv[index] === "--port") options.port = Number(argv[++index]);
  }
  return options;
}

async function main() {
  const options = cliOptions(process.argv.slice(2));
  const helper = createAnnotationServer({ root: options.root });
  const address = await helper.listen(options.port);
  console.log("Annotation editor helper is running locally.");
  console.log(address.url);
  console.log("Press Ctrl+C to stop it.");
  const stop = async () => { await helper.close(); process.exit(0); };
  process.on("SIGINT", stop);
  process.on("SIGTERM", stop);
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main().catch(error => { console.error(error.message); process.exitCode = 1; });
}
