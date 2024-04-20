import socket

# Function to connect to server
def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9999))
    return client_socket

# Function to list files on server
def list_files():
    client_socket = connect_to_server()
    client_socket.send("list".encode())
    files = client_socket.recv(1024).decode()
    print("Files on server:")
    print(files)

# Function to download file from server
def download_file(file_name):
    client_socket = connect_to_server()
    client_socket.send(f"download {file_name}".encode())
    data = client_socket.recv(1024)
    if data.decode() == "[!] File not found":
        print("[!] File not found on server")
    else:
        with open(file_name, "wb") as file:
            file.write(data)
        print("[+] File downloaded successfully")

# Function to upload file to server
def upload_file(file_name):
    client_socket = connect_to_server()
    client_socket.send(f"upload {file_name}".encode())
    with open(file_name, "rb") as file:
        data = file.read()
        client_socket.send(data)
    print("[+] File uploaded successfully")

# Main function
def main():
    while True:
        print("\nOptions:")
        print("1. List files on server")
        print("2. Download file from server")
        print("3. Upload file to server")
        print("4. Disconnect from server")
        choice = input("Enter choice: ")

        if choice == "1":
            list_files()
        elif choice == "2":
            file_name = input("Enter file name to download: ")
            download_file(file_name)
        elif choice == "3":
            file_name = input("Enter file name to upload: ")
            upload_file(file_name)
        elif choice == "4":
            break
        else:
            print("[!] Invalid choice")

if __name__ == "__main__":
    main()
