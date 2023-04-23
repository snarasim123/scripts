import pyodbc

from lib.utilities.log import log, create_data_file
from fhir.resources.patient import Patient, address, codeableconcept, contactpoint, humanname, identifier, fhirdate
from fhir.resources.careteam import CareTeam, identifier, contactpoint, codeableconcept, period, CareTeamParticipant
from fhir.resources.practitioner import Practitioner, codeableconcept, period, humanname, identifier, fhirdate, contactpoint

fake_api = True


class EotClient(object):
    counter: int = 0
    jdc_str: str = 'jdbc:sqlserver://dmdsql03.corp.{}.com:1433;DatabaseName=eot_{}'
    server_name: str = 'dmdsql03.corp.'
    db_name: str = 'eot_{}'
    username: str = '{}'
    password: str = ''
    cursor: pyodbc.Cursor
    log_file: str = ''
    date_file: str = ''


    sql1: str = \
        'select care_coach_id, c.created_date, first_name, last_name, email_address, office_phone, extension, ' \
        'address_line1, address_line2, city, state_code, zipcode  ' \
        'from eOT_Coachnote.dbo.carecoach c ' \
        'left join eOT_Coachnote.dbo.address_common a on c.care_coach_id = a.common_address_id ' \
        'left join eOT_Coachnote.dbo.state_lkup s on a.state_id = s.state_id ' \
        'join eOT_Coachnote.dbo.aspnet_users au on c.UserId = au.UserId ' \
        'inner join eOT_Coachnote.dbo.aspnet_Membership am on au.UserId = am.UserId ' \
        'where am.IsLockedOut = 0 ' \
        'order by care_coach_id'

    sql2: str = 'select pr.erehab_id, pc.patient_id, pc.care_coach_id, pc.updated_date ' \
                'from patient_carecoach pc ' \
                'inner join eOT_Coachnote.dbo.carecoach c on pc.care_coach_id = c.care_coach_id ' \
                'inner join eOT_Coachnote.dbo.program pr on pc.patient_id = pr.patient_id ' \
                'inner join eOT_Coachnote.dbo.aspnet_users au on c.UserId = au.UserId ' \
                'inner join eOT_Coachnote.dbo.aspnet_Membership am on au.UserId = am.UserId ' \
                'where am.IsLockedOut = 0 AND pr.enroll_status_id in (7,8,9) ' \
                'order by pc.care_coach_id, pr.erehab_id'

    def __init__(self, log_file, data_file):
        self.counter = 0
        self.log_file = log_file
        self.date_file = data_file
        return None

    def connect(self):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server_name + ';DATABASE=' +
                self.db_name + ';UID=' + self.username + ';PWD=' + self.password)
            self.cursor = cnxn.cursor()
        except Exception as e:
            log(self.log_file, "Error Connecting to eot db,  -> exception msg: " + str(e) + "\n")
        return True

    def fetch_coaches(self):
        try:
            fetchcount: int = 0
            ret = self.cursor.execute(self.sql1)
            log(self.log_file, "carecoach ->  care_coach_id, created_date, first_name, last_name, email_address, "
                               "office_phone, extension, address_line1, address_line2, city, state_code, zipcode")
            cc_data_file = create_data_file("carecoach.dat")
            for carecoach in self.cursor.fetchall():
                log(cc_data_file, "{},{},{},{},{},{},{},{},{},{},{},{}\n".format(carecoach.care_coach_id, carecoach.created_date, carecoach.first_name,
                                                carecoach.last_name, carecoach.email_address, carecoach.office_phone,
                                                carecoach.extension, carecoach.address_line1, carecoach.address_line2,
                                                carecoach.city, carecoach.state_code, carecoach.zipcode))
                log(self.log_file, "carecoach -> {0}\n".format(carecoach))
                fetchcount += 1
            self.cursor.close()
            self.connect()

        except Exception as e:
            log(self.log_file, "Error Connecting to eot db,  -> exception msg: " + str(e) + "\n")
        log(self.log_file, "Fetched {0}\n".format(fetchcount))
        return fetchcount

    def fetch_teams(self):
        try:
            fetchcount: int = 0
            ret = self.cursor.execute(self.sql2)
            ct_data_file = create_data_file("careteam.dat")
            log(self.log_file, "careteam -> erehab_id, patient_id, care_coach_id, updated_date")
            for careteam in self.cursor.fetchall():
                log(ct_data_file, "{},{},{},{}\n".format(careteam.erehab_id, careteam.patient_id, careteam.care_coach_id, careteam.updated_date))
                log(self.log_file, "careteam -> {0}\n".format(careteam))
                fetchcount += 1

        except Exception as e:
            log(self.log_file, "Error Connecting to eot db,  -> exception msg: " + str(e) + "\n")
        log(self.log_file, "Fetched {0}\n".format(fetchcount))
        return fetchcount
