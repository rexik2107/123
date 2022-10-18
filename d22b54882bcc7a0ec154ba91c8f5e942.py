import psutil #для мониторинга системы
import sys #позволяет напрямую работать с интерпритатором
import json
import zipfile
import datetime #для работы с датой и временем
import os
from psutil._common import bytes2human #Для перевода байтов в читабельный вид
import xml.etree.ElementTree as ET #парсит и создает xml

def work(menu, switch):
    print_menu(menu)
    choose(len(menu), switch)

def print_menu(argc):
    for i in range(len(argc)):
        print(i + 1, " " + argc[i])

def choose(count_action, func):
    flag = True
    while flag:
        try:
            print("Действие - ", end="")
            number_action = int(input())
            flag = False
        except Exception:
            print("Нет такого действия")
    if number_action <= count_action:
        try:
            #print("_" * 100)
            func(number_action)()
            #print("_" * 100)
            choose(count_action, func)
        except KeyError as e:
            raise ValueError('Неизвестное значение: {}'.format(e.args[0]))

MENU = ["Информаия о диске", "Работа с файлом", "JSON", "XML", "ZIP", "Выход"] 


def switch_menu(value):
    return {
        1: disk_info,
        2: work_file,
        3: work_json,
        4: work_xml,
        5: work_zip,
        6: sys.exit
    }.get(value)

def disk_info():
    template = "%-17s %8s %8s %8s %8s %5s %5s"
    print(template % ("Устройство", "Кол-во", "Занято", "Свободно", "Использ.", "Тип", "Привод"))
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                continue
        usage = psutil.disk_usage(part.mountpoint)
        print(template % (part.device, bytes2human(usage.total), bytes2human(usage.used), bytes2human(usage.free), int(usage.percent), part.fstype, part.mountpoint))

FILE = ["Создать файл", "Записать в файл", "Считать из файла", "Удалить файл", "ОБратно"]


def switch_file(value):
    return{
        1: create_file,
        2: write_string_in_file,
        3: read_file,
        4: deleted_file,
        5: main
    }.get(value)

def create_file():
    print("Имя файла - ", end="")
    file_name = input()
    open(file_name, "w")


def write_string_in_file():
    print("Имя файла - ", end="")
    file_name = input()
    print("Строка - ", end="")
    string = input()

    try:
        fd = open(file_name, 'w')
        fd.write(string)
    except IOError:
        print("Нет такого файла")


def read_file():
    print("Имя файла - ", end="")
    file_name = input()

    try:
        fd = open(file_name, 'r')
        print(fd.read())
        fd.close()
    except IOError:
        print("Нет такого файла")


def deleted_file():
    print("Имя файла - ", end="")
    file_name = input()

    try:
        os.remove(file_name)
    except IOError:
        print("Нет такого файла")

JSON = ["Создать JSON", "Записать в JSON", "Считать JSON", "Удалить", "Обратно"]


def switch_json(value):
    return {
        1: create_file,
        2: write_string_in_json,
        3: read_json,
        4: deleted_file,
        5: main
    }.get(value)

def write_string_in_json():
    print("Имя файла - ", end="")
    file_name = input()

    data = {'URL': 'mirea.ru', 'name': 'mirea'}

    try:
        with open(file_name, "w") as write_file:
            json.dump(data, write_file)
    except IOError:
        print("Нет аткого файла")


def read_json():
    print("Имя файла - ", end="")
    file_name = input()

    try:
        with open(file_name, "r") as rf:
            decoded_data = json.load(rf)

        print(decoded_data)
    except IOError:
        print("Нет аткого файла")

XML = ["Создать XML", "Записать в XML", "Считать XML", "Удалить XML", "Обратно"]

def switch_xml(value):
    return {
        1: create_file,
        2: write_string_in_xml,
        3: read_xml,
        4: deleted_file,
        5: main
    }.get(value)

def write_string_in_xml():
    print("Имя файла - ", end="")
    file_name = input()

    data = ET.Element('parent')
    ET.SubElement(data, 'child1')
    try:
        my_data = ET.tostring(data)
        with open(file_name, "wb") as binary_file:
            binary_file.write(my_data)
    except IOError:
        print("Нет такого файла")


def read_xml():
    print("Имя файла - ", end="")
    file_name = input()

    try:
        fd = open(file_name, 'r')
        print(fd.read())
        fd.close()
    except IOError:
        print("Нет такого файла")

ZIP = ["Создать ZIP", "Добавить файл в ZIP архив", "Считать ZIP", "Удалить ZIP", "Обратно"]


def switch_zip(value):
    return {
        1: create_zip,
        2: add_file_in_zip,
        3: read_zip,
        4: deleted_file,
        5: main
    }.get(value)
    
def create_zip():
    print("Имя архива - ", end="")
    zip_name = input()
    try:
        zipfile.ZipFile(zip_name, mode='w', compression=zipfile.ZIP_DEFLATED)
    except Exception:
        print("No file")


def add_file_in_zip():
    print("Имя файла - ", end="")
    file_name = input()

    print("Имя архива - ", end="")
    zip_name = input()
    try:
        with zipfile.ZipFile(zip_name, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(file_name)
    except Exception:
        print("Нет такого файла")


def read_zip():
    print("Имя файла - ", end="")
    file_name = input()

    try:
        with zipfile.ZipFile(file_name, mode='a') as zf:
            for file in zf.infolist():
                date = datetime.datetime(*file.date_time)
                name = os.path.basename(file.filename)
                print(f"{name},\t{file.file_size},\t{file.compress_size},\t \
                                       {date.strftime('%H:%M %d.%m.%Y')}")
    except Exception:
        print("Нет такого файла")

def main():
    print_menu(MENU)
    choose(len(MENU), switch_menu)

def work_file():
    work(FILE, switch_file)

def work_json():
    work(JSON, switch_json)

def work_xml():
    work(XML, switch_xml)

def work_zip():
    work(ZIP, switch_zip)

if __name__ == '__main__':
    main()