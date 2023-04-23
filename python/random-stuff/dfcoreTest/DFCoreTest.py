from typing import Any

import csv
import json
import requests
import time
import concurrent.futures
import timeit
import datetime

from DFCareTeam import CareTeam
from DFPatient import Patient
from DFClient import DFClient
from utilities.log_util import log_to_file, create_log_file

num_threads = 1
input_filename = "./data.dat"
skip_first_line = False
log_file: str
validation_state: bool = True
total_errors: int = 0


def ids_from_file(input_file, line_from, line_to):
    total_lines = file_length(input_file)
    if line_to < line_from:
        return None, -1
    if line_from <= 0 or line_to <= 0:
        return None, -1
    if total_lines < line_from:
        return None, -1

    data_file = open(input_file)
    line_list = data_file.readlines()
    id_list = line_list[line_from - 1:line_to]
    data_file.close()

    return id_list, 0


def file_length(file_name):
    file = open(file_name)
    total_lines: int = len(file.readlines())
    file.close()
    return total_lines


def process(input_file, from_line, to_line):
    log_to_file(log_file, 'Processing lines {0} to {1}\n'.format(from_line, to_line))
    id_list, error = ids_from_file(input_file, from_line, to_line)

    total_threads = to_line - from_line + 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=total_threads) as executor:
        for index in range(total_threads):
            executor.submit(validate, id_list[index].rstrip())
    return


def validate(mongo_id):
    dfclient = DFClient()
    global validation_state
    global total_errors

    try:
        team = dfclient.careteam_read(mongo_id)
        if dfclient.error > 0:
            validation_state = False
            total_errors += dfclient.error
            log_to_file(log_file,
                        "Cateteam Validation Failed to GET Careteam record,  {0} \n".format(mongo_id))
            return None

        dfclient.patient_read(team.patient_mongoid)
        if dfclient.error > 0:
            validation_state = False
            total_errors += dfclient.error
            log_to_file(log_file,
                        "Cateteam Validation Failed to GET Patient, {0} with Patient {1} \n".format(mongo_id,
                                                                                                    team.patient_mongoid))
            return None

        dfclient.carecoach_read(team.carecoach_mongoid)
        if dfclient.error > 0:
            validation_state = False
            total_errors += dfclient.error
            log_to_file(log_file,
                        "Cateteam Validation Failed to GET CareCoach, {0} with Patient {1} and Carecoach {2} \n".format(
                            mongo_id,
                            team.patient_mongoid,
                            team.carecoach_mongoid))
            return None

        log_to_file(log_file,
                    "Validated Cateteam {0} with Patient {1} and Carecoach {2} \n".format(mongo_id,
                                                                                          team.patient_mongoid,
                                                                                          team.carecoach_mongoid))


    except Exception as e:
        log_to_file(log_file, "Error -> exception msg: " + str(e) + "\n")

    return None


def main():
    current_line: int = 1
    to_line: int = 1
    datestamp = datetime.date.today().strftime("%b-%d-%Y")
    start_time: str = datetime.datetime.now().strftime("%H:%M:%S")
    global log_file
    log_file = create_log_file()

    start = timeit.default_timer()
    log_to_file(log_file, "Data validation start at {0} {1}\n".format(datestamp, start_time))

    file_size: int = file_length(input_filename)
    if file_size == 0:
        return

    if skip_first_line:
        current_line = 2
        to_line = 2

    if to_line >= file_size:
        to_line = file_size

    while current_line <= file_size:
        process(input_filename, current_line, to_line)
        current_line = to_line + 1
        to_line = current_line + (num_threads - 1)
        if to_line >= file_size:
            to_line = file_size
    end = timeit.default_timer()

    total_time = end - start
    log_to_file(log_file, "Data validation end = {0}\n".format(datetime.datetime.now().strftime("%H:%M:%S")))
    log_to_file(log_file,
                'Took {0:0.2f} minutes/{1:0.2f} seconds.\n'.format((total_time / 60), total_time))

    if not validation_state:
        log_to_file(log_file, "Data validation failed, found {0} errors from {1} lines\n".format(total_errors,file_size))
    else:
        log_to_file(log_file, "Data validation success, found {0} errors from {1} lines\n".format(total_errors,file_size))


if __name__ == "__main__":
    main()
