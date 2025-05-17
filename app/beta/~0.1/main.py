import time
import os
import threading
import colorama
from colorama import Fore
colorama.init(autoreset=True)

start_time = time.time()
print(f"{Fore.CYAN}Debugger başlangıç saati {start_time} olarak ayarlandı")

def timer():
    global start_time
    global second
    while True:
        second = int(time.time() - start_time)


def console():
    os.system('clear') 
    print(f"{second}: {Fore.CYAN} Eğer bu ekranı görüyorsanız, muhtemelen yanlış derlenmiş bir versiyonu kullanıyorsunuz")
    print(f"{second}: {Fore.CYAN} Kendiniz kurulum yapmadıysanız, https://textify.dev adresinden bilgisayarınıza uygun kurulum dosyasından kurulum yapın")
    print(f"{second}: {Fore.GREEN} Hatalar burada görülür, bir hata gözükmüyor.")
    
    time.sleep(5)
    
    while True:
        print(f"{second}: {Fore.LIGHTGREEN_EX} Arkaplan işlevleri çalışmaya devam ediyor")
        time.sleep(1)
    
    
def main():
    pass

timerThread = threading.Thread(target=timer)
timerThread.start()

consoleThread = threading.Thread(target=console)
consoleThread.start()

mainThread = threading.Thread(target=main)
mainThread.start()