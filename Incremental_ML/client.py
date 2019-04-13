import socket
from network_setup import *
from sys import argv, exit


# Will send (x, y) to cluster
def main():
    if len(argv) != 2:
        print("Usage: python3 client.py <IP Address> <Port Number>")
        exit(0)

    # Test Values for connection
    if valid_ip(argv[0]):
        ip = argv[0]
    else:
        print("Invalid IP Address!")
        exit(0)

    if valid_port(argv[1]):
        port = int(argv[1])
    else:
        print("Invalid Port Number!")
        exit(0)

    # Keep sending (x, y) coordinates...
    while True:
        try:
            var = input("ML> ")

            if var == "exit":
                break
            else:
                # connect to the server on local computer
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((ip, port))

                client_socket.send(var.encode())
                y_hat = client_socket.recv(1024).decode()
                print(y_hat)

        except EOFError:
            print("EOF detected, exiting!")
            break

        except socket.timeout:
            print("Timeout Exception!")
            continue

        except KeyboardInterrupt:
            print('CTRL-C received, exiting!')
            break


if __name__ == "__main__":
    main()
