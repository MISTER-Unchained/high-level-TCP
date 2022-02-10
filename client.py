import socket
import threading as th


def main(input_fun, call_back_fun, HOST, PORT):
    global_socket = None

    running = 1

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


    def connection_handler(out_fun):
        nonlocal global_socket
        nonlocal running
        data = bytes()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            global_socket = s
            while running:
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
                            raise Exception("Contained invalid data")
                if data.find(close) != -1:
                    s.sendall(close)
                    running = False
                    print("connection closed")
                    break
        raise Exception("Error occured in call-back")

    def get_input_loop(inp_fun):
        nonlocal running
        nonlocal global_socket
        while running:
            datatosend = inp_fun()
            if check_valid_message(datatosend):
                if datatosend == close:
                    global_socket.sendall(close)
                    running = False
                    break
                else:
                    global_socket.sendall(datatosend + end)
            else:
                raise("Contained invalid data")
        raise Exception("Error occured in input-loop")

    
    th1 = th.Thread(target=connection_handler, daemon=True, args=(call_back_fun, ))
    th2 = th.Thread(target=get_input_loop, daemon=True, args=(input_fun, ))
    th2.start()
    th1.start()
    th2.join()
    th1.join()
