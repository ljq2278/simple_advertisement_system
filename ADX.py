import socket
import numpy as np
import json
import threading
from threading import Thread
# import multiprocessing
# from multiprocessing import Process

class MySocket:
    def __init__(self,socket,address):
        self.sk = socket
        self.address = address

    def acceptAndProcessMsg(self):
        data = "port %d"%self.address[1] + " connect success!"
        self.sk.send(data.encode())
        try:
            while True:
                # 接收客户端消息
                data = self.sk.recv(1024)
                print("port %d: "%self.address[1]+data.decode())
                # 接收到退出指令
                if data == b'exit':
                    break
                # 处理客户端信息 本实例直接将接收到的消息重新发回去
                self.sk.send(data)
        finally:
            self.sk.close()

class ADX:
    def __init__(self):
        # self.portList = [5000,5001,5002,5003,5004]
        self.all_connection = {}
        # socket.setdefaulttimeout(2.0)

    def main(self):
        sk = socket.socket()
        # 绑定IP与端口
        ip_port = ('127.0.0.1', 8888)
        # 绑定监听
        sk.bind(ip_port)
        # 最大连接数
        sk.listen(1)
        # 不断循环 处理接入请求
        while True:
            print("线程数: %d" % threading.active_count())
            print("正在等待接收数据。。。。")
            # 接受数据  连接对象与客户端地址
            connSocket, address = sk.accept()
            newConnSocket = MySocket(connSocket,address)
            thread = Thread(target=newConnSocket.acceptAndProcessMsg)
            thread.start()

adx = ADX()
adx.main()