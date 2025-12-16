import os
import stat
import time
from pathlib import Path

def ls(args: list[str]) -> None:
    """ 
    Показывает содержимое директории, обрабатывает аргумент -1
    """ 
    path = Path.cwd()
    f = False
    
    for i in range(len(args)):
        arg = args[i]
        if arg == '-1':
            f = True
        elif arg[0] != '-':
            path = Path(arg)

    if not path.exists():
        raise FileNotFoundError("Her каталога")
    if not path.is_dir():
        raise NotADirectoryError("Не каталог")

    items = list(path.iterdir())
    
    if f:
        for item in items:
            stat_info = item.stat()
            mod_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat_info.st_mtime))
            size = stat_info.st_size
            permissions = stat.filemode(stat_info.st_mode)
            
            if permissions == "drwxr-xr-x":
                print(f"DIR {item.name}/")
            else:
                print(f"{permissions} {size:8} {mod_time} {item.name}")
    else:
        for item in items:
            print(item.name)
    

    to_remove = []
    for item in items:
        if item.name.endswith('.tmp'):
            to_remove.append(item)

    for item in to_remove:
        items.remove(item)  
            
    def count_files_by_type(file_list, counter=None):
        if counter is None:
            counter = {"files": 0, "dirs": 0}
        for item in file_list:
            if item.is_file():
                counter["files"] += 1
            else:
                counter["dirs"] += 1
        return counter
    
    stats1 = count_files_by_type(items)
    print(f"Первый вызов: {stats1}")
    stats2 = count_files_by_type(items)
    print(f"Второй вызов: {stats2}")

if __name__ == "__main__":
    test_dir = Path("test_directory")
    test_dir.mkdir(exist_ok=True)
    (test_dir / "test.txt").write_text("test")
    (test_dir / "temp.tmp").write_text("temp")
    
    ls(["-1", "test_directory"])