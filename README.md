# Clash-Verge-RCE-POC

**郑重声明：文中所涉及的技术、思路和工具仅供以安全为目的的学习交流使用，任何人不得将其用于非法用途和盈利等目的，否则后果自负。**

## Clash Verge rev 本地提权/远程命令执行漏洞 POC

![图片](https://github.com/user-attachments/assets/87300d09-5848-46ed-8e64-7d9037dca454)

# Usage steps

![图片](https://github.com/user-attachments/assets/e2a5ca4f-c78c-4cb9-88ef-0f2b52c2c8ef)

```
usage: poc.py [-h] -c COMMAND -p PORT --host HOST [--proxy PROXY_IP]

Clash Verge RCE POC

optional arguments:

  -h, --help            show this help message and exit
  
  -c COMMAND, --command COMMAND  Executed commands
          
  -p PORT, --port PORT  Set local listening port
  
  --host HOST           Set local IP address
  
  --proxy PROXY_IP      Optional SOCKS5 proxy IP, default port 7897
```
  
# Example usage

## Remote Command Execution

<img width="1919" alt="25fca5d41abf5ccd604f38f422ccf94" src="https://github.com/user-attachments/assets/bc74d7c9-e152-448b-a0b7-603305af693a" />

## Local empowerment

![13390476346200152](https://github.com/user-attachments/assets/05bd6179-9d04-4371-ab84-94d98e12f343)
