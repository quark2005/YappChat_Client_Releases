import ClientGUIRework as GUI
import json
import socket
import threading


class ClientReceiver:

    def __init__(self, client_socket: socket, gui: GUI.ClientGUIHomepage):
        self.online_users = list()
        self.client_socket = client_socket
        self.gui = gui

    def run(self):
        """ Creates Receiver Thread"""
        x = threading.Thread(target=self.receiver)
        x.start()

    def receiver(self):
        """ Receives Data from Socket\n
            This method MUST be run in a Thread """

        print("Receiver Running")

        while True:
            try:
                data_received = self.client_socket.recv(1024).decode()
            except WindowsError:
                print("\nConnection Aborted")
                break

            data_received = json.loads(data_received)
            print("1", data_received)

            if data_received["type"] == "message":
                received_from = data_received["from"]
                message_received = data_received["msg"]

                self.gui.update_incoming_message_box(received_from, message_received)

            elif data_received["type"] == "rejected_msg":
                reasons_for_reject = data_received["reasons"]
                self.gui.show_warning("MSG_VERIFICATION_ERR", reasons_for_reject)

            elif data_received["type"] == "profanity_warning_msg":
                self.gui.show_warning("PROFANITY_WARNING", "You speak to your mother with that mouth?")

            elif data_received["type"] == "rejected_name":
                reasons_for_reject = data_received["reasons"]
                self.gui.show_warning("MSG_VERIFICATION_ERR", reasons_for_reject)
                self.gui.settings_page.change_name(data_received["old_name"])

            elif data_received["type"] == "profanity_warning_name":
                self.gui.show_warning("PROFANITY_WARNING", "You speak to your mother with that mouth?")
                self.gui.settings_page.change_name(data_received["old_name"])

            elif data_received["type"] == "room_id_invalid":
                self.gui.show_warning("ROOM DOES NOT EXIST", f"The room {data_received['room_id']} does not exist")

            elif data_received["type"] == "name_changed":
                print("1")
                old_name = data_received["old_name"]
                new_name = data_received["new_name"]
                self.gui.update_incoming_message_box("===>", f"{old_name} has changed their name to {new_name}")

            elif data_received["type"] == "user_list":
                online_users: list = data_received["users"]
                print(f"Users Online: {online_users}")
                # self.gui.update_online_user_text(online_users)
