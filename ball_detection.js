const images = [
  ["red_ball", "Red ball"],
  ["red_ball_x2", "Two red balls"],
  ["red_ball_obscured", "Partially obscured red ball"],
  ["new_ball", "Real ball"],
  ["new_ball_obscured", "Partially obscured real ball"],
  ["nao_bottom_field", "Camera bottom field"],
  ["nao_bottom_line", "Camera bottom line"],
  ["nao_top_near", "Camera top near"],
  ["nao_top_far", "Camera top far"],
];

const svgNamespace = "http://www.w3.org/2000/svg";
let pyodide = null;
let pyodideNamespace = null;
let imageSelector = null;
let imageSvg = null;
let imageCanvasWidth = null;
let imageCanvasHeight = null;
let imageCanvasContext = null;
let output = null;

if (codeValue === null) {
  codeValue = `# Get a reference to the image
image = get_ball_image()

# Some test code ... you can replace/remove these lines
print("Hello, world!")
print("Image with", image.width, "x", image.height, "pixels")
print(f"Red value of pixel in the top left corner: {image.at(x=0, y=0).r}")

# Draw a circle onto the image at position [25, 35] with a radius of 20 in red 
plot_detected_ball(x=25, y=35, radius=20)
`;
  storeCodeValue(codeValue);
}

window.addEventListener("load", async function () {
  pyodide = await loadPyodide({
    stdout: (line) => { addOutput(line, false); },
    stderr: (line) => { addOutput(line, true); },
  });
  pyodideNamespace = pyodide.globals.get("dict")();
  pyodideNamespace.set("get_ball_image", getBallImage);
  pyodideNamespace.set("plot_detected_ball", plotDetectedBall);
  const ballDetectionElement = document.getElementById("ball_detection");
  while (ballDetectionElement.firstChild) {
    ballDetectionElement.removeChild(ballDetectionElement.firstChild);
  }
  ballDetectionElement.classList.add("loaded");
  const runProgram = document.createElement("button");
  runProgram.innerText = "Run program";
  runProgram.id = "run_program";
  runProgram.addEventListener("click", () => {
    updateBallDetection();
  });
  ballDetectionElement.appendChild(runProgram);
  imageSelector = document.createElement("select");
  imageSelector.id = "image_selector";
  for (const [image, imageDescription] of images) {
    const imageOption = document.createElement("option");
    imageOption.value = image;
    imageOption.innerText = imageDescription;
    imageSelector.appendChild(imageOption);
  }
  imageSelector.addEventListener("change", () => {
    updateCanvas();
  });
  ballDetectionElement.appendChild(imageSelector);
  output = document.createElement("div");
  output.id = "output";
  ballDetectionElement.appendChild(output);
  imageSvg = document.createElementNS(svgNamespace, "svg");
  imageSvg.id = "image";
  ballDetectionElement.appendChild(imageSvg);
  updateCanvas();
});

function getCurrentImagePath() {
  return `ball_detection_images/${imageSelector.value}.png`;
}

function updateCanvas() {
  const image = new Image();
  image.crossOrigin = "anonymous";
  image.src = getCurrentImagePath();
  image.onload = () => {
    const canvas = document.createElement("canvas");
    canvas.width = image.width;
    canvas.height = image.height;
    imageCanvasWidth = image.width;
    imageCanvasHeight = image.height;
    imageCanvasContext = canvas.getContext("2d");
    imageCanvasContext.drawImage(image, 0, 0);

    updateSvg();
    clearOutput();
  };
}

function updateSvg() {
  while (imageSvg.firstChild) {
    imageSvg.removeChild(imageSvg.firstChild);
  }
  imageSvg.setAttribute(
    "viewBox",
    `0 0 ${imageCanvasWidth} ${imageCanvasHeight}`
  );
  const imageElement = document.createElementNS(svgNamespace, "image");
  imageElement.setAttribute("href", getCurrentImagePath());
  imageElement.setAttribute("x", "0");
  imageElement.setAttribute("y", "0");
  imageSvg.appendChild(imageElement);
}

function clearOutput() {
  while (output.firstChild) {
    output.removeChild(output.firstChild);
  }
}

function addOutput(line, isError) {
  if (output === null) {
    return;
  }
  console.log(line, isError);
  const lineElement = document.createElement("pre");
  lineElement.classList.add("line");
  lineElement.classList.add(isError ? "stderr" : "stdout");
  lineElement.innerText = line;
  output.appendChild(lineElement);
}

function updateBallDetection() {
  updateSvg();
  clearOutput();
  try {
    pyodide.runPython(editor.getValue(), { globals: pyodideNamespace });
  } catch (error) {
    error.message.split("\n").forEach((line) => addOutput(line, true));
    console.error(error.message);
  }
}

function getBallImage() {
  return {
    width: imageCanvasWidth,
    height: imageCanvasHeight,
    at: (keywordArguments) => {
      if (typeof keywordArguments.x !== "number") {
        throw "Missing keyword parameter x for Image.at(x, y)";
      }
      if (typeof keywordArguments.y !== "number") {
        throw "Missing keyword parameter y for Image.at(x, y)";
      }
      const imageData = imageCanvasContext.getImageData(keywordArguments.x, keywordArguments.y, 1, 1);
      return {
        r: imageData.data[0],
        g: imageData.data[1],
        b: imageData.data[2],
      };
    },
  };
}

function plotDetectedBall(keywordArguments) {
  console.log(keywordArguments);
  if (typeof keywordArguments.x !== "number") {
    throw "Missing keyword parameter x for plot_detected_ball(x, y, radius)";
  }
  if (typeof keywordArguments.y !== "number") {
    throw "Missing keyword parameter y for plot_detected_ball(x, y, radius)";
  }
  if (typeof keywordArguments.radius !== "number") {
    throw "Missing keyword parameter radius for plot_detected_ball(x, y, radius)";
  }
  const circle = document.createElementNS(svgNamespace, "circle");
  circle.setAttribute("cx", keywordArguments.x);
  circle.setAttribute("cy", keywordArguments.y);
  circle.setAttribute("r", keywordArguments.radius);
  circle.setAttribute("stroke", "yellow");
  circle.setAttribute("stroke-width", "2");
  circle.setAttribute("fill", "none");
  imageSvg.appendChild(circle);
}
