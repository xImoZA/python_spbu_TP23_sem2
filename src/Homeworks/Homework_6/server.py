import random
import socket
from threading import Thread

from loguru import logger


class Server:
    def __init__(self, cur: int, first: int, second: int) -> None:
        self.cur = cur
        self.first = first
        self.second = second

    def give_response(
        self, self_sock: tuple[socket.socket, str], other_sock: tuple[socket.socket, str], data: bytes
    ) -> None:
        def swap() -> None:
            if self.cur == self.first:
                self.cur = self.second
            else:
                self.cur = self.first

        message, received_port = data.decode().split()
        if str(message) == "?":
            if int(received_port) == self.cur:
                self_sock[0].sendall(bytes("you", encoding="UTF-8"))
                logger.info(f"The message b'you' has been sent to {self_sock[1]}")
            else:
                self_sock[0].sendall(bytes("not you", encoding="UTF-8"))
                logger.info(f"The message b'not you' has been sent to {self_sock[1]}")

        elif int(received_port) == self.cur:
            other_sock[0].sendall(data)
            logger.info(f"The message {str(data)} has been sent to {other_sock[1]}")
            swap()

    def get_data(self, self_sock: tuple[socket.socket, str], other_sock: tuple[socket.socket, str]) -> None:
        conn, addr = self_sock
        while True:
            data = conn.recv(1024)
            if data:
                logger.info(f"The message {str(data)} was received from {self_sock[1]}")
                self.give_response(self_sock, other_sock, data)
            else:
                conn.close()
                logger.info(f"{addr} has been disconnected")
                break


def main(ip: str, port: int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind((ip, port))
    sock.listen(2)
    logger.info(f"Started server with ip: {ip}, port: {port}")

    server = Server(0, 0, 0)
    while True:
        conn1, addr1 = sock.accept()
        logger.info(f"Connected from {addr1}")
        conn2, addr2 = sock.accept()
        logger.info(f"Connected from {addr2}")

        server.first = addr1[1]
        server.second = addr2[1]
        server.cur = random.choice([server.first, server.second])

        thread_1 = Thread(target=server.get_data, args=((conn1, addr1), (conn2, addr2)))
        thread_2 = Thread(target=server.get_data, args=((conn2, addr2), (conn1, addr1)))
        thread_1.start()
        thread_2.start()


if __name__ == "__main__":
    main("127.0.0.1", 12345)
