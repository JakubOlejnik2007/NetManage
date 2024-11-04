class COM_CONNECTION:
    def __init__(self, data: dict):
        self.METHOD = "COM"
        self.PORT = data["PORT"]
        self.BAUDRATE = data["BAUDRATE"]
        self.DEVICE = data["DEVICE"]+"_serial"
        self.EXECPASS = data["EXECPASS"] if data.get("EXECPASS") else ""


class SSHTEL_CONNECTION:
    def __init__(self, data: dict):
        self.METHOD = "COM"
        self.PORT = data["PORT"]
        self.BAUDRATE = data["BAUDRATE"]
        self.DEVICE = data["DEVICE"] + "_serial"
        self.EXECPASS = data["EXECPASS"] if data.get("EXECPASS") else ""


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
            return SSHTEL_CONNECTION(conn_data)
        elif conn_data.get("METHOD") == "TFTP":
            return TFTP_CONNECTION()
        else:
            raise AttributeError("Unknown or unhandled connection type.")

if __name__ == '__main__':
    read_nmconn("switch.nmconn")