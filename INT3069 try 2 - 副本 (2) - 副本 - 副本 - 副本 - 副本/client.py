import socket

def send_request(sock, request):
    sock.send(request.encode('utf-8'))
    return sock.recv(1024).decode('utf-8')

def client_interface():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 65432))
        while True:
            print("\n1. Signup\n2. Login\n3. Send Message\n4. Add Friend\n5. Send File\n6. Review Messages\n7. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                user_id = input("Enter user ID: ")
                password = input("Enter password: ")
                print(send_request(sock, f"signup,{user_id},{password}"))
            elif choice == '2':
                user_id = input("Enter user ID: ")
                password = input("Enter password: ")
                print(send_request(sock, f"login,{user_id},{password}"))
            elif choice == '3':
                receivers = input("Enter receiver's user IDs separated by ';': ")
                message = input("Type your message: ")
                print(send_request(sock, f"message,{receivers},{message}"))
            elif choice == '4':
                friend_id = input("Enter friend's user ID to add: ")
                print(send_request(sock, f"add_friend,{friend_id}"))
            elif choice == '5':
                receiver_id = input("Enter receiver's user ID: ")
                file_path = input("Enter text file path: ")
                try:
                    with open(file_path, 'r') as file:
                        file_content = file.read()
                    print(send_request(sock, f"send_file,{receiver_id},{file_content}"))
                except FileNotFoundError:
                    print("File not found.")
            elif choice == '9':
                # show friend list
                # use a loop read the csv and show all
                # cnm buxiangkaohsi
                pass
            elif choice == '8':
                # show all message by reading the csv file
                # even can add a filter if i want to only check xx's message
                # cccccc
                pass
            elif choice == '6':
                print("Fetching sent messages...")
                # This would require implementing a function to fetch messages from the server
            elif choice == '7':
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    client_interface()
