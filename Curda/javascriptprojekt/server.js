const express = require("express");
const http = require("http");
const socketIO = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

app.use(express.static(__dirname + "/static"));

let drawingActions = [];
let clients = {};

io.on("connection", (socket) => {
  console.log("A new client connected.");
  let uuid = socket.handshake.query.uuid

  if (!clients[uuid]) {
    clients[uuid] = {
      color: getRandomColor()
    }
  }
  
  // Canvas state (load existing drawing)
  socket.emit("initialState", drawingActions);
  
  socket.on("drawing", (data) => {
    let drawData = {
      ...data, // Unpack
      color: clients[uuid].color
    }
    drawingActions.push(drawData);
    io.emit("clientDrawEvent", drawData)
  });

  socket.on("clear", () => {
    drawingActions.splice(0, drawingActions.length)
    io.emit("clientClearedBoard")
  })

  socket.on("disconnect", () => {
    console.log("A client disconnected.");
  });
});

function getRandomColor() {
  const letters = "0123456789ABCDEF";
  let color = "#";
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

const port = 3000;
server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});