# client
import socket
import json
import picture_send_clinet


def main():
    print('Face Recognizing...')
    # instantiate the socket object
    client_socket = socket.socket()
    # establish a connection with the server
    while True:
        try:
            client_socket.connect(('127.0.0.1', 10310))
            break
        except ConnectionRefusedError:
            continue

    # Client login function
    def SingIn():
        username = input('please enter user name：').strip()
        password = input('Please enter password：').strip()
        # Form a dictionary of username and password and send it to the server
        user_dict = {'username': username, 'password': password}
        # Reverse the username entered by the client, add 1014 to the password, and then send
        user_dict['username'] = username[-1::-1]
        user_dict['password'] = password + '1014'
        # Serialize the user information dictionary to a string before sending
        str_user_dict = json.dumps(user_dict)
        client_socket.send(str_user_dict.encode())

    # Client and server communication functions
    def Talk():
        while True:

            # Reverse the entered information and send it
            client_message = input('----->')[-1::-1]
            client_socket.send(client_message.encode())
            if client_message == 'end_talk'[::-1]:
                client_socket.close()
                print('Disconnected from server！')
                return

            server_message = client_socket.recv(1460)
            if server_message == b'end_talk'[::-1]:
                client_socket.close()
                print('Disconnected from server！!!')
                return

            # Reverse the message sent by the print server
            print(server_message.decode()[-1::-1])


    # First print the information sent by the client
    print(client_socket.recv(1460).decode())
    # while True:
    #     try:
    #         print(client_socket.recv(1460).decode())
    #         break
    #     except:
    #         continue

    while True:

        # Execute the login function
        SingIn()

        # View logged in results
        res = client_socket.recv(1460).decode()

        if res == 'pass':
            print('Landed successfully！')
            Talk()
            break

        elif res == '404':
            print('The server refused your connection！')
            print('Please re-select an account or IP to log in！')
            continue


        else:
            print('Incorrect username or password! please enter again!')

    client_socket.close()


if __name__ == '__main__':
    picture_send_clinet.sock_client_image()
    main()
