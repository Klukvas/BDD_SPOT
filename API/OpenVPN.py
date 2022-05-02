import os
import subprocess
import time
import platform
import settings


class OpenVPN:
    def __init__(self):
        self.system = platform.system()
        if settings.openvpn_path == 'NOT_SET' or settings.openvpn_profile_name == 'NOT_SET':
            raise Exception('openvpn_path or openvpn_profile_name is not set at environment variables')
        if self.system == 'Windows':
            self.create_batch_files()
        else:
            raise Exception('Your OS is not supported')

    def create_batch_files(self):
        self.create_connection_batch()
        self.create_disconection_batch()

    def create_connection_batch(self):
        with open('../openvpn/connect.bat', 'r') as f:
            connection_string = f.read()
            first_quote = connection_string.find('"')
            second_quote = connection_string.find('"', first_quote + 1)
            connection_string = connection_string[first_quote] + settings.openvpn_path + connection_string[second_quote:]

            start = connection_string.find('connect ') + len('connect ')
            connection_string = connection_string[:start] + settings.openvpn_profile_name
        with open('../openvpn/connect.bat', 'w') as f:
            f.write(connection_string)

    def create_disconection_batch(self):
        with open('../openvpn/disconnect.bat', 'r') as f:
            connection_string = f.read()
            first_quote = connection_string.find('"')
            second_quote = connection_string.find('"', first_quote + 1)
            connection_string = connection_string[first_quote] + settings.openvpn_path + connection_string[second_quote:]

            start = connection_string.find('disconnect ') + len('disconnect ')
            connection_string = connection_string[:start] + settings.openvpn_profile_name

        with open('../openvpn/disconnect.bat', 'w') as f:
            f.write(connection_string)

    def connect(self):
        if self.system == 'Windows':
            script_path = os.path.join(settings.working_directory, 'openvpn', 'connect.bat')
            subprocess.call([script_path])
            time.sleep(20)  # waiting for openvpn connect
            print("OpenVPN connection is opened")

    def disconnect(self):
        if self.system == 'Windows':
            script_path = os.path.join(settings.working_directory, 'openvpn', 'disconnect.bat')
            subprocess.call([script_path])
            print("OpenVPN connection is closed")

if __name__ == '__main__':
    openvpn_client = OpenVPN()
    openvpn_client.connect()
    openvpn_client.disconnect()
