import timeit
import datetime

from pymongo import MongoClient

from lib.fhir_mongo.fhir_mongo import FhirMongo
from lib.sqlclient.EotClient import EotClient
from lib.utilities.log import log, create_log_file, create_data_file
import lib.fhir_mongo

data_file: str
log_file: str
id_dict: dict = {}
mongo_client: MongoClient
# db: Database
dry_run: bool = True


def main():
    datestamp = datetime.date.today().strftime("%b-%d-%Y")
    start_time: str = datetime.datetime.now().strftime("%H:%M:%S")

    global data_file
    data_file = create_data_file()
    global log_file
    log_file = create_log_file()
    fhir = FhirMongo()

    # eotclient = EotClient(log_file,data_file)
    start = timeit.default_timer()
    log(log_file, "\nData gen started at {0} {1}\n".format(datestamp, start_time))
    # eotclient.connect()
    # eotclient.fetch_coaches()
    # eotclient.fetch_teams()
    end = timeit.default_timer()
    total_time = end - start

    log(log_file, "Data gen  end = {0}\n".format(datetime.datetime.now().strftime("%H:%M:%S")))
    log(log_file,
        'Took {0:0.2f} minutes/{1:0.2f} seconds To get Carecoach and Careteam ids from eOnTrak.\n'.format((total_time / 60),
                                                                                        total_time))


if __name__ == "__main__":
    main()
