var resultsLoad = (evt) => {
    var status = evt.target.status;

    if (status == 200) {
        data = JSON.parse(evt.target.responseText);

        document.querySelector(".code-output").innerText = data.stdout
        plotBall(data.ball);
    } else {
        alert(`Server returned status ${status}! See console for details.`);
        console.log(evt.target);
    }
};

var requestError = (evt) => {
    alert('Request resulted in an error. See console for details.');
    console.log(evt.target);
};

var requestTimeout = (evt) => {
    alert('Request resulted in a timeout. See console for details.');
    console.log(evt.target);
};

var plotBall = (ball) => {
    var cursor = document.querySelector(".cursor");
    cursor.style.opacity = "1";

    cursor.style.top = `${ball.y}px`;
    cursor.style.left = `${ball.x}px`;
};

window.addEventListener("load", () => {
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/github");
    editor.session.setMode("ace/mode/python");

    var runForm = document.querySelector("form");
    var runButton = document.querySelector("button");

    runButton.addEventListener("click", (evt) => {
        evt.preventDefault();

        var fd = new FormData(runForm);
        fd.append("code-input", editor.getValue());

        var req = new XMLHttpRequest();
        req.addEventListener("load", resultsLoad);
        req.addEventListener("error", requestError);
        req.addEventListener("timeout", requestTimeout);
        req.open("POST", "/run");
        req.send(fd);
    });
});
