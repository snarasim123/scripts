import sys
import time
import datetime


def log_to_file(file_name, msg):
    file = open(file_name, 'a')
    file.write(msg)
    file.close()
    return None


def create_log_file():
    datestamp = datetime.date.today().strftime("%b-%d-%Y")
    timestamp = datetime.datetime.now().strftime("%H-%M-%S")

    # output_file = "./output-" + str(datestamp) + str(timestamp) + ".log"
    output_file = "./output-" + str(datestamp) + ".log"

    file = open(output_file, 'a')
    # file.write("\nNew Run at {0} {1}".format(datestamp, timestamp))
    # file.write("\n")
    file.close()
    return output_file


def create_data_file():
    datestamp = datetime.date.today().strftime("%b-%d-%Y")
    timestamp = datetime.datetime.now().strftime("%H-%M-%S")
    data_file = "./data" + ".dat"
    file = open(data_file, 'w')
    file.close()
    return data_file
