from socket import *
from threading import Thread

IP = "192.168.0.171"
PORT = 8848
ADDR = (IP, PORT)
sensitive_words = ["xx", "aa", "bb", "oo"]  # 屏蔽语
list_black = []  # 黑名单
DICT_USER = {}  # 当前登录用户


class ChatServer:


    def __init__(self):
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.bind(ADDR)
        print("盗版QQ服务器启动～")

    def main(self):
        t = Thread(target=self.run)
        t.setDaemon(True)
        t.start()
        self.send_manager()

    def send_manager(self):
        while True:
            msg = input("管理员消息：")
            msg = "Chat 管理员 " + msg
            self.s.sendto(msg.encode(),ADDR)

    def run(self):
        while True:
            data, addr = self.s.recvfrom(4080)
            data_info = data.decode().split(" ", 2)
            if data_info[0] == "Login":
                self._do_login(data_info[1], addr)
            elif data_info[0] == "Chat":
                self._do_chat(data_info[1], data_info[2])
            elif data_info[0] == "Exit":
                pass

    def _do_login(self, name, addr):
        """
        登录功能
        :param name: 姓名
        :param addr: ip地址
        """
        if name in DICT_USER or '管理' in name or addr in list_black:
            self.s.sendto("FAIL".encode(), addr)
        else:
            self.s.sendto("OK".encode(), addr)
            for key in DICT_USER:
                self.s.sendto(("欢迎%s加入聊天室" % name).encode(), DICT_USER[key][0])
            DICT_USER[name] = [addr, 0]

    def _do_chat(self, name, content):
        """
        聊天功能
        :param name: 用户名
        :param content: 聊天内容
        """
        if self.deal_msg(content, name):
            msg = "%s :%s" % (name, content)
            for key in DICT_USER:
                if name != key:
                    self.s.sendto(msg.encode(), DICT_USER[key][0])
        else:
            if DICT_USER[name][0] in list_black:
                msg = "系统：%s存在违规行为，已被退出聊天室" % name
                for key in DICT_USER:
                    if name != key:
                        self.s.sendto(msg.encode(), DICT_USER[key][0])
                    else:
                        self.s.sendto("EXIT".encode(), DICT_USER[name][0])
                del DICT_USER[name]
            else:
                self.s.sendto("存在敏感词，请注意".encode(), DICT_USER[name][0])

    def deal_msg(self, info, user):
        """
        关键字处理
        :param info: 消息内容
        :param user: 用户名
        """
        for word in sensitive_words:
            if word in info:
                DICT_USER[user][1] += 1
                self.append_black_name(user)
                return False
        return True

    @staticmethod
    def append_black_name(user):
        """
        黑名单添加
        :param user: 用户名
        """
        if DICT_USER[user][1] >= 3:
            list_black.append(DICT_USER[user][0])


if __name__ == '__main__':
    server = ChatServer()
    server.main()
