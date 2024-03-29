# -*- coding: UTF-8 -*-
# =====================================================
#   Copyright (C) since 2022 All rights reserved.
#
#   filename : parsing_server.py
#   author   : okcd00 / okcd00@qq.com
#   date     : 2022-03-31
#   desc     : A simple socket server and client 
#              for interaction between different processes.
# =====================================================
import json
import time
import socket


class ParsingServer(object):
    BUFSIZE = 1024
    PONAZU_PORT = 2020

    def __init__(self, port=2023):
        self.serversocket = None
        self.clientsocket = None
        self._BUFSIZE = 1024
        self.new_server(port=port)
        self.new_client(port=self.PONAZU_PORT)

    def new_server(self, port=2023):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind(('localhost', port))

    def new_client(self, port=2020):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.bind(('localhost', port))

    def send_command(self, command):
        json_str = json.dumps({'command': command})
        self.clientsocket.send(json_str.encode('utf-8'))
        print(self.clientsocket.recv(1024))

    def start_server(self, exit_msg="<CLIENT_ENDS>"):
        # become a server socket, maximum 10 connections
        self.serversocket.listen(5) 
        while True:
            connection, address = self.serversocket.accept()
            sender_host, sender_port = address
            try:
                connection.settimeout(100)
                while True:
                    buf = connection.recv(64, socket.MSG_WAITALL)
                    if len(buf) > 0:
                        # connection.send("Received".encode('utf-8'))
                        connection.sendall(f"{buf}".encode('utf-8'))
                        text = buf.decode('utf-8')
                        print(f"[{time.ctime()}] {sender_host}:{sender_port} says \n{text}")
                        if text == exit_msg:
                            connection.close()
                            break
            except socket.timeout:
                print("timeout")
            print(f"Closing current connection: {sender_host}:{sender_port}")
            connection.close()


if __name__ == '__main__':
    ps = ParsingServer()
    ps.start_server()
