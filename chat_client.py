from socket import *
from multiprocessing import Process
import sys


class ChatClient:
    IP = "192.168.0.171"
    PORT = 8848
    ADDR = (IP, PORT)

    def __init__(self):
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.p = Process(target=self._recv_msg)

    def main(self):
        self._login()

    def _login(self):
        while True:
            self.name = input("请输入您的姓名：")
            msg = "Login " + self.name
            self.s.sendto(msg.encode(), ChatClient.ADDR)
            data, addr = self.s.recvfrom(4080)
            if data.decode() == "OK":
                print("登录成功")
                break
            else:
                print(data.decode())
        self._chat()

    def _chat(self):
        self.p.daemon = True
        self.p.start()
        self._send_msg()

    def _send_msg(self):
        while True:
            # 异常退出
            try:
                text = input(">>")
            except:
                text = "exit"
            # 指令退出
            if text == "exit":
                msg = "Exit"
                self.s.sendto(msg.encode(), ChatClient.ADDR)
                sys.exit()
            msg = "Chat %s " % self.name + text
            if self.p.is_alive():
                self.s.sendto(msg.encode(), ChatClient.ADDR)
            else:
                sys.exit()

    def _recv_msg(self):
        while True:
            data, addr = self.s.recvfrom(4080)
            if data == b"EXIT":
                sys.exit()
            else:
                print("\n" + data.decode() + "\n>>", end="")


if __name__ == '__main__':
    client = ChatClient()
    client.main()



