import ClientGUIRework as GUI
import ClientReceiver as Receiver
import ClientSender as Sender
import json
import socket
import time


class Client:

    def __init__(self, client_name: str):

        # Initialises the server connection settings to the external IP of server
        self.host = "80.2.69.224"

        # self.host = "192.168.0.15"
        self.port = 7000  # socket server port number

        self.client_socket = socket.socket()  # instantiate

        self.client_name = client_name

    def run(self):

        while True:
            # Wait for client to find connection to server
            try:
                self.client_socket.connect((self.host, self.port))  # connect to the server
                break
            except ConnectionRefusedError:
                print("waiting for server...")
                time.sleep(1)

        # send initial message to server of client name
        init_msg = json.dumps({"name": self.client_name})
        self.client_socket.send(init_msg.encode())

        data_received = self.client_socket.recv(1024).decode()  # receive response
        print(data_received)  # show in terminal

        # Create a Sender for the client
        sender = Sender.ClientSender(self.client_socket)

        # Create a GUI for the client
        gui = GUI.ClientGUIHomepage(self.client_name, self.client_socket, sender)

        # Create a Receiver for the client and start its process.
        receiver = Receiver.ClientReceiver(self.client_socket, gui)
        receiver.run()

        # Run the GUI process
        gui.run()
