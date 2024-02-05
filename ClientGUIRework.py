import ClientSender
import ClientSender as Sender
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import tkinter.scrolledtext as scrlltxt
import socket
import json


class ClientGUICustomSettings:
    colour_schemes = {
        "Pastel Khaki": (
            "#6A7152",
            "#CCD5AE",
            "#E9EDC9",
            "#FEFAE0",
            "#FAEDCD"
        ),
        "Pastel Pinks": (
            "#FF9494",
            "#FFD1D1",
            "#FFE3E1",
            "#FFF5E4"
        ),
        "eye_sore.exe": (
            "#FF1F0F",
            "#F811F5",
            "#15A1FF",
            "#010101"
        )
    }  # Available colour schemes the user could choose

    current_colour_scheme = "Pastel Khaki"

    @classmethod
    def get_colour_scheme(cls, ret=""):
        if ret == "key":
            return cls.current_colour_scheme
        else:
            return cls.colour_schemes.get(cls.current_colour_scheme)

    @classmethod
    def set_colour_scheme(cls, new_scheme):
        if new_scheme in cls.colour_schemes.keys():
            cls.current_colour_scheme = new_scheme
            return 0
        else:
            return 1


class ClientGUIHomepage:
    def __init__(self, client_name: str, client_socket: socket.socket, client_sender: Sender.ClientSender):
        self.client_sender = client_sender
        self.client_name = client_name
        self.client_socket = client_socket

        self.isSettingsWinOpen = False
        self.isRoomAdminWinOpen = False
        self.isAddBuddyWinOpen = False
        self.isMessageBuddyWinOpen = False
        self.isCreateRoomWinOpen = False
        self.isJoinRoomWinOpen = False
        self.isLeaveRoomWinOpen = False

        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.client_gui_homepage = tk.Tk()
        self.client_gui_homepage.geometry("1000x750")
        self.client_gui_homepage.resizable(False, False)
        self.client_gui_homepage.title(f"YappChat - {client_name}")
        self.client_gui_homepage.protocol("WM_DELETE_WINDOW", self.window_closed)

        # Defining Tkinter widget variables in __init__ #
        if True:
            self.root = None
            self.left_frame = None
            self.buddy_list_label = None
            self.buddy_list_box = None
            self.add_buddy_button = None
            self.message_buddy_button = None
            self.app_settings_button = None
            self.room_admin_button = None
            self.create_room_button = None
            self.join_room_button = None
            self.leave_room_button = None
            self.right_frame = None
            self.incoming_messages_box = None
            self.text_to_send_box = None
            self.send_message_button = None
            self.add_buddy_page = None
            self.message_buddy_page = None
            self.settings_page = None
            self.room_admin_page = None
            self.create_room_page = None
            self.join_room_page = None
            self.leave_room_page = None

        self.format_window()

    def format_window(self):
        self.root = tk.Frame(self.client_gui_homepage, bg=self.colour_list[1])
        self.root.place(width=1000, height=750, x=0, y=0)

        self.left_frame = tk.Frame(self.root, bg=self.colour_list[0])
        self.left_frame.place(width=250, height=730, x=10, y=10)

        self.right_frame = tk.Frame(self.root, bg=self.colour_list[0])
        self.right_frame.place(width=720, height=730, x=270, y=10)

        self.format_select_bar()
        self.format_chatroom_area()

    def format_select_bar(self):
        """ Subroutine that formats Tk for selection bar """

        self.buddy_list_label = tk.Label(self.left_frame, text="Buddy List", font=("Arial", 20), bg=self.colour_list[0],
                                         foreground="White")
        self.buddy_list_label.pack()
        self.buddy_list_box = tk.Text(self.left_frame, state="disabled")
        self.buddy_list_box.place(width=240, height=270, x=5, y=35)

        self.add_buddy_button = tk.Button(self.left_frame, text="Add Buddy", font=("Arial", 15),
                                          command=lambda: ClientGUIAddBuddyPage.open_window(self))
        self.add_buddy_button.place(width=240, height=50, x=5, y=315)

        self.message_buddy_button = tk.Button(self.left_frame, text="Message Buddy", font=("Arial", 15),
                                              command=lambda: ClientGUIMessageBuddyPage.open_window(self))
        self.message_buddy_button.place(width=240, height=50, x=5, y=365)

        self.app_settings_button = tk.Button(self.left_frame, text="App Settings", font=("Arial", 15),
                                             command=lambda: ClientGUISettingsPage.open_window(self,
                                                                                               self.client_socket,
                                                                                               self.client_sender,
                                                                                               self.client_name))
        self.app_settings_button.place(width=240, height=50, x=5, y=435)

        self.room_admin_button = tk.Button(self.left_frame, text="Room Admin", font=("Arial", 15),
                                           command=lambda: ClientGUIRoomAdminPage.open_window(self))
        self.room_admin_button.place(width=240, height=50, x=5, y=485)

        self.create_room_button = tk.Button(self.left_frame, text="Create Room", font=("Arial", 15),
                                            command=lambda: ClientGUICreateRoomPage.open_window(self, self.client_sender))
        self.create_room_button.place(width=240, height=50, x=5, y=550)

        self.join_room_button = tk.Button(self.left_frame, text="Join Room", font=("Arial", 15),
                                          command=lambda: ClientGUIJoinRoomPage.open_window(self, self.client_sender))
        self.join_room_button.place(width=240, height=50, x=5, y=600)

        self.leave_room_button = tk.Button(self.left_frame, text="Leave Room", font=("Arial", 15),
                                           command=lambda: ClientGUILeaveRoomPage.open_window(self))
        self.leave_room_button.place(width=240, height=50, x=5, y=650)

    def format_chatroom_area(self):
        """ Subroutine that formats the chatroom area"""
        self.incoming_messages_box = scrlltxt.ScrolledText(self.right_frame, state="disabled", font=("Arial", 10),
                                                           background=self.colour_list[2])
        self.incoming_messages_box.place(width=710, height=600, x=5, y=5)

        self.text_to_send_box = tk.Text(self.right_frame, font=("Arial", 9), background=self.colour_list[2])
        self.text_to_send_box.place(width=600, height=105, x=5, y=610)

        self.send_message_button = tk.Button(self.right_frame, text="Send", font=("Arial", 15),
                                             command=self.send_message)
        self.send_message_button.place(width=105, height=105, x=610, y=610)

    def send_message(self):
        """ Gets Message from text box\n
            Gives Message to ClientSender """

        message_to_send = self.text_to_send_box.get(1.0, "end-1c")
        print(message_to_send)

        self.client_sender.send_message("message", message_to_send)
        self.text_to_send_box.delete("1.0", tk.END)

    def update_incoming_message_box(self, received_from: str, message_received: str):
        """ Adds Message to Incoming Message Box when Received """

        self.incoming_messages_box.config(state="normal")
        message_to_add = received_from + ": " + message_received + "\n"
        self.incoming_messages_box.insert("end", message_to_add)
        self.incoming_messages_box.config(state="disabled")

        self.incoming_messages_box.see(tk.END)

    def update_window(self):
        self.colour_list = ClientGUICustomSettings.get_colour_scheme()
        messages = self.incoming_messages_box.get(1.0, "end-1c")

        self.format_window()
        self.root.update()

        self.incoming_messages_box.config(state="normal")
        self.incoming_messages_box.insert("end", messages)
        self.incoming_messages_box.config(state="disabled")

        if self.isMessageBuddyWinOpen:
            self.room_admin_page.update_window()
        if self.isAddBuddyWinOpen:
            self.add_buddy_page.update_window()
        if self.isRoomAdminWinOpen:
            self.room_admin_page.update_window()
        if self.isCreateRoomWinOpen:
            self.create_room_page.update_window()
        if self.isJoinRoomWinOpen:
            self.join_room_page.update_window()
        if self.isLeaveRoomWinOpen:
            self.leave_room_page.update_window()

    def run(self):
        """ Runs Tkinter MainLoop """

        self.client_gui_homepage.mainloop()

    def window_closed(self):
        """ Initiates when GUI Window Closes """

        data_to_send = {"type": "conn_shutdown"}
        data_to_send = json.dumps(data_to_send)
        self.client_socket.send(data_to_send.encode())

        if self.isMessageBuddyWinOpen:
            self.message_buddy_page.window_closed()
        if self.isAddBuddyWinOpen:
            self.add_buddy_page.window_closed()
        if self.isSettingsWinOpen:
            self.settings_page.window_closed()
        if self.isRoomAdminWinOpen:
            self.room_admin_page.window_closed()
        if self.isCreateRoomWinOpen:
            self.create_room_page.window_closed()
        if self.isJoinRoomWinOpen:
            self.join_room_page.window_closed()
        if self.isLeaveRoomWinOpen:
            self.leave_room_page.window_closed()

        self.client_gui_homepage.destroy()
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()

    @staticmethod
    def show_warning(warning_type, warning_message=""):
        """
        :param warning_type: MSG_VERIFICATION_ERR, PROFANITY_WARNING, UNDER_DEVELOPMENT
        :param warning_message: Any Message
        """
        if warning_type == "MSG_VERIFICATION_ERR":
            msgbox.showerror(title=warning_type, message=warning_message)
        elif warning_type == "PROFANITY_WARNING":
            msgbox.showwarning(title=warning_type, message=warning_message)
        elif warning_type == "UNDER_DEVELOPMENT":
            msgbox.showinfo(title=warning_type, message="THIS AREA IS UNDER DEVELOPMENT")
        elif warning_type == "ROOM DOES NOT EXIST":
            msgbox.showinfo(title=warning_type, message=warning_message)


class ClientGUIAddBuddyPage:
    def __init__(self, homepage: ClientGUIHomepage):
        self.homepage = homepage

        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.add_buddy_window = tk.Tk()
        self.add_buddy_window.geometry("500x500")
        self.add_buddy_window.resizable(False, False)
        self.add_buddy_window.title(f"YappChat - Add Buddy")
        self.add_buddy_window.protocol("WM_DELETE_WINDOW", self.window_closed)

        self.root = None

        self.format_window()

    def format_window(self):
        self.root = tk.Frame(self.add_buddy_window, background=self.colour_list[1])
        self.root.place(width=500, height=500, x=0, y=0)

    def update_window(self):
        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.format_window()
        self.root.update()

    def run(self):
        self.add_buddy_window.mainloop()

    def window_closed(self):
        """ Initiates when GUI Window Closes """
        self.close_window(self.homepage)
        self.add_buddy_window.destroy()

    @staticmethod
    def open_window(homepage: ClientGUIHomepage):
        if not homepage.isAddBuddyWinOpen:
            homepage.isAddBuddyWinOpen = True
            homepage.add_buddy_page = ClientGUIAddBuddyPage(homepage)
            homepage.add_buddy_page.run()

    @staticmethod
    def close_window(self):
        self.isAddBuddyWinOpen = False


class ClientGUIMessageBuddyPage:
    def __init__(self, homepage: ClientGUIHomepage):
        self.homepage = homepage

        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.message_buddy_window = tk.Tk()
        self.message_buddy_window.geometry("500x500")
        self.message_buddy_window.resizable(False, False)
        self.message_buddy_window.title(f"YappChat - Message Buddy")
        self.message_buddy_window.protocol("WM_DELETE_WINDOW", self.window_closed)

        self.root = None
        self.border = None
        self.send_message_button = None
        self.text_to_send_box = None
        self.buddies_list_dropdown = None
        self.incoming_messages_box = None

        self.format_window()

    def format_window(self):
        self.root = tk.Frame(self.message_buddy_window, background=self.colour_list[2])
        self.root.place(width=500, height=500, x=0, y=0)

        self.border = tk.Frame(self.root, background=self.colour_list[0])
        self.border.place(width=490, height=490, x=5, y=5)

        self.incoming_messages_box = scrlltxt.ScrolledText(self.root, state="disabled", font=("Arial", 10),
                                                           background=self.colour_list[2])
        self.incoming_messages_box.place(width=480, height=375, x=10, y=10)

        self.text_to_send_box = tk.Text(self.root, font=("Arial", 9), background=self.colour_list[1])
        self.text_to_send_box.place(width=375, height=60, x=10, y=390)

        self.buddies_list_dropdown = ttk.Combobox(self.root, state="readonly")
        self.buddies_list_dropdown.place(width=375, height=35, x=10, y=455)

        self.send_message_button = tk.Button(self.root, text="Send", font=("Arial", 15),
                                             command=lambda: ClientGUIHomepage.show_warning("UNDER_DEVELOPMENT"))
        self.send_message_button.place(width=100, height=100, x=390, y=390)

    def update_window(self):
        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.format_window()
        self.root.update()

    def run(self):
        self.message_buddy_window.mainloop()

    def window_closed(self):
        """ Initiates when GUI Window Closes """
        self.close_window(self.homepage)
        self.message_buddy_window.destroy()

    @staticmethod
    def open_window(homepage: ClientGUIHomepage):
        if not homepage.isMessageBuddyWinOpen:
            homepage.isMessageBuddyWinOpen = True
            homepage.message_buddy_page = ClientGUIMessageBuddyPage(homepage)
            homepage.message_buddy_page.run()

    @staticmethod
    def close_window(self):
        self.isMessageBuddyWinOpen = False


class ClientGUISettingsPage:
    def __init__(self, client_socket: socket.socket, homepage: ClientGUIHomepage, sender: Sender.ClientSender,
                 client_name: str):
        self.client_socket = client_socket
        self.homepage = homepage
        self.sender = sender
        self.client_id = "000000"
        self.client_name = client_name

        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.settings_window = tk.Tk()
        self.settings_window.geometry("500x500")
        self.settings_window.resizable(False, False)
        self.settings_window.title(f"YappChat - Settings")
        self.settings_window.protocol("WM_DELETE_WINDOW", self.window_closed)

        if True:
            self.root = None
            self.client_id_label = None
            self.client_id_text = None
            self.client_name_label = None
            self.client_name_text = None
            self.client_name_edit_button = None
            self.colour_scheme_label = None
            self.colour_scheme_dropdown = None
            self.colour_scheme_apply_button = None

        self.client_name_box_editable = False

        self.format_window()

    def format_window(self):
        # ROOT FRAME #
        self.root = tk.Frame(self.settings_window, bg=self.colour_list[2])
        self.root.place(width=500, height=500, x=0, y=0)

        # CLIENT ID #
        self.client_id_label = tk.Label(self.root, text=f"CLIENT ID", font=("Arial", 12),
                                        background=self.colour_list[1], relief="solid", borderwidth=1)
        self.client_id_label.place(width=175, height=50, x=10, y=10)

        self.client_id_text = tk.Entry(self.root, font=("Arial", 15), relief="solid", justify="center",
                                       disabledbackground=self.colour_list[1])
        self.client_id_text.place(width=175, height=50, x=185, y=10)
        self.client_id_text.insert(tk.END, self.client_id)
        self.client_id_text.config(state="disabled")

        # CLIENT NAME #
        self.client_name_label = tk.Label(self.root, text=f"CLIENT NAME", font=("Arial", 12),
                                          background=self.colour_list[1], relief="solid", borderwidth=1)
        self.client_name_label.place(width=175, height=50, x=10, y=62)

        self.client_name_text = tk.Entry(self.root, font=("Arial", 15), relief="solid", justify="center",
                                         disabledbackground=self.colour_list[1])
        self.client_name_text.place(width=175, height=50, x=185, y=62)
        self.client_name_text.insert(tk.END, self.client_name)
        self.client_name_text.config(state="disabled")

        self.client_name_edit_button = tk.Button(self.root, text="Edit", font=("Arial", 12), bg=self.colour_list[1],
                                                 activebackground=self.colour_list[0],
                                                 command=self.change_username_box_to_editable)
        self.client_name_edit_button.place(width=120, height=50, x=370, y=62)

        # COLOUR SCHEME CHANGE #
        self.colour_scheme_label = tk.Label(self.root, text="Change Colour Scheme", font=("Arial", 12),
                                            bg=self.colour_list[1], relief="solid", borderwidth=1)
        self.colour_scheme_label.place(width=175, height=25, x=10, y=120)

        self.colour_scheme_dropdown = ttk.Combobox(self.root, state="readonly",
                                                   values=list(ClientGUICustomSettings.colour_schemes.keys()),
                                                   background=self.colour_list[1])
        self.colour_scheme_dropdown.place(width=175, height=25, x=10, y=145)
        self.colour_scheme_dropdown.set(value=ClientGUICustomSettings.get_colour_scheme("key"))

        self.colour_scheme_apply_button = tk.Button(self.root, text="Apply", font=("Arial", 12), bg=self.colour_list[1],
                                                    activebackground=self.colour_list[0], command=self.update_window)
        self.colour_scheme_apply_button.place(width=120, height=50, x=185, y=120)

    def change_username_box_to_editable(self):
        if self.client_name_box_editable is False:
            self.client_name_text.config(state="normal")
            self.client_name_edit_button.config(text="Apply")
        else:
            self.client_name_text.config(state="disabled")
            self.client_name_edit_button.config(text="Edit")
            self.change_name()

        self.client_name_box_editable = not self.client_name_box_editable

    def change_name(self, name=None):
        if name is None:
            new_name = self.client_name_text.get()
            self.client_name = new_name
            self.sender.send_message("name_change_request", new_name)
            self.homepage.client_gui_homepage.title(f"YappChat - {new_name}")
        else:
            self.client_name = name
            self.homepage.client_gui_homepage.title(f"YappChat - {name}")

    def update_window(self):
        new_colour_scheme = self.colour_scheme_dropdown.get()
        ClientGUICustomSettings.set_colour_scheme(new_colour_scheme)
        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.format_window()
        self.root.update()

        self.homepage.update_window()

    def run(self):
        self.settings_window.mainloop()

    def window_closed(self):
        """ Initiates when GUI Window Closes """
        self.close_window(self.homepage)
        self.settings_window.destroy()

    @staticmethod
    def open_window(homepage: ClientGUIHomepage, client_socket: socket, sender: ClientSender.ClientSender, client_name: str):
        if not homepage.isSettingsWinOpen:
            homepage.isSettingsWinOpen = True
            homepage.settings_page = ClientGUISettingsPage(client_socket, homepage, sender, client_name)
            homepage.settings_page.run()

    @staticmethod
    def close_window(homepage: ClientGUIHomepage):
        homepage.isSettingsWinOpen = False


class ClientGUIRoomAdminPage:
    def __init__(self, homepage: ClientGUIHomepage):
        self.homepage = homepage

        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.room_admin_window = tk.Tk()
        self.room_admin_window.geometry("500x500")
        self.room_admin_window.resizable(False, False)
        self.room_admin_window.title(f"YappChat - Room Admin")
        self.room_admin_window.protocol("WM_DELETE_WINDOW", self.window_closed)

        self.root = None
        self.format_window()

    def format_window(self):
        self.root = tk.Frame(self.room_admin_window, background=self.colour_list[2])
        self.root.place(width=500, height=500, x=0, y=0)

    def update_window(self):
        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.format_window()
        self.root.update()

    def run(self):
        self.room_admin_window.mainloop()

    def window_closed(self):
        """ Initiates when GUI Window Closes """
        self.close_window(self.homepage)
        self.room_admin_window.destroy()

    @staticmethod
    def open_window(homepage: ClientGUIHomepage):
        if not homepage.isRoomAdminWinOpen:
            homepage.isRoomAdminWinOpen = True
            homepage.room_admin_page = ClientGUIRoomAdminPage(homepage)
            homepage.room_admin_page.run()

    @staticmethod
    def close_window(homepage: ClientGUIHomepage):
        homepage.isRoomAdminWinOpen = False


class ClientGUICreateRoomPage:
    def __init__(self, homepage, client_sender: Sender.ClientSender):
        self.homepage = homepage
        self.client_sender = client_sender

        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.create_room_window = tk.Tk()
        self.create_room_window.geometry("500x500")
        self.create_room_window.resizable(False, False)
        self.create_room_window.title(f"YappChat - Create Room")
        self.create_room_window.protocol("WM_DELETE_WINDOW", self.window_closed)

        self.root = None
        self.create_room_button = None

        self.format_window()

    def format_window(self):
        self.root = tk.Frame(self.create_room_window, background=self.colour_list[2])
        self.root.place(width=500, height=500, x=0, y=0)

        self.create_room_button = tk.Button(self.root, text="Create", command=self.create_room)
        self.create_room_button.place(width=100, height=100, x=10, y=10)

    def create_room(self):
        self.client_sender.send_message("new_room")

    def update_window(self):
        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.format_window()
        self.root.update()

    def run(self):
        self.create_room_window.mainloop()

    def window_closed(self):
        """ Initiates when GUI Window Closes """
        self.close_window(self.homepage)
        self.create_room_window.destroy()

    @staticmethod
    def open_window(homepage: ClientGUIHomepage, client_sender: ClientSender.ClientSender):
        if not homepage.isCreateRoomWinOpen:
            homepage.isCreateRoomWinOpen = True
            homepage.create_room_page = ClientGUICreateRoomPage(homepage, client_sender)
            homepage.create_room_page.run()

    @staticmethod
    def close_window(homepage: ClientGUIHomepage):
        homepage.isCreateRoomWinOpen = False


class ClientGUIJoinRoomPage:
    def __init__(self, homepage: ClientGUIHomepage, client_sender: Sender.ClientSender):
        self.homepage = homepage
        self.client_sender = client_sender

        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.join_room_window = tk.Tk()
        self.join_room_window.geometry("500x500")
        self.join_room_window.resizable(False, False)
        self.join_room_window.title(f"YappChat - Join Room")
        self.join_room_window.protocol("WM_DELETE_WINDOW", self.window_closed)

        self.root = None
        self.room_entry = None
        self.join_room_button = None

        self.format_window()

    def format_window(self):
        self.root = tk.Frame(self.join_room_window, background=self.colour_list[2])
        self.root.place(width=500, height=500, x=0, y=0)

        self.room_entry = tk.Entry(self.root, font=("Arial", 15), relief="solid", justify="center")
        self.room_entry.place(width=350, height=50, x=10, y=10)

        self.join_room_button = tk.Button(self.root, text="Create", command=self.join_room)
        self.join_room_button.place(width=100, height=100, x=400, y=400)

    def join_room(self):
        room_id = self.room_entry.get()
        self.client_sender.send_message("join_room", room_id)

    def update_window(self):
        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.format_window()
        self.root.update()

    def run(self):
        self.join_room_window.mainloop()

    def window_closed(self):
        """ Initiates when GUI Window Closes """
        self.close_window(self.homepage)
        self.join_room_window.destroy()

    @staticmethod
    def open_window(homepage: ClientGUIHomepage, client_sender: Sender.ClientSender):
        if not homepage.isJoinRoomWinOpen:
            homepage.isJoinRoomWinOpen = True
            homepage.join_room_page = ClientGUIJoinRoomPage(homepage, client_sender)
            homepage.join_room_page.run()

    @staticmethod
    def close_window(homepage: ClientGUIHomepage):
        homepage.isJoinRoomWinOpen = False


class ClientGUILeaveRoomPage:
    def __init__(self, homepage: ClientGUIHomepage):
        self.homepage = homepage

        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.leave_room_window = tk.Tk()
        self.leave_room_window.geometry("500x500")
        self.leave_room_window.resizable(False, False)
        self.leave_room_window.title(f"YappChat - Leave Room")
        self.leave_room_window.protocol("WM_DELETE_WINDOW", self.window_closed)

        self.root = None
        self.format_window()

    def format_window(self):
        self.root = tk.Frame(self.leave_room_window, background=self.colour_list[2])
        self.root.place(width=500, height=500, x=0, y=0)

    def update_window(self):
        self.colour_list = ClientGUICustomSettings.get_colour_scheme()

        self.format_window()
        self.root.update()

    def run(self):
        self.leave_room_window.mainloop()

    def window_closed(self):
        """ Initiates when GUI Window Closes """
        self.close_window(self.homepage)
        self.leave_room_window.destroy()

    @staticmethod
    def open_window(homepage: ClientGUIHomepage):
        if not homepage.isLeaveRoomWinOpen:
            homepage.isLeaveRoomWinOpen = True
            homepage.leave_room_page = ClientGUILeaveRoomPage(homepage)
            homepage.leave_room_page.run()

    @staticmethod
    def close_window(homepage: ClientGUIHomepage):
        homepage.isLeaveRoomWinOpen = False
