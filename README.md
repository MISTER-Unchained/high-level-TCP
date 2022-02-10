# A semi-high-level TCP server & client.

## What does it do?
This module makes it very easy to start and run a TCP server in python without having to worry about splitting messages and closing connections.

## Examples:

A simple client that let's you enter some data and prints the received data.
```python
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
```

A simple server that echoes the received data.
(Set ```server.logging``` to ```False``` to disable debugging)

```python
import server

HOST = "localhost"
PORT = 5000

def cb(input):
    return input
    
server.logging = True

server.main(cb, HOST, PORT)

```
