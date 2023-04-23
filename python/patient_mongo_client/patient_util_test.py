import json
from datetime import date, datetime, time
# from pymongo import MongoClient
# from copy import deepcopy
# from deepdiff import DeepDiff
# from bson import ObjectId

from simple_mockforce import mock_salesforce
from simple_salesforce import Salesforce

from simple_mockforce.virtual import virtual_salesforce
MOCK_CREDS = {
    "username": "hi",
    "password": "hello",
    "security_token": "123",
    "domain": "mock",
}


from patient_mongo_client.catasysFHIR import standardizeGender, standardizeDateTime, sMarStat, getPatientExt, Patient, \
    standardizePh, Period
from patient_mongo_client.catasysFHIR import getTelecomExt, ContactPoint, getAddressExt, Address, HumanName, getNameExt, \
    Organization
from patient_mongo_client.catasysFHIR import buildRef, Identifier, CodeableConcept



FAIL_WAIT = 3
PYMONGO_BATCH_SIZE = 10000

BAD_START = ["01/01/0001"]
BAD_END = ["12/31/9999"]
DEFAULT_PERIOD_START = "01/01/1700"
DEFAULT_PERIOD_END = "12/31/4000"

SALESFORCE_INST = "https://test.salesforce.com/"
SALESFORCE_USERNAME = 'salesforce.app.log@catasys.com.apiuser.pmb'
SALESFORCE_PASSWORD = "$j<.+4vbeR)7:5'q'-&~r2ymP`t\:,A+"
SALESFORCE_TOKEN = 'pEvHmySiCA0araNUFgnElTc0j'
SALESFORCE_DOMAIN = 'test'

clientNames = {
    'Aetna': 'Aetna, Inc.',
    'Anthem': None,
    'CapBlueCross': 'Capital BlueCross',
    'Centene': 'Centene Corporation',
    'Centene_TX': 'Centene Corporation',
    'Coventry_MO': 'Coventry Health Care, Inc.',
    'Coventry_IA': 'Coventry Health Care, Inc.',
    'Coventry_NE': 'Coventry Health Care, Inc.',
    'Coventry_KS': 'Coventry Health Care, Inc.',
    'Cigna_HealthSpring': 'Cigna Corporation',
    'HAMP': 'Health Alliance Medical Plans, Inc.',
    'HCSC_IL': 'Health Care Service Corporation',
    'HCSC_OK': 'Health Care Service Corporation',
    'Humana': 'Humana, Inc.',
    'Optima': 'Optima, Inc.'
}

g_healthPlan = 'Cigna Corporation'


# noinspection DuplicatedCode
def createPatient(eRec):
    # update simple HP Keys
    gender = standardizeGender(eRec['gender'])
    birthDate = datetime.strptime(standardizeDateTime(eRec['dob']), "%Y-%m-%dT%H:%M:%S").date()
    maritalStatus = sMarStat(eRec['marStat'])
    active = isActive(eRec)
    orgName = eRec['healthPlan']
    ext = getPatientExt(False)
    patient = Patient(birthDate=birthDate,
                      maritalStatus=CodeableConcept(text=maritalStatus),
                      active=active, source='Health Plan', extension=ext)
    patient = dict(patient)
    if gender in ['male', 'female']:
        patient['gender'] = gender
    contained = []
    ident, c = getHPIdent(eRec)

    a, b = getIdent('Eligibility_Status_Id', "1", orgName)
    ident.append(a)
    c.append(b)
    patient['identifier'] = ident
    contained.extend(c)
    name = getHPName(eRec)
    if name:
        patient['name'] = name
    telecom = getHPTelecom(eRec)
    if telecom:
        patient['telecom'] = telecom
    address = getHPAddress(eRec)
    if address:
        patient['address'] = address
    morg, c = getHPMOrg_local(eRec['healthPlan'])
    contained.extend(c)
    patient['managingOrganization'] = morg
    patient['contained'] = contained
    return patient


# noinspection PyBroadException
# noinspection DuplicatedCode
def cleanDate(dateString):
    """This method is a hack, to ensure that dates coming out of the eligibility table always have the same
    form; as they are strings and can be in many forms.  The more correct fix is to update eligibility to
    always push dates in the same form into the collection, and the most correct fix is to use isoDates,
    not strings."""
    if dateString.count("/") == 2:  # MM/DD/YYYY, expected form
        return dateString
    if dateString.count("-") == 2:  # YYYY-MM-DD or YYYY-MM-DD 00:00:00
        d = dateString.split(" ")[0].split("-")
        return d[1] + "/" + d[2] + "/" + d[0]


# noinspection DuplicatedCode
def isActive(eRec):
    """Accepts an eligibility record, and returns True/False, if the patient is active."""
    eDate = cleanDate(eRec['effectDate'])
    tDate = cleanDate(eRec['termDate'])
    effectDate = datetime.strptime(eDate, "%m/%d/%Y")
    termDate = datetime.strptime(tDate, "%m/%d/%Y")
    if effectDate > datetime.now():
        return False
    if termDate < datetime.now():
        return False
    return True


# noinspection DuplicatedCode
def getContactPoint(ph, use, rank, system='phone'):
    if system == 'phone':
        ph = standardizePh(ph)
    ext = getTelecomExt()
    cp = ContactPoint(system=system, value=ph,
                      use=use, rank=rank, extension=ext)
    cp = dict(cp)
    return cp


# noinspection DuplicatedCode
def getHPTelecom(eRec):
    """Pulls values, if they exist, for eRec: mobilePh, homePh, workPh."""
    telecom = []
    tRank = 1
    homePh = standardizePh(eRec['homePh'])
    mobilePh = standardizePh(eRec['mobilePh'])
    workPh = standardizePh(eRec['workPh'])
    email = eRec['email']
    if email and email != 'NA':
        telecom.append(getContactPoint(email, 'home', tRank, 'email'))
        tRank += 1
    if homePh != 'NA':
        telecom.append(getContactPoint(homePh, 'home', tRank))
        tRank += 1
    if mobilePh != 'NA':
        telecom.append(getContactPoint(mobilePh, 'mobile', tRank))
        tRank += 1
    if workPh != 'NA':
        telecom.append(getContactPoint(workPh, 'work', tRank))
        tRank += 1
    return telecom


# noinspection DuplicatedCode
def getHPAddress(eRec):
    """Returns the address information, given an eligibility record."""
    lines = []
    addr1 = eRec['addr1']
    addr2 = eRec['addr2']
    city = eRec['city']
    state = eRec['state']
    postalCode = eRec['zip']
    if addr1:
        lines.append(addr1)
    if addr2:
        lines.append(addr2)
    timeZone = getTZ_local(postalCode)
    ext = getAddressExt(timezone=timeZone)
    kwargs = {'extension': ext}
    if lines:
        kwargs['line'] = lines
    if city:
        kwargs['city'] = city
    if state:
        kwargs['state'] = state
    if postalCode:
        kwargs['postalCode'] = postalCode
    a = Address(**kwargs)
    # a = dict(a)
    # if len(a.keys()) > 1:  # all address start w/extension, but need more to be valid
    return [a]
    return None


# noinspection DuplicatedCode
def getHPName(eRec):
    fn = eRec['first']
    mn = eRec['middle']
    ln = eRec['last']
    textName = ""
    if fn:
        textName += fn + " "
    if mn:
        textName += mn + " "
    if ln:
        textName += ln
    else:
        if len(textName):
            textName = textName[0:-1]  # trailing space, if no last name provided
    prefix = []
    suffix = []
    n = HumanName(
        use='usual',
        extension=getNameExt()
    )
    n = dict(n)
    if textName:
        n['text'] = textName
    if ln:
        n['family'] = ln
    if fn:
        n['given'] = [fn]
    if len(n.keys()) > 2:  # use, extension exist by default
        return [n]
    return None


# noinspection DuplicatedCode
def getHPIdent(eRec):
    """Returns both a list of identifiers, and contained objects."""
    idents = []
    contained = []
    # set period according to their health plan effect/term dates
    # ->
    eDate = cleanDate(eRec['effectDate'])
    tDate = cleanDate(eRec['termDate'])
    if eDate in BAD_START:
        eDate = None
    if tDate in BAD_END:
        tDate = DEFAULT_PERIOD_END
    if eDate:
        start = datetime.strptime(eDate, '%m/%d/%Y').date()
        end = datetime.strptime(tDate, '%m/%d/%Y').date()
        hpPeriod = Period(start=start, end=end)
    else:
        hpPeriod = None
    i, o = getValidIdent(eRec, 'Ins_Id', 'memId', 'healthPlan', hpPeriod)
    if i and o:
        idents.append(i)
        contained.append(o)
    i, o = getValidIdent(eRec, 'Subscriber_Id', 'subsId', 'healthPlan', hpPeriod)
    if i and o:
        idents.append(i)
        contained.append(o)
    i, o = getValidIdent(eRec, 'Group_Id', 'grpId', 'grpName', hpPeriod)
    if i and o:
        idents.append(i)
        contained.append(o)
    i, o = getValidIdent(eRec, 'MBI_Id', 'mbi', 'healthPlan', hpPeriod)
    if i and o:
        idents.append(i)
        contained.append(o)
    svcId, svcName = getHPSvcInfo(eRec)
    if svcId and svcName:
        i, o = getIdent('Service_Center_Id', svcId, svcName, hpPeriod)
        if i and o:
            idents.append(i)
            contained.append(o)
    return idents, contained


# noinspection DuplicatedCode
def getValidIdent(eRec, text, valKey, assignerKey, period=None):
    if valKey not in eRec.keys():
        return None, None
    if assignerKey not in eRec.keys():
        return None, None
    val = eRec[valKey]
    assigner = eRec[assignerKey]
    if not val or not assigner:
        return None, None
    if not len(val) or not len(assigner):
        return None, None
    return getIdent(text, val, assigner, period)


# noinspection DuplicatedCode
def getHPSvcInfo(eRec):
    invClientNames = {v: k for k, v in clientNames.items()}
    hpName = invClientNames[eRec['healthPlan']]
    elig_state = eRec['state']
    elig_lob = eRec['lob']
    elig_healthplan = eRec['healthPlan']
    elig_plan_type = eRec['planType']

    svcInfo = getSvcCenterInfo_local()

    lob = None

    if elig_lob:
        if elig_lob == 'CP' or 'Commercial' in elig_lob:
            lob = 'Commercial'
        if elig_lob == 'ME':
            lob = 'Medicare'
        if elig_lob == 'MEDICAID':
            lob = 'Medicaid'

    if elig_healthplan == 'Health Alliance Medical Plans, Inc.':
        elig_state = 'IL'  # force all HAMP member's service center to IL
        lob = 'Commercial'
        if elig_plan_type == 'M':
            if eRec['entityCd'] not in ['SUP', 'MNH', 'MSH', 'MPH', 'MSS', 'MWH']:
                lob = 'Medicare'
            else:
                return None, None
        if eRec['grpId'] == '321224' and eRec['entityCd'] == 'IEX':
            lob = 'FFM (HIX)'
        if eRec['grpId'] == '321725' and eRec['entityCd'] in ['IEX', 'ALL', 'ALM', 'MEX', 'PPO']:
            lob = 'Individual'
        if eRec['grpId'][0:1] == 'S':
            lob = 'SelfFund'
        if eRec['entityCd'] == 'WAX':
            return None, None
    if not lob:
        lob = elig_lob
    if elig_healthplan == 'Optima, Inc.':
        if elig_lob in ['Commercial-HMO-FF', 'Commercial-POS-FF', 'Commercial-PPO-FF']:
            lob = 'Commercial'
        elif elig_lob in ['Medicare-DSNPHMOFF', 'MedicareHMOFF']:
            lob = 'Medicare'
        elif elig_lob in ['MedicaidHMOFF', 'Medicaid-MLTSSHMOFF']:
            lob = 'Medicaid'
        else:
            lob = None
        hpName = 'Sentara-Optima'
        elig_state = 'VA'
    svcName = "{} {}: {}".format(hpName, elig_state, lob)
    if svcName in svcInfo.keys():
        return svcInfo[svcName], svcName
    svcName = "{} {} - {}".format(hpName, elig_state, lob)
    if svcName in svcInfo.keys():
        return svcInfo[svcName], svcName
    return None, None  # not found


# noinspection DuplicatedCode
def getIdent(typeText, identValue, assigner, p=None):
    """Returns both an identifier, and associated contained objects."""
    org = Organization(name=assigner)
    r, o = buildRef(org)
    o = dict(o)
    i = Identifier(use='official',
                   type=CodeableConcept(text=typeText),
                   value=identValue, assigner=r)
    i = dict(i)
    if p:
        i['period'] = dict(p)
    return i, o


def getHPMOrg_local(healthplan_name):
    org = Organization(name=healthplan_name)
    r, o = buildRef(org)
    r = dict(r)
    o = dict(o)
    return r, [o]

@mock_salesforce(fresh=True)
def getSvcCenterInfo_local(sf=None):
    sf = Salesforce(**MOCK_CREDS)
    response = sf.Service_Center__c.create({"Name": "Cigna corp"})

    svc_ctr_info = {}
    results = sf.query(f"SELECT Id, Name FROM Service_Center__c")

    for rec in results['records']:
        svc_ctr_info[rec['Name']] = rec['Id']
    return svc_ctr_info


def getTZ_local(z):
    try:

        return 'Pacific'
    except:
        return 'NA'


def main():
    cigna_healthspring_clientname = '"Cigna_HealthSpring"'
    cigna_corp_name = "Cigna Corporation"
    first_name = "Tinker"
    last_name = "Soldier"
    middle_name = "Taylor"
    json_str1 = f'"specCopay": "","locNum":"","relation": "E", "addr1":"909 CARLTON ROAD",  \
                "termDate":"12/31/9999", "pcpCopay": "","ethnicity": "", "subsIdOther": "180662142",  \
                "lob": "", "city": "WYLIE", "memStat": "A", "grpName": "FANNIE MAE", "memIdOther": "180662142",  \
                "bhFlag": "Y","mobilePh": "", "state": "", "race": "", "healthPlan":  \"{cigna_corp_name}\", \
                "pcpId":"888888809","workPh": "", "email": "", "maiden": "","grpId": "00600288", \
                "effectMemberMonth": "12/16/2019","memId":"10021796608325", "marStat": "unknown", "planType":"M", \
                "_id": "5e2e670f8b022211e2792a00", "zip": "75098","dob":"01/07/1981", \
                "gender":"F","dod":"","termReason": "","recInd": "Y","effectDate": "06/21/2010","addr2":"", \
                "pharmCov": "N", "homePh": "972-0658-5497", "subsId": "10021796608325",  \
                "extDate": "01/11/2020 07:04:07", "first": \"{first_name}\","last": \"{last_name}\","middle":\"{middle_name}\"'

    print(json_str1)
    eligibility_rec = json.loads("{" + json_str1 + "}")
    try:
        patient_rec = createPatient(eligibility_rec)
        print(patient_rec)
        pass
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    main()
