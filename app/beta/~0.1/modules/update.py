import requests
import time
from colorama import Fore

##! buraya sonra devam et


THİSVERSİONHASH = '100100101101010111011011010101010'

# VERSİON CONTROL


try:
    url = "https://raw.githubusercontent.com/berhatpasha/OBC/main/OBC/versionControl/version"
    response = requests.get(url)
    response.raise_for_status()
    content = response.text.strip()

    print(f"{Fore.CYAN}Last version : {content}")
    print(f"{Fore.CYAN}Used version : {versionHash}")
    if versionHash == content:
        print(f"{Fore.GREEN}OBC in its most current version ✓")
        time.sleep(3)
    else:
        print("\n"*2)
        print(f"{Fore.YELLOW}Update available ! ")
        print(f"{Fore.YELLOW}Use : git clone https://github.com/berhatpasha/OBC.git")
        update = True
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

if update:
    print(f"{Fore.YELLOW} It will resume in 20 seconds.")
    time.sleep(20)
else:
    time.sleep(5)