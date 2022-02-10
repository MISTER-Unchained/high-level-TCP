import server

HOST = "localhost"
PORT = 5000

def cb(input):
    return input

server.main(cb, HOST, PORT)