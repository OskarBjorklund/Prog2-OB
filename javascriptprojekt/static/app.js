import { v4 as uuidv4 } from 'https://jspm.dev/uuid';

/**
 * Saves uuid in cookie if not present
 * @returns universal unique id
 */
function getUuid() {
  if (!document.cookie) {
      document.cookie = uuidv4()
  }
  return document.cookie;
}

// Client sends an uuid to the server upon connection
const socket = io({
  query: {
    uuid: getUuid()
  }
});

const whiteboard = document.getElementById("whiteboard"); // Canvas element
const context = whiteboard.getContext("2d"); // Canvas context
const thicknessSlider = document.getElementById("thickness-slider") // Get info from slider

let isDrawing = false;
let lastX = 0;
let lastY = 0;

context.lineCap = "round"; // Round pencil draws

/**
 * Draws a line fromX, fromY to toX, toY with designated color and thickness
 * @param {Number} fromX 
 * @param {Number} fromY 
 * @param {Number} toX 
 * @param {Number} toY 
 * @param {String (HEX)} color 
 * @param {Number} thickness 
 */
function drawLine(fromX, fromY, toX, toY, color, thickness) {
  context.strokeStyle = color;
  context.lineWidth = thickness;
  context.beginPath();
  context.moveTo(fromX, fromY);
  context.lineTo(toX, toY);
  context.stroke();
}

// 
whiteboard.addEventListener("mousedown", (event) => {
  isDrawing = true;
  lastX = event.offsetX;
  lastY = event.offsetY;
});

whiteboard.addEventListener("mouseup", () => {
  isDrawing = false;
});

whiteboard.addEventListener("mousemove", (event) => {
  if (!isDrawing) return;

  const { offsetX, offsetY } = event;
  const data = {
    fromX: lastX,
    fromY: lastY,
    toX: offsetX,
    toY: offsetY,
    lineWidth: thicknessSlider.value,
    socketId: socket.id
  };

  socket.emit("drawing", data);

  lastX = offsetX;
  lastY = offsetY;
});

socket.on("clientDrawEvent", (data) => {
  drawLine(data.fromX, data.fromY, data.toX, data.toY, data.color, data.lineWidth);
});

socket.on("initialState", (drawingActions) => {
  drawingActions.forEach((data) => {
    drawLine(data.fromX, data.fromY, data.toX, data.toY, data.color, data.lineWidth);
  });
});

const clearButton = document.getElementById("clear-button");
clearButton.addEventListener("click", () => {
  socket.emit("clear");
});

socket.on("clientClearedBoard", () => {
  clearWhiteboard()
})

function clearWhiteboard() {
  context.clearRect(0, 0, whiteboard.width, whiteboard.height);
}