import socket
import threading
import json
import random
import string
import time

class NetworkManager:
    def __init__(self):
        self.is_server = False
        self.socket = None
        self.clients = []  # Server only: list of connected client sockets
        self.host = '0.0.0.0'  # Bind to all local network interfaces
        self.port = 5050
        self.meeting_code = None
        
        # Callback function to send incoming network data to the active Flet screen
        self.on_message_received = None 

    def generate_meeting_code(self):
        """Generates a random 6-character alphanumeric meeting code."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # ==========================================
    # SERVER (TEACHER ROLE)
    # ==========================================
    def start_server(self):
        """Starts the local TCP server for the classroom."""
        self.is_server = True
        self.meeting_code = self.generate_meeting_code()
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        
        # Start accepting connections in a background thread so the UI doesn't freeze
        threading.Thread(target=self._accept_connections, daemon=True).start()
        
        # Determine local IP to show to students
        local_ip = socket.gethostbyname(socket.gethostname())
        return self.meeting_code, local_ip

    def _accept_connections(self):
        """Background loop to accept incoming student connections."""
        while self.is_server:
            try:
                client_socket, address = self.socket.accept()
                self.clients.append(client_socket)
                threading.Thread(target=self._handle_client, args=(client_socket,), daemon=True).start()
            except Exception:
                break

    def _handle_client(self, client_socket):
        """Listens for data from a specific student and broadcasts it."""
        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                message = json.loads(data.decode('utf-8'))
                
                # Pass data to the Teacher's UI
                if self.on_message_received:
                    self.on_message_received(message)
                    
                # Broadcast the message to all OTHER students
                self.broadcast(message, exclude=client_socket)
            except Exception:
                break
                
        # Cleanup when student disconnects
        if client_socket in self.clients:
            self.clients.remove(client_socket)
        client_socket.close()

    def broadcast(self, message, exclude=None):
        """Sends a JSON message to all connected students."""
        try:
            data = json.dumps(message).encode('utf-8')
            for client in self.clients:
                if client != exclude:
                    try:
                        client.sendall(data)
                    except:
                        pass
        except Exception as e:
            print(f"Broadcast error: {e}")

    # ==========================================
    # CLIENT (STUDENT ROLE)
    # ==========================================
    def connect_to_meeting(self, host_ip, code, user_name, role):
        """Connects a student to the Teacher's local server."""
        self.is_server = False
        self.meeting_code = code
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.socket.connect((host_ip, self.port))
            # Start listening for server broadcasts in the background
            threading.Thread(target=self._listen_for_messages, daemon=True).start()
            
            # Send initial join packet
            join_msg = {
                "type": "system", 
                "action": "join",
                "sender": user_name, 
                "role": role, 
                "code": code,
                "timestamp": time.time()
            }
            self.send_message(join_msg)
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def _listen_for_messages(self):
        """Background loop to receive broadcasts from the Teacher's server."""
        while not self.is_server:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                message = json.loads(data.decode('utf-8'))
                
                # Pass data to the Student's UI
                if self.on_message_received:
                    self.on_message_received(message)
            except Exception:
                break

    # ==========================================
    # SHARED NETWORK FUNCTIONS
    # ==========================================
    def send_message(self, message):
        """Sends a packet over the network based on role."""
        if self.is_server:
            # Teacher sends to everyone, and updates their own UI
            self.broadcast(message)
            if self.on_message_received:
                self.on_message_received(message)
        else:
            # Student sends to Teacher (who then broadcasts it)
            try:
                data = json.dumps(message).encode('utf-8')
                self.socket.sendall(data)
            except Exception as e:
                print(f"Failed to send message: {e}")

    def disconnect(self):
        """Safely shuts down the network connection."""
        if self.is_server:
            self.is_server = False
            for client in self.clients:
                client.close()
            self.clients.clear()
        if self.socket:
            self.socket.close()