import os
import sys
import subprocess
import platform

def run(filename, args=None):
    if not os.path.exists(filename):
        print(f"Ошибка: файл '{filename}' не найден")
        return False
    
    filepath = os.path.abspath(filename)
    
    try:
        file_ext = os.path.splitext(filename)[1].lower()
        
        if args is None:
            args = []
        
        if file_ext == '.py':
            subprocess.run([sys.executable, filepath] + args, check=True)
            
        elif file_ext == '.bat':
            if platform.system() == 'Windows':
                subprocess.run([filepath] + args, shell=True, check=True)
            else:
                print("BAT файлы поддерживаются только в Windows")
                return False
                
        elif file_ext == '.sh':
            if platform.system() != 'Windows':
                subprocess.run(['bash', filepath] + args, check=True)
            else:
                print("SH файлы не поддерживаются в Windows")
                return False
                
        elif file_ext == '.exe':
            subprocess.run([filepath] + args, check=True)
            
        else:
            print(f"Неподдерживаемый тип файла: {file_ext}")
            print("Попытка запуска через системную ассоциацию...")
            if platform.system() == 'Windows':
                os.startfile(filepath)
            elif platform.system() == 'Darwin':
                subprocess.run(['open', filepath] + args)
            else:
                subprocess.run(['xdg-open', filepath] + args)
                
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске файла: {e}")
        return False
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return False