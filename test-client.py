import client
from time import sleep


HOST = "localhost"
PORT = 5000

def inp_f():
    sleep(0.2)
    return (input("enter_input:")).encode("utf-8")


def cb(input):
    print(f"received data: {input}")
    return None

client.main(inp_f, cb, HOST, PORT)