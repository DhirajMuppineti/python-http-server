import socket
import threading
import os

OK_RESP = b"HTTP/1.1 200 OK\r\n\r\n"
NOT_FOUND_RESP = b"HTTP/1.1 404 Not Found\r\n\r\n"
METHOD_NOT_ALLOWED = b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"
CREATED = b"HTTP/1.1 201 Created\r\n\r\n"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "tmp/data")

def handle_client(connection):
    try:
        data = connection.recv(1024).decode("utf-8").split("\r\n")
        if not data:
            return

        header = data[0]
        headers = header.split()
        url = headers[1]
        url_params = url.split("/")
        print(data)
        print(url.split("/"))
        print(headers)

        if headers[0] == "GET":
            if url == "/":
                response = OK_RESP
            elif len(url_params) > 1 and url_params[1] == "echo":
                body = url_params[2]
                # status line
                response = "HTTP/1.1 200 OK"
                response += "\r\n"
                # headers
                response += "Content-Type: text/plain" + "\r\n"
                response += "Content-Length: " + str(len(body)) + "\r\n"
                response += "\r\n"
                # body
                response += body
                response = response.encode()
            elif len(url_params) == 2 and url_params[1] == "user-agent":
                for d in data:
                    if d.find("User-Agent") != -1:
                        user_agent = d
                        break
                # print(user_agent)
                body = user_agent[12:]
                print(body)
                # status line
                response = "HTTP/1.1 200 OK"
                response += "\r\n"
                # headers
                response += "Content-Type: text/plain" + "\r\n"
                response += "Content-Length: " + str(len(body)) + "\r\n"
                response += "\r\n"
                # body
                response += body
                response = response.encode()
            elif len(url_params) == 3 and url_params[1] == "files":
                try:
                    file_path = os.path.join(DATA_DIR, url_params[2])
                    with open(file_path, "r") as file:
                        data = file.read()
                    # status line
                    response = "HTTP/1.1 200 OK"
                    response += "\r\n"
                    # headers
                    response += "Content-Type: application/octet-stream" + "\r\n"
                    response += "Content-Length: " + str(len(data)) + "\r\n"
                    response += "\r\n"
                    # body
                    response += data
                    response = response.encode()

                except OSError:
                    response = NOT_FOUND_RESP
            else:
                response = NOT_FOUND_RESP

        elif headers[0] == "POST":
            if len(url_params) == 3 and url_params[1] == "files":
                file_path = os.path.join(DATA_DIR, url_params[2])
                with open(file_path, "w") as file:
                    file.write(data[-1])
                response = CREATED
            else:
                response = NOT_FOUND_RESP

        connection.send(response)
    finally:
        connection.close()


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        connection, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection,))
        client_thread.start()


if __name__ == "__main__":
    main()
