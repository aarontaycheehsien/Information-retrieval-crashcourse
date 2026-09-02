import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import vm from "node:vm";

const editorPath = resolve("lightweight-wysiwyg-html-editor-v4-footnotes.html");
const source = await readFile(editorPath, "utf8");

test("the standalone editor script parses", () => {
  const scripts = [...source.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)];
  assert.equal(scripts.length, 1);
  assert.doesNotThrow(() => new vm.Script(scripts[0][1], { filename: "editor-inline.js" }));
});

test("annotation controls and cleanup paths remain wired", () => {
  for (const id of ["commentBtn", "annotationPanel", "annotationList", "annotationDialog",
    "runAllClaudeBtn", "copyAllCodexBtn", "importProposalBtn"]) {
    assert.match(source, new RegExp(`id=["']${id}["']`));
  }
  assert.match(source, /cleanAnnotationArtifacts\(clone\)/);
  assert.match(source, /\.annotations\.json/);
  assert.match(source, /event\.altKey && event\.key\.toLowerCase\(\) === "m"/);
});

test("all three WebMCP tools register in the top-level page with execute handlers", () => {
  for (const name of ["list_editor_annotations", "get_editor_annotation_context", "propose_editor_revision"]) {
    assert.match(source, new RegExp(`name: ["']${name}["']`));
  }
  assert.match(source, /modelContext\.registerTool\(\{ \.\.\.definition, execute: handler \}\)/);
  assert.match(source, /document\.modelContext/);
});

test("proposal acceptance is explicit and stale proposals are guarded", () => {
  assert.match(source, /function acceptAnnotationProposal/);
  assert.match(source, /anchor\.textContent !== proposal\.baseText/);
  assert.match(source, /proposal\.outcome = "accepted"/);
  assert.match(source, /documentChanged: false/);
});
