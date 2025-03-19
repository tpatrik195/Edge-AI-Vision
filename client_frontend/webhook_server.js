const express = require("express");
const bodyParser = require("body-parser");
const http = require("http");
const cors = require("cors");
const { Server } = require("socket.io");

const app = express();
const PORT = 9000;

app.use(cors());
app.use(bodyParser.json());

const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "http://localhost:3000",   // react client address
    methods: ["GET", "POST"]
  }
});

io.on("connection", (socket) => {
  console.log("Client connected");
});

app.post("/webhook", (req, res) => {
  console.log("Received Webhook:", req.body);
  io.emit("gesture_event", req.body);
  res.json({ status: "received" });
});

server.listen(PORT, () => {
  console.log(`Webhook server running on http://127.0.0.1:${PORT}`);
});
