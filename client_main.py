import Client
import argparse


def client_main(client_name: str):
    client = Client.Client(client_name)
    client.run()


if __name__ == '__main__':
    client_main("user")
