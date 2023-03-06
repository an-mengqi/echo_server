import http
import re
import socket
import datetime


# Create a TCP server socket
http_response = (
        f"HTTP/1.0 200 OK\r\n"
        f"Server: otusdemo\r\n"
        f"Date: Sat, 01 Oct 2022 09:39:37 GMT\r\n"
        f"Content-Type: text/html; charset=UTF-8\r\n"
        f"\r\n"
        )

end_of_stream = '\r\n\r\n'


def handle_client(connection, address):
    client_data = ''
    with connection:
        while True:
            data = connection.recv(1024)
            print("Received:", data)
            if not data:
               break
            client_data += data.decode()
            if end_of_stream in client_data:
                break

        method = re.search(r"(POST|GET|PUT|DELETE|HEAD|CONNECT|OPTIONS|TRACE)", client_data).group(1)
        try:
            status = re.search(r"([/][?]status=)(\d{1,3} )", client_data).group(2)
        except:
            status = 200
        status_code = http.HTTPStatus(int(status))
        status_phrase = status_code.phrase
        method_text = "Request Method: " + method
        address_text = "Request Source: " + str(address)
        status_text = "Response Status: " + str(status) + " " + status_phrase

        result_response = http_response + "\n" + method_text + "\n" + address_text + "\n" + status_text + "\n"
        splitted_list = client_data.split('\r\n')
        for x in splitted_list[1:]:
            result_response += x + "\n"

        print(result_response)

        # Send current server time to the client
        serverTimeNow = "%s"%datetime.datetime.now()
        connection.send(result_response.encode() + serverTimeNow.encode() + f"\r\n".encode())


with socket.socket() as serverSocket:
    # Bind the tcp socket to an IP and port
    serverSocket.bind(("127.0.0.1", 40404))
    # Keep listening
    serverSocket.listen()

    while(True): # Keep accepting connections from clients
        (clientConnection, clientAddress) = serverSocket.accept()
        handle_client(clientConnection, clientAddress)
        print(f"Sent data to {clientAddress}")
