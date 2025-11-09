import socket
import threading

SERVER_IP = "0.0.0.0"
SERVER_PORT = 9090

clients = {}
usernames = {}


def broadcast(message, sender_socket=None, recipient_username=None):
    sender_username = "Server" if sender_socket is None else clients.get(sender_socket, "Unknown")

    if recipient_username:
        # Private message
        recipient_socket = usernames.get(recipient_username)
        if recipient_socket:
            try:
                formatted_message = f"(Private from {sender_username}) {sender_username}: {message}"
                recipient_socket.sendall(formatted_message.encode("utf-8"))
            except:
                recipient_socket.close()
                del clients[recipient_socket]
                del usernames[recipient_username]
    else:
        # Broadcast to everyone except sender
        for client in list(clients.keys()):
            if client != sender_socket:
                try:
                    client.sendall(f"{sender_username}: {message}".encode("utf-8"))
                except:
                    client.close()
                    del clients[client]


def broadcast_file(filename, file_data, sender_socket):
    sender_username = clients.get(sender_socket, "Unknown")

    for client in list(clients.keys()):
        if client != sender_socket:
            try:
                client.sendall("FILE".encode("utf-8"))
                client.sendall(f"{sender_username}_{filename}".encode("utf-8"))

                for chunk in file_data:
                    client.sendall(chunk)

                client.sendall(b"DONE")
            except:
                client.close()
                del clients[client]


def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")

    try:
        # Request and store the username
        username = client_socket.recv(1024).decode("utf-8").strip()
        if not username:
            username = f"User_{client_address[1]}"  # Assign default username if empty
        clients[client_socket] = username
        usernames[username] = client_socket
        print(f"Username '{username}' registered from {client_address}")

        while True:
            command = client_socket.recv(1024).decode("utf-8")

            if command == "FILE":
                # filename (short text)
                filename = client_socket.recv(1024).decode("utf-8", errors="ignore").strip()
                # 8-byte length header
                size_bytes = client_socket.recv(8)
                file_size = int.from_bytes(size_bytes, "big")

                received = 0
                file_data = b""
                while received < file_size:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    file_data += chunk
                    received += len(chunk)

                print(f"Got file {filename} ({received} bytes) from {username}")


            elif command == "TEXT":
                message = client_socket.recv(1024).decode("utf-8")
                print(f"{username}: {message}")  # Print message in server log

                # Check for private message
                if message.startswith("@"):
                    split_msg = message.split(" ", 1)
                    if len(split_msg) > 1:
                        recipient = split_msg[0][1:]  # Remove '@' and get username
                        private_msg = split_msg[1]
                        broadcast(private_msg, sender_socket=client_socket, recipient_username=recipient)
                else:
                    broadcast(message, sender_socket=client_socket)
    except ConnectionResetError:
        print(f"Client {username} ({client_address}) disconnected.")
    except Exception as e:
        print(f"Error handling {username} ({client_address}): {e}")
    finally:
        client_socket.close()
        del clients[client_socket]
        del usernames[username]
        print(f"{username} ({client_address}) removed from active clients.")


def server_send_message():
    while True:
        message = input("\n(Server) Enter message to broadcast (or type 'exit' to stop server): ").strip()
        if message.lower() == "exit":
            print("\nShutting down the server.")
            for client in list(clients.keys()):
                client.close()
            break
        broadcast(message)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #Fastening the socket to IP
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(6)
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")

    threading.Thread(target=server_send_message, daemon=True).start()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()
    except KeyboardInterrupt:
        print("\nShutting down the server.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
