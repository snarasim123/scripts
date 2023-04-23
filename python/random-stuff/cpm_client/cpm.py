from lib.restclient.CPMClient import CPM_Client
from lib.restclient.CPMCareCoach import CPM_CareCoach
from lib.utilities.fileutilities import file_length
from lib.utilities.log import log, create_data_file, create_log_file
import csv
import datetime

input_filename = "./input.csv"


def main():
    file_size = file_length(input_filename)
    if file_size == 0:
        return
    cpm_client = CPM_Client()
    cpm_client.set_env(stage=True)
    with open(input_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print('Skipping First row with Column names.')
                line_count += 1
            else:
                columns = len(row)
                if columns != 12:
                    print('Skipping row, number of csv columns is not 12')
                    continue
                cpm_client.set_carecoach(carecoach_id=row[0],
                                         created_date=row[1],
                                         first_name=row[2],
                                         last_name=row[3],
                                         email_address=row[4],
                                         office_phone=row[5],
                                         extension=row[6],
                                         address_line1=row[7],
                                         address_line2=row[8],
                                         city=row[9],
                                         state_code=row[10],
                                         zipcode=row[11])
                response = cpm_client.carecoach_post()
                if response is None:
                    print('Error Posting CC')
                else:
                    print('Posted 1 CC and got response {}'.format(response))
                line_count += 1
        print('Processed {} lines.'.format(line_count))


if __name__ == "__main__":
    main()
