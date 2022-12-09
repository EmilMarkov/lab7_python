import socket

HOST = "127.0.0.1"
PORT = 50007

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))

while True:
    email = input("Email: ").encode("utf-8")
    text = input("Text: ").encode("utf-8")
    server.send((email))
    server.send((text))