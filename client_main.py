import Client
import argparse


def client_main(client_name: str):
    client = Client.Client(client_name)
    client.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True)
    args = parser.parse_args()

    client_main(args.name)
