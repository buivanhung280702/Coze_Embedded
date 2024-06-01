const WebSocket = require('ws');

// Tạo một server WebSocket
const server = new WebSocket.Server({ port: 3000, host: '0.0.0.0' });

// Danh sách các kết nối client
const clients = new Set();

// Gửi tin nhắn đến tất cả các client
function sendToAllClients(message) {
    for (const client of clients) {
        client.send(message);
    }
}

// Sự kiện xử lý khi có một kết nối WebSocket mới
server.on('connection', (socket) => {
    console.log('Client connected');

    // Thêm kết nối client vào danh sách
    clients.add(socket);

    // Gửi tin nhắn đến client khi có kết nối thành công
    socket.send('Welcome to the WebSocket server!');

    // Sự kiện xử lý khi nhận được tin nhắn từ client
    socket.on('message', (message) => {
        const mes = message.toString('utf8');
        console.log('Received message:', mes);

        // Gửi tin nhắn trả lời cho client
        socket.send(`Server received: ${message}`);

        // Gửi tin nhắn nhận được đến tất cả các client
        sendToAllClients(`${message}`);
    });

    // Sự kiện xử lý khi client đóng kết nối
    socket.on('close', () => {
        console.log('Client disconnected');

        // Xóa kết nối client khỏi danh sách
        clients.delete(socket);
    });
});

console.log('WebSocket server is running on port 3000');