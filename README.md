Secure Chat Application (WebSocket Based) with End-to-End Encryption
Overview

This project is a Secure Real-Time Chat Application built using Python, WebSockets, and Cryptographic techniques to ensure end-to-end encrypted communication between users. The system enables clients to exchange messages in real time while protecting confidentiality, integrity, and authenticity.

Unlike traditional messaging systems where messages may be decrypted on the server, this application ensures that only the communicating users can read the messages, making it resistant to server-side data exposure and interception.

The project demonstrates practical implementation of secure communication protocols, public key cryptography, and real-time networking, making it a useful cybersecurity learning project.

Key Features
1. Real-Time Messaging

Uses WebSocket protocol for full-duplex communication.

Enables instant message delivery between connected clients.

2. End-to-End Encryption (E2EE)

Messages are encrypted on the sender's device.

Only the intended recipient can decrypt the message.

The server never sees plaintext messages.

3. Public Key Exchange

Each user generates a public/private key pair.

Public keys are exchanged securely when users connect.

4. Message Integrity

Cryptographic hashing ensures that messages cannot be altered during transmission.

5. Replay Protection

Message timestamps and IDs help detect duplicate or replayed messages.

6. Multi-Client Support

Multiple users can connect simultaneously.

Server manages active connections using a connection manager.

Project Structure
secure-chat/
│
├── app.py
├── connection_manager.py
├── crypto_utils.py
├── client.py
├── requirements.txt
└── README.md
File Description

app.py

Main WebSocket server

Handles incoming client connections

Routes encrypted messages between users

connection_manager.py

Maintains list of connected clients

Handles connect, disconnect, and message broadcasting

crypto_utils.py

Implements cryptographic functions

Key generation

Encryption and decryption

client.py

Chat client application

Connects to WebSocket server

Encrypts outgoing messages

Decrypts received messages

requirements.txt

Contains required Python libraries.

Technologies Used
Technology	Purpose
Python	Core programming language
WebSockets	Real-time communication
FastAPI / Asyncio	Async server handling
Cryptography Library	Encryption and key management
JSON	Message format
Installation
1. Clone the Repository
git clone https://github.com/yourusername/secure-chat-e2ee.git
cd secure-chat-e2ee
2. Create Virtual Environment (Recommended)
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
Running the Project (Linux Terminal)
Start the WebSocket Server
python3 app.py

or if using FastAPI with Uvicorn:

uvicorn app:app --host 0.0.0.0 --port 8000

Server will start at:

ws://localhost:8000
Run the Chat Client

Open a new terminal window:

python3 client.py

Run the client in multiple terminals to simulate multiple users.

Example Workflow

Start the WebSocket server.

Run multiple client instances.

Clients generate encryption keys.

Public keys are exchanged.

Messages are encrypted before sending.

Recipient decrypts the message locally.

Security Architecture
Sender
   |
   | Encrypt Message (Recipient Public Key)
   v
WebSocket Server
   |
   | Forward Encrypted Message
   v
Recipient
   |
   | Decrypt Message (Private Key)
   v
Plaintext Message

The server acts only as a relay and cannot decrypt messages.

Future Improvements

User authentication system

Secure key exchange using Diffie-Hellman

Message persistence with encrypted database

Web-based chat interface

File transfer with encryption

Group chat support

Secure session management

Educational Value

This project demonstrates concepts in:

Secure communication protocols

Cryptographic systems

Network programming

WebSocket real-time applications

Cybersecurity engineering

It is a suitable academic or portfolio project for cybersecurity and software engineering students.

License

This project is open-source and available under the MIT License.

Author

Soumyajit Dutta

Cybersecurity and Computer Science Enthusiast.
