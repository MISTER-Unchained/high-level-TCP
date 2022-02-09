import socket

HOST = "0.0.0.0"
PORT = 5000

end = "EOM".encode("utf-8")


def check_valid_message(mes: bytes):
    if mes.find(end) == -1:
        return True
    else:
        return False


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        mes = (input("enter message:")).encode("utf-8")
        if check_valid_message(mes):
            s.sendall(mes + end)
        else:
            print("invalid message")
            continue