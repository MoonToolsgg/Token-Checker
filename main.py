import os, datetime
from colorama import Fore, init
from pystyle import Center, Colorate, Colors
from tls_client import Session
if os.name == "nt":
    import ctypes

init()
timestamp = datetime.datetime.now().strftime('%H:%M:%S')

session = Session(client_identifier="chrome_122")
def load_tokens():
    with open("tokens.txt", "r", encoding='utf-8') as f:
        return f.read().splitlines()
    
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def title(title):
    if os.name == "nt":    
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        pass
    
def time():
    date = datetime.now()
    timestamp = "{:02d}:{:02d}:{:02d}".format(date.hour, date.minute, date.second)
    return timestamp


banner = """
 _____     _                _____  _               _             
|_   _|   | |              /  __ \| |             | |            
  | | ___ | | _____ _ __   | /  \/| |__   ___  ___| | _____ _ __ 
  | |/ _ \| |/ / _ \ '_ \  | |   || '_ \ / _ \/ __| |/ / _ \ '__|
  | | (_) |   <  __/ | | | | \__/\| | | |  __/ (__|   <  __/ |   
  \_/\___/|_|\_\___|_| |_|  \____/|_| |_|\___|\___|_|\_\___|_|"""


def main():
    while True:
        clear()
        title("Token Checker • dsc.gg/nyxtools")
        print(Colorate.Vertical(Colors.red_to_purple, Center.XCenter(banner)))
        print(Colorate.Horizontal(Colors.red_to_purple, Center.XCenter("\n[01] check\n[02] quit")))
        choice = input(Colorate.Diagonal(Colors.red_to_purple, "choice: "))
        
        if choice == "1" or choice == "01":
            tokens = load_tokens()
            for token in tokens:
                try:
                    headers = {"authorization": token}
                    r = session.get("https://discord.com/api/v9/users/@me", headers=headers)
                    
                    if r.status_code == 200:
                        data = r.json()
                        id = data['id']
                        username = data['username']
                        global_name = data['global_name']
                        email = data.get('email', 'N/A')
                        Nitrotype = data.get('premium_type', 0) != 0
                        twofa = data.get('mfa_enabled', False)
                        bio = data.get('bio', 'N/A').replace("\n", " ")
                        avatar_url = f"https://cdn.discordapp.com/avatars/{id}/{data['avatar']}.png"
                        
                        print(Fore.LIGHTMAGENTA_EX + f"[ {Fore.RED}{timestamp}{Fore.LIGHTMAGENTA_EX} ] " + Fore.GREEN + f"Valid {Fore.LIGHTMAGENTA_EX}| " + Fore.LIGHTBLUE_EX + f"{token[:45]}******")
                        
                        with open("output/valid.txt", "a+", encoding='utf-8') as f:
                            f.write(f"{token} | username: {username} | global name: {global_name} | bio: {bio} | email: {email} | nitro: {Nitrotype} | 2fa: {twofa} | avatar_url: {avatar_url}\n")
                    
                    elif r.status_code == 401 or "Unauthorized" in r.text:
                        print(Fore.RED + f"[ {Fore.RED}{timestamp}{Fore.LIGHTMAGENTA_EX} ] " + Fore.LIGHTYELLOW_EX + f"Invalid {Fore.LIGHTMAGENTA_EX}| " + Fore.LIGHTBLACK_EX + f"{token[:45]}******")
                        with open("output/invalid.txt", "a+", encoding='utf-8') as f:
                            f.write(f"{token}\n")
                
                except Exception as e:
                    print(Fore.RED + f"[ {Fore.RED}{timestamp}{Fore.LIGHTMAGENTA_EX} ] " + Fore.LIGHTMAGENTA_EX + "Error: " + Fore.LIGHTBLACK_EX + str(e))
        
        elif choice == "2" or choice == "02":
            quit()
if __name__ == "__main__":
    main()