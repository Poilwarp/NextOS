import os
import sys
os.chdir("../driver")
sys.path.insert(0, "../driver")
from running import run

os.chdir("../file system/file(text)")
sys.path.insert(0, "../file system/file(text)")

print(f"""{"=" * 77}
={" " * 34} команды {" " * 32}=
{"=" * 77}
= write-создание файла                                                      =
= read-чтение файла                                                         =
= add-добавление в файл                                                     =
= del-удаление файла                                                        =
{"=" * 77}""")
operation = None

if operation == "exit":   
    os.chdir("../system")
    sys.path.insert(0, "../system")
    run("NextOS.py")

def write_file():
    filename = input("имя файла: ")
    ext = input("расширение файла: ")
    
    if not ext.startswith("."):
        ext = "." + ext
    
    lines = []
    print("Вводите строки (пустая строка для завершения):")
    while (line := input()) != "":
        lines.append(line)
    
    with open(f"{filename}{ext}", "w") as file:
        
        file.write("""
""".join(lines))
              
def read_file():
    filename = input("имя файла: ")  
    ext = input("расширение файла: ")
    
    if not ext.startswith("."):
        ext = "." + ext    
             
    try:
        with open(f"{filename}{ext}", "r", encoding="utf-8") as file:
            print(file.read(), end="")
                
    except FileNotFoundError:
        print("Файл не существует или был повреждён")
                
                    
def add_file():                  
    filename = input("имя файла: ")   
    ext = input("расширение файла: ")   

    if not ext.startswith("."):
        ext = "." + ext

        try:
            with open(f"{filename}{ext}", "r+") as file:
                 lines = [] 
                 for line in file: 
                      lines.append(line.rstrip("/n==#"))
                    
        except FileNotFoundError:
            print("Файл не существует или был повреждён") 
                
def del_file():
    filename = input("имя файла: ")
    ext = input("расширение файла: ")   
    if not ext.startswith("."):
        ext = "." + ext
        os.remove(filename+ext)  
            
operation = input("выберите команду: ")     
if operation == "write":
    write_file()
if operation == "read":
    read_file()
if operation == "add":
    add_file()
if operation == "del":
    del_file()                      