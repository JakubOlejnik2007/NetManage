class COM_CONNECTION:
    def __init__(self, data: dict):
        self.METHOD = "COM"
        self.PORT = data["PORT"]
        self.BAUDRATE = data["BAUDRATE"]
        self.DEVICE = data["DEVICE"]+"_serial"
        self.EXECPASS = data["EXECPASS"] if data.get("EXECPASS") else ""

    def __str__(self):
        print(self.METHOD, self.PORT, self.BAUDRATE, self.DEVICE, self.EXECPASS)

    def getNetmikoConnDict(self):
        return {
            'device_type': self.DEVICE,
            'serial_settings': {
                'port': self.PORT,
                'baudrate': self.BAUDRATE,
            },
            'username': '',
            'password': '',
            'secret': self.EXECPASS,
        }

class SSHTEL_CONNECTION:
    def __init__(self, data: dict):
        self.METHOD = data["METHOD"]
        self.HOST = data["HOST"]
        self.PORT = data["PORT"]
        self.USERNAME = data["USERNAME"]
        self.PASSWORD = data["PASSWORD"]
        self.DEVICE = data["DEVICE"] + ("" if self.METHOD == "SSH" else "_telnet")
        self.EXECPASS = data["EXECPASS"] if data.get("EXECPASS") else ""

    def __str__(self):
        print(self.METHOD, self.HOST, self.PORT, self.USERNAME, self.PASSWORD, self.EXECPASS)

    def getNetmikoConnDict(self):
        return {
            'device_type': self.DEVICE,
            'host': self.HOST,
            'port': self.PORT,
            'username': self.USERNAME,
            'password': self.PASSWORD,
            'secret': self.EXECPASS,
        }

class TFTP_CONNECTION:
    pass

def read_nmconn(file: str) -> COM_CONNECTION | SSHTEL_CONNECTION | TFTP_CONNECTION:
    with open(file, 'r') as f:
        lines = f.readlines()
        conn_data = {}
        for idx, line in enumerate(lines):
            line = line.strip()
            if len(line) > 0 and line[0:2] != '--':
                key, value = line.split(': ')
                print(key, value)
                conn_data[key] = value
        print(conn_data)

        if conn_data.get("DEVICE") is None:
            raise ValueError("DEVICE is not defined")

        if conn_data.get("METHOD") == "COM":
            if conn_data.get("PORT") is None or conn_data.get("BAUDRATE") is None:
                raise AttributeError("Expected more data.")
            return COM_CONNECTION(conn_data)
        elif conn_data.get("METHOD") == "SSH" or conn_data.get("METHOD") == "TELNET":
            if conn_data.get("HOST") is None or conn_data.get("PORT") is None or conn_data.get("USERNAME") is None or conn_data.get("PASSWORD") is None:
                raise AttributeError("Expected more data.")
            return SSHTEL_CONNECTION(conn_data)
        elif conn_data.get("METHOD") == "TFTP":
            return TFTP_CONNECTION()
        else:
            raise AttributeError("Unknown or unhandled connection type.")

if __name__ == '__main__':
    read_nmconn("switch_com.nmconn")