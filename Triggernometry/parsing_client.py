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


class ParsingClient(object):
    def __init__(self, port=2020):
        self.clientsocket = None
        self.port = port
        self.renew_client(port)

    def renew_client(self, port=None):
        port = port or self.port
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect(('localhost', port))

    def sent_data(self, text=None):
        """
        发送数据,短连接
        :param data: 要发送的数据 [str]
        :return: 收到的服务端发来的数据或状态 [str]
        """
        if text:
            self.clientsocket.sendall(text.encode('utf-8'))
            recv = self.clientsocket.recv(1024)
            self.clientsocket.close()
            return recv
        else:
            print("The sent data is empty or not sent!")

    def sent_data_pending_input(self, exit_msg="<CLIENT_ENDS>"):
        """
        发送数据，长连接
        """
        lastdata = ''
        while lastdata != "quit":
            lastdata = input("请输入要发送的数据：")
            lastdata = json.dumps({'command': lastdata})
            if len(lastdata) > 0:
                try:
                    self.clientsocket.sendall(lastdata.encode("utf-8"))
                    recv = self.clientsocket.settimeout(10)
                    recv = self.clientsocket.recv(64)
                    print(recv.decode("utf-8"))
                except BrokenPipeError:
                    self.renew_client()
                    print("Renew Connection")
            else:
                print("The sent data is empty or not sent!")
        self.clientsocket.sendall(exit_msg.encode("utf-8"))
        print("Client Closed.")
        self.clientsocket.close()


if __name__ == '__main__':
    ps = ParsingClient()
    ps.sent_data_pending_input()