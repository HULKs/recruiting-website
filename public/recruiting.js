var resultsLoad = (evt) => {
    var status = evt.target.status;

    if (status == 200) {
        data = JSON.parse(evt.target.responseText);
        clearBalls();

        document.querySelector(".code-output").innerText = data.stdout
        for (ball of data.balls) {
            plotBall(ball);
        }
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

var clearBalls = () => {
    var cursors = document.getElementsByClassName("cursor");
    while(cursors[0]) {
        cursors[0].parentNode.removeChild(cursors[0]);
    }
};

var plotBall = (ball) => {
    var graphic = document.querySelector(".graphic");
    var plot = document.querySelector(".plot");
    var cursor = document.createElement("img");
    cursor.setAttribute("class", "cursor");
    cursor.src = "cursor.png"
    plot.insertBefore(cursor, graphic);

    if (ball.y < 0) {
        alert('Y-Koordinate darf nicht kleiner als 0 sein >:/');
        return;
    }

    if (ball.x < 0) {
        alert('X-Koordinate darf nicht kleiner als 0 sein >:/');
        return;
    }

    if (ball.y > graphic.naturalHeight) {
        alert(`Y-Koordinate darf nicht größer als ${graphic.naturalHeight} sein >:/`);
        return;
    }

    if (ball.x > graphic.naturalWidth) {
        alert(`X-Koordinate darf nicht größer als ${graphic.naturalWidth} sein >:/`);
        return;
    }

    var x = (ball.x / graphic.naturalWidth) * graphic.width;
    var y = (ball.y / graphic.naturalHeight) * graphic.height;

    console.log(`Scaled cursor offset: y=${y}, x=${x}`);

    cursor.style.top = `${y}px`;
    cursor.style.left = `${x}px`;
};

window.addEventListener("load", () => {
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/github");
    editor.session.setMode("ace/mode/python");
    editor.session.setOptions({
        tabSize: 4,
        useSoftTabs: true
    });

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
