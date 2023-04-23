import sys
import time
import datetime


def log(file_name, msg):
    file = open(file_name, 'a')
    file.write(msg)
    file.close()
    return None


def create_log_file():
    datestamp = datetime.date.today().strftime("%b-%d-%Y")
    output_file = "./output-" + str(datestamp) + ".log"
    file = open(output_file, 'w')
    file.close()
    return output_file


def create_data_file(file_name=''):
    data_file: str = ''
    if len(file_name) > 0:
        data_file = file_name
    else:
        data_file = "./data" + ".dat"
    file = open(data_file, 'w')
    file.close()
    return data_file
