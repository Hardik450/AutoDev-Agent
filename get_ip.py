import socket

def get_ip_address():
    """
    Fetches the local machine's IP address by attempting to connect to an external host.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't actually send data, just establishes a connection locally
        # to determine the outgoing interface IP.
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1' # Fallback to localhost if no network connection
    finally:
        s.close()
    return IP

if __name__ == '__main__':
    ip_address = get_ip_address()
    file_name = 'ip_address.txt'
    with open(file_name, 'w') as f:
        f.write(ip_address)
    print(f"IP address '{ip_address}' saved to '{file_name}'")