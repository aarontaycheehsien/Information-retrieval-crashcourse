const mode = process.argv[2] || "success";
let prompt = "";
for await (const chunk of process.stdin) prompt += chunk;
const contextMarker = "ANNOTATION CONTEXT\n";
let context = {};
try { context = JSON.parse(prompt.slice(prompt.indexOf(contextMarker) + contextMarker.length)); } catch { /* test path */ }

if (mode === "delay") {
  setTimeout(() => process.stdout.write(JSON.stringify({
    annotationId: context.annotationId, baseText: context.selectedText,
    replacementHtml: "Delayed replacement", rationale: "Mock delay"
  })), 5000);
} else if (mode === "malformed") {
  process.stdout.write("not json");
} else {
  process.stdout.write(JSON.stringify({ structured_output: {
    annotationId: context.annotationId, baseText: context.selectedText,
    replacementHtml: "<strong>Mock replacement</strong>",
    rationale: "Mocked proposal for automated verification."
  } }));
}
