import server

HOST = "localhost"
PORT = 5000

def cb(input):
    return input

server.logging = True
server.main(cb, HOST, PORT)