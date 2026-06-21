const PYODIDE_VERSION = "v0.26.4";

export async function getPyodide(statusEl) {
  if (!window.__miscDivesPyodidePromise) {
    setStatus(statusEl, "Loading Pyodide...", "loading");
    window.__miscDivesPyodidePromise = loadPyodide({
      indexURL: `https://cdn.jsdelivr.net/pyodide/${PYODIDE_VERSION}/full/`,
    });
  }
  const pyodide = await window.__miscDivesPyodidePromise;
  setStatus(statusEl, "Pyodide ready", "ready");
  return pyodide;
}

export async function loadPythonFile(pyodide, path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`Could not load ${path}: ${response.status}`);
  }
  const source = await response.text();
  await pyodide.runPythonAsync(source);
}

export function setStatus(el, message, kind = "ready") {
  el.textContent = message;
  el.dataset.kind = kind;
}

export function setText(el, value) {
  el.textContent = value == null ? "" : String(value);
}

export function pretty(value) {
  return JSON.stringify(value, null, 2);
}

export async function callPythonJson(pyodide, functionName, payload) {
  pyodide.globals.set("tool_payload_json", JSON.stringify(payload));
  const result = await pyodide.runPythonAsync(`
import json
tool_payload = json.loads(tool_payload_json)
json.dumps(${functionName}(**tool_payload))
`);
  return JSON.parse(result);
}

export async function copyText(text, statusEl) {
  await navigator.clipboard.writeText(text);
  setStatus(statusEl, "Copied", "ready");
}
