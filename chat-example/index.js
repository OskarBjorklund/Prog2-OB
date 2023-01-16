const express = require("express");
const app = express();
const http = require("http");
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

app.get("/", (req, res) => {
    //res.send("<h1>Skraggan största löken!</h1>");
    res.sendFile(__dirname + "/index.html");
});

io.on("connection", (socket) => {
    let username = "User";

    socket.on("chat message", (msg) => {
        console.log("message: " + msg)
    }),
    socket.on("chat message", (msg) => {
        if (msg[0] == "/"){
            msg = msg.slice(1)
            
            io.emit("chat message", username + ": " + msg);
        } else {
            io.emit("chat message", username + ": " + msg);
        }
        
    });
    console.log("a lök connected");
    socket.on("disconnect", (socket) => {
        console.log("a lök disconnected");
    });
});


server.listen(3000, () => {
    console.log("Lisening on *:3000");
});