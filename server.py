import socket


def main(out_fun, HOST, PORT):
    end = "$EOM".encode("utf-8")
    close = "$CLOSE_ENTIRE_CONNECTION".encode("utf-8")
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
                    return_data = out_fun(output)
                    if return_data != None:
                        if check_valid_message(return_data):
                            if return_data.find(close) == -1:
                                conn.sendall(return_data + end)
                            else:
                                conn.sendall(return_data + end + close)
                        else:
                            raise("Contained invalid data")
                if data.find(close) != -1:
                    conn.sendall(close)
                    print("connection closed")
                    break
    print("exiting")

