A lightweight Python script designed to brute-force username and password combinations for an OpenVPN .ovpn configuration file.
Ideal for testing login credentials in controlled environments.

🚀 Features
Brute-forces combinations from user-provided username and password lists

Supports stopping after the first successful login or continuing (--cont)

Clean and informative terminal output

Simple CLI interface with help and usage examples

📌 Usage

```sudo python3 brute.py -u users.txt -p passwords.txt -c config.ovpn```

To continue brute-forcing after a valid login is found:

```sudo python3 brute.py -u users.txt -p passwords.txt -c config.ovpn --cont```

![image](https://github.com/user-attachments/assets/6a8888d9-860d-4508-a596-9af1561a11b9)



⚠️ Disclaimer
This script is intended for educational purposes and authorized testing only.
Do not use it on networks or systems without explicit permission.
