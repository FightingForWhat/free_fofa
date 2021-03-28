import config_auto

def logo():
    print(r'''
  _____                            _____       _____        
_/ ____\______   ____   ____     _/ ____\_____/ ____\____   
\   __\\_  __ \_/ __ \_/ __ \    \   __\/  _ \   __\\__  \  
 |  |   |  | \/\  ___/\  ___/     |  | (  <_> )  |   / __ \_
 |__|   |__|    \___  >\___  >____|__|  \____/|__|  (____  /
                    \/     \/_____/                      \/ 
    ''')

def checkSession():
    if config_auto.COOKIE=="":
        print("请配置config文件")
        exit(0)
    print("[*] 检测cookie成功\n")
    return

def init():
    config_auto.TimeSleep = 5
    return
