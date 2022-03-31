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

import socket, time


class ParsingServer(object):
    def __init__(self, port=2023):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostname = socket.gethostname() or 'localhost'
        self.serversocket.bind(('localhost', port))

    def start(self):
        # become a server socket, maximum 10 connections
        self.serversocket.listen(5) 
        while True:
            connection, address = self.serversocket.accept()
            sender_host, sender_port = address
            try:
                connection.settimeout(50)
                while True:
                    buf = connection.recv(1024)
                    if len(buf) > 0:
                        connection.send("Approved".encode('utf-8'))
                        text = buf.decode('utf-8')
                        print(f"{sender_host}:{sender_port} says \n{text}")
                        if text == 'end':
                            connection.close()
                            break
            except socket.timeout:
                print("timeout")
            print(f"Closing current connection: {sender_host}:{sender_port}")
            connection.close()


class ParsingClient(object):
    def __init__(self, port=2023):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect(('localhost', port))
    
    def send(self, text):
        self.clientsocket.send(text.encode('utf-8'))
        print(self.clientsocket.recv(1024))
        if text == 'end':
            self.clientsocket.close()


if __name__ == '__main__':
    ps = ParsingServer()
    ps.start(2023)