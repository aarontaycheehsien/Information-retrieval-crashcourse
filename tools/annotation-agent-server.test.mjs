import test from "node:test";
import assert from "node:assert/strict";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createAnnotationServer, parseClaudeResult, safeRepositoryPath } from "./annotation-agent-server.mjs";

const toolsDirectory = dirname(fileURLToPath(import.meta.url));
const repositoryRoot = resolve(toolsDirectory, "..");
const fixture = resolve(toolsDirectory, "fixtures", "mock-claude.mjs");

function context() {
  return {
    annotationId: "ann-test", instruction: "Make this clearer.", selectedText: "Original words",
    selectedHtml: "Original words", containingBlock: { tag: "p", text: "Original words in context." },
    headingBreadcrumb: ["Test"], previousBlock: "Before", nextBlock: "After"
  };
}

async function start(mode = "success", timeoutMs = 3000) {
  const helper = createAnnotationServer({
    root: repositoryRoot, token: "test-token", claudeReady: true,
    claudeCommand: process.execPath, claudeBaseArgs: [fixture, mode], timeoutMs
  });
  const address = await helper.listen(0);
  return { helper, ...address, headers: { Authorization: "Bearer test-token", Origin: address.origin } };
}

async function waitForJob(origin, id, headers) {
  for (let attempt = 0; attempt < 80; attempt += 1) {
    const response = await fetch(`${origin}/api/jobs/${id}`, { headers });
    const job = await response.json();
    if (!["queued", "running"].includes(job.status)) return job;
    await new Promise(resolveWait => setTimeout(resolveWait, 25));
  }
  throw new Error("Mock job did not finish");
}

test("repository paths cannot escape the root", () => {
  assert.equal(safeRepositoryPath(repositoryRoot, "/../outside.txt"), null);
  assert.equal(safeRepositoryPath(repositoryRoot, "/%2e%2e/outside.txt"), null);
  assert.ok(safeRepositoryPath(repositoryRoot, "/lightweight-wysiwyg-html-editor-v4-footnotes.html"));
});

test("Claude parser accepts structured output and rejects malformed output", () => {
  const result = parseClaudeResult(JSON.stringify({ structured_output: {
    annotationId: "a", baseText: "b", replacementHtml: "c", rationale: "d"
  } }));
  assert.equal(result.annotationId, "a");
  assert.throws(() => parseClaudeResult("not json"), /malformed JSON/);
});

test("helper enforces bearer token and same origin", async t => {
  const { helper, origin, headers } = await start();
  t.after(() => helper.close());
  assert.equal((await fetch(origin + "/api/health")).status, 401);
  assert.equal((await fetch(origin + "/api/health", {
    headers: { Authorization: headers.Authorization, Origin: "http://evil.invalid" }
  })).status, 401);
  const response = await fetch(origin + "/api/health", { headers });
  assert.equal(response.status, 200);
  assert.equal((await response.json()).claudeReady, true);
});

test("mocked Claude output becomes a reviewable job result", async t => {
  const { helper, origin, headers } = await start();
  t.after(() => helper.close());
  const response = await fetch(origin + "/api/claude/jobs", {
    method: "POST", headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({ context: context() })
  });
  assert.equal(response.status, 202);
  const created = await response.json();
  const job = await waitForJob(origin, created.id, headers);
  assert.equal(job.status, "completed");
  assert.equal(job.result.annotationId, "ann-test");
  assert.equal(job.result.baseText, "Original words");
});

test("malformed agent output is reported without changing files", async t => {
  const { helper, origin, headers } = await start("malformed");
  t.after(() => helper.close());
  const response = await fetch(origin + "/api/claude/jobs", {
    method: "POST", headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({ context: context() })
  });
  const created = await response.json();
  const job = await waitForJob(origin, created.id, headers);
  assert.equal(job.status, "failed");
  assert.match(job.error, /malformed JSON/);
});

test("running jobs can be cancelled", async t => {
  const { helper, origin, headers } = await start("delay");
  t.after(() => helper.close());
  const response = await fetch(origin + "/api/claude/jobs", {
    method: "POST", headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({ context: context() })
  });
  const created = await response.json();
  const cancelledResponse = await fetch(`${origin}/api/jobs/${created.id}`, { method: "DELETE", headers });
  assert.equal(cancelledResponse.status, 200);
  assert.equal((await cancelledResponse.json()).status, "cancelled");
});

test("jobs time out and oversized payloads are rejected", async t => {
  const { helper, origin, headers } = await start("delay", 50);
  t.after(() => helper.close());
  const response = await fetch(origin + "/api/claude/jobs", {
    method: "POST", headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({ context: context() })
  });
  const created = await response.json();
  const job = await waitForJob(origin, created.id, headers);
  assert.equal(job.status, "timed_out");

  const oversized = await fetch(origin + "/api/claude/jobs", {
    method: "POST", headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({ padding: "x".repeat(300 * 1024) })
  });
  assert.equal(oversized.status, 413);
});
