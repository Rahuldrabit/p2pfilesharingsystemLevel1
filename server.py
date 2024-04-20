import socket
import threading
import os

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"[+] Accepted connection from {client_address}")
    
    # Receive and handle client requests
    while True:
        request = client_socket.recv(1024).decode()
        if not request:
            break
        elif request == "list":
            files = os.listdir("server_files")
            file_list = "\n".join(files)
            client_socket.send(file_list.encode())
        elif request.startswith("download"):
            file_name = request.split()[1]
            try:
                with open(f"server_files/{file_name}", "rb") as file:
                    data = file.read()
                    client_socket.send(data)
            except FileNotFoundError:
                client_socket.send("[!] File not found".encode())
        elif request.startswith("upload"):
            file_name = request.split()[1]
            data = client_socket.recv(1024)
            with open(f"server_files/{file_name}", "wb") as file:
                file.write(data)
            client_socket.send("[+] File uploaded successfully".encode())
    
    print(f"[-] Connection from {client_address} closed")
    client_socket.close()

# Main server function
def main():
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 9999))
    server_socket.listen(5)
    print("[+] Server started")

    # Create folder for server files if not exists
    if not os.path.exists("server_files"):
        os.makedirs("server_files")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
    except KeyboardInterrupt:
        print("[!] Server shutting down")
        server_socket.close()

if __name__ == "__main__":
    main()
