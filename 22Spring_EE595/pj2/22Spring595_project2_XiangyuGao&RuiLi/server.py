# server
import socketserver
import socket
import json
import time
import face_recognize
import picture_receive_server


# Server User Information Database
user_db = {'user1': '123456', 'user2': '112233', 'user3': '123123', '1': '1'}

print('Waiting For Client To Connect......')


# Define the TargetServer class to allow concurrent connections of tcp
class TargetServer(socketserver.BaseRequestHandler):
    # Define the handle method of the parent class
    def handle(self):
        # Implement custom logic
        print('Client with IP {} is connected, port is {}'.format(self.client_address[0], self.client_address[1]))
        server_info = ('''Face Verification Succeeded!
                                     
                           --------  Welcome to 595 Serving System  --------
                       ''')

        # send the above message
        self.request.send(server_info.encode())

        while True:

            # Receive username and password and print
            client_res = self.Server_Recv()
            self.Client_Info(client_res)

            # Execute the verification procedure and send the login result to the client
            # Face Verification
            if self.Login(client_res) == 'pass':
                self.request.send('pass'.encode())

                print(time.ctime())
                with open(r'C:/UW/22 Spring/595/pj2/login_log.txt', mode='a+', encoding='utf-8') as fp:
                    fp.write('Login IP:' + self.client_address[0] + ' login port：' + str(self.client_address[1]) +
                             ' Login time：' + time.ctime() + ' username：' + client_res['username'][::-1] + '\n')

                    # After the verification is passed, socket communication with the server can be performed.
                self.Talk()
                break

                # Returns 404 if the user matches the firewall policy
            elif self.Login(client_res) == '404':
                self.request.send('404'.encode())
                print('Client IP or login username is firewall blacklist！')

                # Disconnect if username or password is wrong
            else:
                self.request.send('fall'.encode())
                print('Account password mismatch, disconnected！')

        print('Waiting For New Host to Connect......')


    # The function that the server receives the username and password
    def Server_Recv(self):
        user_info = self.request.recv(1460)
        str_user_info = user_info.decode()
        return json.loads(str_user_info)


    # The function to print the username and password in the server
    def Client_Info(self, client_res):
        print('Client Login Successfully：')
        # 解密过程
        # decryption process
        print('username' + ':' + client_res['username'][-1::-1])
        print('password' + ':' + client_res['password'][:-4])


    # Login verification function
    def Login(self, client_res, face_ver=False):

        # Authenticate against encrypted data
        deny_user = {'IP': '127.0.0.1', 'user': 'user1'}

        # If the ACL is satisfied, an error code is returned, and the login is denied!
        if (self.client_address[0] == deny_user['IP']) and (client_res['username'][::-1] == deny_user['user']):
            return '404'
        for j in user_db:
            if (j[-1::-1] == client_res['username']) and (user_db[j] + '1014' == client_res['password']):
                return 'pass'


    # Client and server communication functions
    def Talk(self):
        while True:

            # Receive messages from clients
            clinet_message = self.request.recv(1460)
            # print(clinet_message)
            if clinet_message == b'end_talk'[::-1]:
                print('Disconnected From Client')
                return
            if len(clinet_message) == 0:
                print('Client Has Been Disconnected！')
                return

            if "password" in clinet_message.decode()[-1::-1]:
                print('Successfully Captured and Sniffed the Keyword: password!')

            # Reverse print messages sent by the client
            print(clinet_message.decode()[-1::-1])


            # Reverse the entered information and send it
            server_message = input('----->')[-1::-1]
            self.request.send(server_message.encode())

            if server_message == b'end_talk':
                print('Disconnected From Client!！')
                return


def face_test():
    while True:
        picture_receive_server.socket_service_image()
        if face_recognize.face_verification() is True:
            break
        else:

            print('Please Try Again!')


def main():
    # Instantiate the socketserver object server_socket
    face_test()
    server_socket = socketserver.ThreadingTCPServer(('127.0.0.1', 10310), TargetServer)
    # loop call
    server_socket.serve_forever()


if __name__ == '__main__':

    main()
