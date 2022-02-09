





end = "EOM".encode("utf-8")
def check_end(data: bytes):
    ind = data.find(end)
    if ind == -1:
        return False
    else:
        return data[0:ind], data[ind+len(end):]




print(check_end("I need some dataEOMOr some other data ig".encode("utf-8")))