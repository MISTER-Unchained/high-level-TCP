import socket
import threading as th

HOST = "localhost"
PORT = 5000



global_socket = None

end = "$EOM".encode("utf-8")
close = "$CLOSE_ENTIRE_CONNECTION".encode("utf-8")
def check_valid_message(mes: bytes):
    if mes.find(end) == -1:
        return True
    else:
        return False

def check_end(data: bytes):
    ind = data.find(end)
    if ind == -1:
        return False, data
    else:
        return data[0:ind], data[ind+len(end):]

def handle_data(output):
    return (f"ok + {output}").encode("utf-8")

def connection_handler(out_fun: function):
    global global_socket
    data = bytes()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        global_socket = s
        s.connect((HOST, PORT))
        while True:
            data += s.recv(1024)
            output, data = check_end(data)
            if output:
                return_data = out_fun(output)
                if return_data != None:
                    if check_valid_message(return_data):
                        if return_data.find(close) == -1:
                            s.sendall(return_data + end)
                        else:
                            s.sendall(return_data + end + close)
                    else:
                        raise("Contained invalid data")
            if data.find(close) != -1:
                s.sendall(close)
                print("connection closed")
                break
    print("exiting")

def get_input_loop():
    global global_socket
    while True:
        datatosend = input("enter command:").encode("utf-8")
        if datatosend == close:
            global_socket.sendall(close)
            break
        else:
            global_socket.sendall(datatosend + end)
get_input_loop()