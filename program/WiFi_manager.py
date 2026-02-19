import os
import sys
os.chdir("../driver")
sys.path.insert(0, "../driver")
from WiFi import WiFiDriver
from running import run
WiFi = WiFiDriver(debug=False)
print(f"""{"=" * 77}=                                команды                                    =
{"=" * 77}
= join-подключится к сети                                                   =
= view-просмотр сетей                                                       =
= edit-редактирование сети                                                  =
= dist-раздача сети                                                         =
{"=" * 77}""")
act = input("действие: ")
if act == "join":
    name = input("название сети: ")
    password = input("пароль (если нет просто оставьте строку пустой): ")
    if not password:
        WiFi.join(name)
    else:
        WiFi.join(name, password)     
elif act == "view":
    WiFi.view()
elif act == "edit":
    oldname = input("старое имя: ")
    newname = input("новое имя: ")
    oldpassword = input("старый пароль (пустота для пропуска): ")
    newpassword = input("новый пароль (пустота для пропуска): ")
    if newpassword:
        WiFi.edit(oldname, newname, newpassword, oldpassword)
    elif not newpassword and not oldpassword:
        newpassword = None
        oldpassword = None
        WiFi.edit(oldname, newname, newpassword, oldpassword)
elif act == "dist":        
    ssid = input("ssid: ")
    password = input("password: ")
    WiFi.dist(ssid, password)
elif act == "exit":
    os.chdir("../system")
    sys.path.insert(0, "../system")
    run("NextOS.py")
else:
    print("неизвестная команда")