import socket

HOST = "0.0.0.0"
PORT = 5000


def handle_data(output):
    print(output)


end = "EOM".encode("utf-8")
close = "CLOSE_ENTIRE_CONNECTION".encode("utf-8")
def check_end(data: bytes):
    ind = data.find(end)
    if ind == -1:
        return False, data
    else:
        return data[0:ind], data[ind+len(end):]

def check_valid_message(mes: bytes):
    if mes.find(end) == -1:
        return True
    else:
        return False


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by: @{addr}")
        data = bytes()
        while True:
            data += conn.recv(1024)
            output, data = check_end(data)
            if output:
                handle_data(output.decode("utf-8"))
            if data.find(close) != -1:
                print("connection closed")
                break

            