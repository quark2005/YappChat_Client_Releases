import ClientSender as Sender
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import tkinter.scrolledtext as scrlltxt
import socket
import json
import time


class ClientGUIChatRoom:
    def __init__(self, client_name: str, client_socket: socket.socket, sender: Sender.ClientSender):

        self.sender = sender
        self.client_name = client_name
        self.client_socket = client_socket

        self.online_users_list: list = []
        self.dropdown_options: list[str] = []
        self.old_time_sent = 0.0

        self.client_gui_chatroom = tk.Tk()
        self.client_gui_chatroom.geometry("1000x750")
        self.client_gui_chatroom.resizable(False, False)
        self.client_gui_chatroom.title(f"Chat Service Client - {client_name}")
        self.client_gui_chatroom.protocol("WM_DELETE_WINDOW", self.window_closed)

        self.root = tk.Frame(self.client_gui_chatroom, bg="grey")
        self.root.place(width=1000, height=750, x=0, y=0)

        self.left_frame = tk.Frame(self.root, bg="orange")
        self.left_frame.place(width=485, height=730, x=10, y=10)

        self.right_frame = tk.Frame(self.root, bg="red")
        self.right_frame.place(width=485, height=730, x=505, y=10)

        self.online_users_frame = tk.Frame(self.left_frame, bg="pink")
        self.online_users_frame.place(width=455, height=330, x=15, y=15)

        tk.Label(self.online_users_frame, text="Online Users:", font=("Arial", 13), bg="pink").place(x=175, y=10)
        self.online_users_text = tk.Text(self.online_users_frame, state="disabled")
        self.online_users_text.place(width=435, height=285, x=10, y=35)

        self.text_to_send_frame = tk.Frame(self.left_frame, bg="cyan")
        self.text_to_send_frame.place(width=455, height=370, x=15, y=345)

        self.text_to_send_box = tk.Text(self.text_to_send_frame)
        self.text_to_send_box.place(width=435, height=300, x=10, y=10)

        # self.send_to_dropdown = ttk.Combobox(self.text_to_send_frame, state="readonly", values=self.dropdown_options)
        # self.send_to_dropdown.place(width=340, height=40, x=10, y=320)

        self.send_message_button = tk.Button(self.text_to_send_frame, text="Send", command=self.send_message)
        self.send_message_button.place(width=85, height=40, x=360, y=320)

        self.incoming_messages_box = scrlltxt.ScrolledText(self.right_frame, state="disabled", background="light grey")
        self.incoming_messages_box.place(width=455, height=700, x=15, y=15)

    def run(self):
        """ Runs Tkinter MainLoop """

        self.client_gui_chatroom.mainloop()

    def update_online_user_text(self, online_users_list: list[str]):
        """ Updates Users Online Box """

        self.online_users_list = online_users_list
        self.online_users_list.remove(self.client_name)

        self.online_users_text.config(state="normal")
        self.online_users_text.delete("0.0", tk.END)
        for user in self.online_users_list:
            # self.send_to_dropdown["values"] = self.dropdown_options + [user]
            # self.dropdown_options.append(user)

            self.online_users_text.insert("end", user + "\n")
        self.online_users_text.config(state="disabled")

    def update_incoming_message_box(self, received_from: str, message_received: str):
        """ Adds Message to Incoming Message Box when Received """

        self.incoming_messages_box.config(state="normal")
        message_to_add = received_from + ": " + message_received + "\n"
        self.incoming_messages_box.insert("end", message_to_add)
        self.incoming_messages_box.config(state="disabled")

        self.incoming_messages_box.see(tk.END)

    def send_message(self):
        """ Gets Message from text box\n
            Gives Message to ClientSender """

        message_to_send = self.text_to_send_box.get(1.0, "end-1c")
        # send_to = self.send_to_dropdown.get()
        time_sent = time.time()
        print(message_to_send)

        valid: bool = self.message_verification(message_to_send, time_sent)
        if valid:
            self.sender.send_message(message_to_send)
            self.text_to_send_box.delete("1.0", tk.END)

    def window_closed(self):
        """ Initiates when GUI Window Closes """

        data_to_send = {"type": "conn_shutdown"}
        data_to_send = json.dumps(data_to_send)
        self.client_socket.send(data_to_send.encode())

        self.client_gui_chatroom.destroy()
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()

    def message_verification(self, message: str, time_sent: float):
        """ Validates Message being Sent"""

        warning_message = ""

        if message == "":
            warning_message += "Message Box Empty.\n"
        if len(message) > 1024:
            warning_message += "Message Too Long. Max Length 1024, Your Message: " + str(len(message)) + "\n"
        if message.count("\n") > len(message) // 10:
            warning_message += "Enter Spam Detected.\n"
        if time_sent - self.old_time_sent <= 1.0:
            warning_message += "Message Spam Detected"

        self.old_time_sent = time.time()

        if warning_message == "":
            return True
        else:
            msgbox.showerror(title="MSG_VERIFICATION_ERR", message=warning_message)
            return False

