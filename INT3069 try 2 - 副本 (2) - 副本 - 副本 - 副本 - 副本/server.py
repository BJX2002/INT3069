import socket
import threading
import csv
import os
from datetime import datetime

def init_files():
    open('users.csv', 'a').close()

def register_user(user_id, password):
    with open('users.csv', 'a+', newline='') as file:
        file.seek(0)
        existing_users = {row[0] for row in csv.reader(file) if row}
        if user_id in existing_users:
            return "Username already exists."
        csv.writer(file).writerow([user_id, password])
        open(f'{user_id}_friends.csv', 'a').close()
        open(f'{user_id}_messages.csv', 'a').close()
    return "Signup successful."

def authenticate_user(user_id, password):
    with open('users.csv', 'r') as file:
        for row in csv.reader(file):
            if row == [user_id, password]:
                return True
    return False

def add_friend(user_id, friend_id):
    if not os.path.exists(f'{friend_id}_friends.csv'):
        return "Friend ID does not exist."
    with open(f'{user_id}_friends.csv', 'a+', newline='') as file:
        file.seek(0)
        if any(friend_id == row[0] for row in csv.reader(file)):
            return "Already friends."
        csv.writer(file).writerow([friend_id])
    return "Friend added successfully."

def send_message(sender_id, receiver_ids, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    receivers = receiver_ids.split(';')
    message_records = []
    for receiver_id in receivers:
        if os.path.exists(f'{receiver_id}_messages.csv'):
            with open(f'{sender_id}_messages.csv', 'a', newline='') as sender_file:
                csv.writer(sender_file).writerow([sender_id, receiver_id, message, timestamp])
            with open(f'{receiver_id}_messages.csv', 'a', newline='') as receiver_file:
                csv.writer(receiver_file).writerow([sender_id, receiver_id, message, timestamp])
            print(f"user {sender_id} to user {receiver_id} {timestamp}: {message}")
            message_records.append(receiver_id)
    if not message_records:
        return "Message failed, no valid receivers."
    return f"Message sent to: {', '.join(message_records)}"

def handle_file_transfer(sender_id, receiver_id, content):
    # meishi ganjuebukaopu woc
    """Handles sending a text file's content as a message."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if os.path.exists(f'{receiver_id}_messages.csv'):
        with open(f'{sender_id}_messages.csv', 'a', newline='') as sender_file:
            csv.writer(sender_file).writerow([sender_id, receiver_id, content, timestamp])
        with open(f'{receiver_id}_messages.csv', 'a', newline='') as receiver_file:
            csv.writer(receiver_file).writerow([sender_id, receiver_id, content, timestamp])
        print(f"user {sender_id} sent file content to user {receiver_id} {timestamp}")
        return "File sent successfully."
    return "File sending failed, receiver not found."

def client_handler(conn, clients):
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            command, *args = data.split(',')
            if command == 'signup':
                response = register_user(*args)
            elif command == 'login':
                if authenticate_user(*args):
                    clients[conn] = args[0]
                    response = "Login successful."
                else:
                    response = "Login failed."
            elif command == 'add_friend':
                if conn in clients:
                    response = add_friend(clients[conn], *args)
                else:
                    response = "Authentication required."
            elif command == 'message':
                if conn in clients:
                    response = send_message(clients[conn], *args)
                else:
                    response = "Authentication required."
            elif command == 'send_file':
                if conn in clients:
                    sender_id = clients[conn]
                    receiver_id, file_content = args
                    response = handle_file_transfer(sender_id, receiver_id, file_content)
                else:
                    response = "Authentication required."
            else:
                response = "Invalid command."
            conn.sendall(response.encode('utf-8'))
    finally:
        conn.close()
        clients.pop(conn, None)
        print(f"Connection closed for {conn}")

def server_listen():
    host, port = '127.0.0.1', 65432
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    clients = {}
    print("Server is listening...")
    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        threading.Thread(target=client_handler, args=(conn, clients)).start()

if __name__ == "__main__":
    init_files()
    server_listen()
