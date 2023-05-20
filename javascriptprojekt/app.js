const canvas = document.getElementById('board');
const context = canvas.getContext('2d');

// Set up WebSocket connection
const socket = new WebSocket('ws://localhost:3000');

// Handle WebSocket connection established
socket.onopen = () => {
  console.log('Connected to WebSocket');
};

// Handle received data from WebSocket
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  // Draw on canvas based on received data
  if (data.type === 'draw') {
    draw(data.x, data.y, data.color);
  }
};

// Handle mouse events
let isDrawing = false;
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', drawLine);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

function startDrawing(event) {
  isDrawing = true;
  const x = event.clientX - canvas.offsetLeft;
  const y = event.clientY - canvas.offsetTop;
  
  draw(x, y);
  
  // Send draw event to WebSocket server
  socket.send(JSON.stringify({ type: 'draw', x, y, color: '#000' }));
}

function drawLine(event) {
  if (!isDrawing) return;
  
  const x = event.clientX - canvas.offsetLeft;
  const y = event.clientY - canvas.offsetTop;
  
  draw(x, y);
  
  // Send draw event to WebSocket server
  socket.send(JSON.stringify({ type: 'draw', x, y, color: '#000' }));
}

function stopDrawing() {
  isDrawing = false;
}

function draw(x, y, color = '#000') {
  context.beginPath();
  context.fillStyle = color;
  context.arc(x, y, 5, 0, 2 * Math.PI);
  context.fill();
}
