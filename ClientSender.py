import socket
import json


class ClientSender:

    def __init__(self, client_socket: socket):
        self.client_socket = client_socket

    def send_message(self, data_type, data1="", data2=""):
        """
        Preps Message into json file\n
        Sends Messaged through socket
        :param data_type: {1} message, {2} name_change_request, {3} new_room, {4} join_room, {5} leave_room
        :param data1: {1} msg, {2} name, {4} room_id
        :param data2:
        """
        data_to_send = {}

        if data_type == "message":
            data_to_send = {"type": data_type, "msg": data1}
        elif data_type == "name_change_request":
            data_to_send = {"type": data_type, "name": data1}
        elif data_type == "new_room":
            data_to_send = {"type": data_type}
        elif data_type == "join_room":
            data_to_send = {"type": data_type, "room_id": data1}
        elif data_type == "leave_room":
            data_to_send = {"type": data_type}

        json_obj = json.dumps(data_to_send)
        self.client_socket.send(json_obj.encode())  # send message
