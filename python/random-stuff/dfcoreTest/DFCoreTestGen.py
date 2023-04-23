from typing import Any

import pymongo
from pymongo import MongoClient
from bson.json_util import dumps, loads
import timeit
import datetime
from utilities.log_util import log_to_file, create_log_file, create_data_file

data_file: str
log_file: str

dev_connection_name = 'Dev'
dev_connect_str = ''
dev_db_name = "catasysfhir"
dev_careteam_collection_name = 'careTeamsFHIR'

stage_connection_name = 'Staging'
stage_connect_str = ''
stage_db_name = 'pipelineprod'
stage_careteam_collection_name = 'careTeamsFHIR'

prod_connection_name = 'Production'
prod_connect_str = ''
prod_db_name = 'pipelineprod'
prod_careteam_collection_name = 'careTeamsFHIR'

current_connection_name = dev_connection_name
current_connection = dev_connect_str
current_db_name = dev_db_name
current_careteam_collection_name = dev_careteam_collection_name


def stage():
    global current_connection_name
    global current_connection
    global current_db_name
    global current_careteam_collection_name

    current_connection_name = stage_connection_name
    current_connection = stage_connect_str
    current_db_name = stage_db_name
    current_careteam_collection_name = stage_careteam_collection_name
    return None


def prod():
    global current_connection_name
    global current_connection
    global current_db_name
    global current_careteam_collection_name

    current_connection_name = prod_connection_name
    current_connection = prod_connect_str
    current_db_name = prod_db_name
    current_careteam_collection_name = prod_careteam_collection_name
    return None


def file_length(file_name):
    file = open(file_name)
    total_lines: int = len(file.readlines())
    file.close()
    return total_lines


def process():
    mongo_client = MongoClient(current_connection)
    db = mongo_client.get_database(current_db_name)
    careteam_collection = db[current_careteam_collection_name]
    counter = 0
    for mongo_doc in careteam_collection.find():
        log_to_file(data_file, "{0}\n".format(mongo_doc['id']))
        counter += 1
    return counter


def main():
    stage()
    datestamp = datetime.date.today().strftime("%b-%d-%Y")
    start_time: str = datetime.datetime.now().strftime("%H:%M:%S")
    global data_file
    data_file = create_data_file()
    global log_file
    log_file = create_log_file()

    start = timeit.default_timer()
    log_to_file(log_file, "Data gen started at {0} {1}\n".format(datestamp, start_time))
    lines_processed = process()
    end = timeit.default_timer()
    total_time = end - start
    # log_to_file(log_file, "\nTime at start = {0} ".format(start_time))
    log_to_file(log_file, "Data gen  end = {0}\n".format(datetime.datetime.now().strftime("%H:%M:%S")))
    log_to_file(log_file,
                'Took {0:0.2f} minutes/{1:0.2f} seconds To generate {2} Careteam ids from {3} mongo.\n'.format(
                    (total_time / 60),
                    total_time, lines_processed, current_connection_name))


if __name__ == "__main__":
    main()
