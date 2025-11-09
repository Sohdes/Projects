import socket
import threading
import sys
from pathlib import Path


SERVER_IP = "127.0.0.1"
SERVER_PORT = 9090


def receive_messages(sock):
    while True:
        try:
            command = sock.recv(1024).decode("utf-8")
            if command == "FILE":
                filename = sock.recv(1024).decode("utf-8")
                sys.stdout.write(f"\rReceiving file: {filename}\n")
                sys.stdout.flush()

                with open(f"received_{filename}", "wb") as file:
                    while True:
                        data = sock.recv(1024)
                        if data == b"DONE":
                            break
                        file.write(data)

                sys.stdout.write(f"\rFile {filename} received successfully.\n")
                sys.stdout.flush()
            else:
                sys.stdout.write(f"\r{command}\n")
                sys.stdout.flush()
        except:
            sys.stdout.write("\rDisconnected from server.\n")
            sys.stdout.flush()
            break


def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        sys.stdout.write(f"Connected to the server at {SERVER_IP}:{SERVER_PORT}\n")
        sys.stdout.flush()

        username = input("Enter your username: ").strip()
        client_socket.sendall(username.encode("utf-8"))
        print('Write a message, "@username + message" for private, or "2" for send a file)\n')
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

        while True:
            sys.stdout.write("Write a message: ")
            sys.stdout.flush()
            message = input().strip()

            if message == "2":
                filepath = input("Enter the file path: ").strip()
                try:
                    with open(filepath, "rb") as f:
                        data = f.read()
                    client_socket.sendall("FILE".encode("utf-8"))
                    filename = Path(filepath).name.encode("utf-8")
                    client_socket.sendall(filename)
                    client_socket.sendall(len(data).to_bytes(8, 'big'))  # send file length
                    client_socket.sendall(data)
                    print("File sent successfully.")
                except Exception as e:
                    print(f"Error sending file: {e}")

            else:
                client_socket.sendall("TEXT".encode("utf-8"))
                client_socket.sendall(message.encode("utf-8"))




    except ConnectionRefusedError:
        sys.stdout.write("\nCould not connect to the server. Is it running?\n")
        sys.stdout.flush()
    except Exception as e:
        sys.stdout.write(f"\nUnexpected error: {e}\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
