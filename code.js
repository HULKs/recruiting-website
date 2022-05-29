let editor = null;

window.addEventListener("load", function () {
  require.config({ paths: { vs: "monaco-editor/min/vs" } });
  require(["vs/editor/editor.main"], function () {
    editor = monaco.editor.create(document.querySelector(".code"), {
      language: "python",
      minimap: {
        enabled: false,
      },
      value: codeValue,
    });
    editor.onDidChangeModelContent(() => {
      storeCodeValue(editor.getValue());
    });
  });
});
