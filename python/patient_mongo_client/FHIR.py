import builtins
from datetime import date, time, datetime, MINYEAR
import uuid
import json
import pprint
import decimal
import ast

from patient_mongo_client.Validator import *

Validator.types_mapping['datetime.date'] = TypeDefinition('datetime.date', (date,), ())
Validator.types_mapping['datetime.time'] = TypeDefinition('datetime.time', (time,), ())

# constants, to help define/create extensions
APISERVER = "https://APISERVER"
EXTROOT = "{}/fhir/catasys".format(APISERVER)
COPAYPLANS = ['Coventry Health Care', 'Aetna, Inc.', 'Health Alliance Medi', 'Centene Corporation']


# helper methods, for generating Patient
def getPatientExt(allPhoneOptOut=False, allEmailOptOut=False, allDirectMailOptOut=False):
    _extension = []

    # removed the /channeloptout 1/27 JIRA ticket DF-642
    _extension.append(ExtensionBool(url="phone", valueBoolean=bool(allPhoneOptOut)))
    _extension.append(ExtensionBool(url="email", valueBoolean=bool(allEmailOptOut)))
    _extension.append(ExtensionBool(url="directmail", valueBoolean=bool(allDirectMailOptOut)))
    ext = []
    ext.append(ExtensionNested(url=EXTROOT + "/channeloptout", extension=_extension))
    return ext


def getTelecomExt(pref='Unknown', consent='NA', status='NA', source='Health Plan'):
    ext = []
    if pref:
        ext.append(Extension(url=EXTROOT + "/preference", valueCode=pref))
    if consent:
        ext.append(Extension(url=EXTROOT + "/SMSconsent", valueCode=consent))
    if status:
        ext.append(Extension(url=EXTROOT + "/status", valueCode=status))
    if source:
        ext.append(Extension(url=EXTROOT + "/source", valueCode=source))
    ext.append(ExtensionValueDateTime(url=EXTROOT + "/timelastmodified", valueDateTime=datetime.now()))
    ext.append(ExtensionValueDateTime(url=EXTROOT + "/timecreated", valueDateTime=datetime.now()))
    return ext


def getAddressExt(pref=None, source='Health Plan', timezone=None):
    ext = []
    if pref:
        ext.append(Extension(url=EXTROOT + "/preference", valueCode=pref))
    if source:
        ext.append(Extension(url=EXTROOT + "/source", valueCode=source))
    if timezone:
        ext.append(Extension(url=EXTROOT + "/timezone", valueCode=timezone))
    ext.append(ExtensionValueDateTime(url=EXTROOT + "/timelastmodified", valueDateTime=datetime.now()))
    ext.append(ExtensionValueDateTime(url=EXTROOT + "/timecreated", valueDateTime=datetime.now()))
    return ext


def getNameExt(pref=None, source='Health Plan'):
    ext = []
    if pref:
        ext.append(Extension(url=EXTROOT + "/preference", valueCode=pref))
    if source:
        ext.append(Extension(url=EXTROOT + "/source", valueCode=source))
    ext.append(ExtensionValueDateTime(url=EXTROOT + "/timelastmodified", valueDateTime=datetime.now()))
    ext.append(ExtensionValueDateTime(url=EXTROOT + "/timecreated", valueDateTime=datetime.now()))
    return ext

#_ml_ added on 4/19/2021 for JIRA ticket PIPE-481
def getCommunicationExt(valCode):
    ext = []
    ext.append(Extension(url="https://APISERVER/fhir/catasys/source", valueCode=valCode))
    return ext

def standardizeDateTime(s):
    """Accepts a string of some forms:
        - MM/DD/YYYY
        - YYYY-MM-DD
        - YYYY-MM-DD HH:MM:SS
        - ...

        returns in YYYY-MM-DDTHH:MM:SS"""
    if "/" in s:
        s = s.split("/")
        s = s[2] + "-" + s[0] + "-" + s[1] + "T00:00:00"
        return s
    if "-" in s:
        s = s.split(" ")[0]
        s = s + "T00:00:00"
        return s

    return s


def standardizeGender(s):
    """
    Given a string, s, which describes a gender,
    return 'male', 'female', or 'unknown'
    """
    try:
        if s[0].lower() == 'm':
            return 'male'
        if s[0].lower() == 'f':
            return 'female'
    except:
        return 'unknown'  # default, no other options


def _standardizePh(s):
    """
    Given a phone number string, s, of any form like:
    (111) 555-1234, or any other style, return
    just the numerics, ie: 1115551234
    """
    try:
        if not s:
            return 'NA'
        try:
            s = str(s)
        except:
            return 'NA'
        d = ''
        for i in s:
            if i.isdigit():
                d = d + i
        return """+1{}""".format(d)
    except:
        return 'NA'


def standardizePh(s):
    if not s:
        return 'NA'
    try:
        s = str(s)
    except:
        return 'NA'
    if s.startswith("+1"):
        s = s[2:]
    s = _standardizePh(s)  # +1AAA0BBBCCCC
    if len(s) == 12:
        return s
    if len(s) == 13 and s[5] == '0':
        return s[0:5] + s[6:]
    return 'NA'  # number did not parse, somehow


def sMarStat(s):
    """Given a string, s, which describes marital
    status, return a standardization of that status.
    allowed: 'single','married','unknown'
    """
    try:
        if s[0].lower == 's':
            return 'single'
        if s[0].lower == 'm':
            return 'married'
        return 'unknown'
    except:
        return 'unknown'


def buildRef(o):
    """Given an object o, build its referece internally, and
  and return a Refernece to it."""
    # gather identifying data
    u = str(uuid.uuid4())
    t = o.resourceType
    ref = t + "/#" + u
    o.id = u
    return Reference(reference=ref, display=None, type=t), o


# add datetime mappings to Validator
datetime_date_type = TypeDefinition('datetime.date', (date,), ())
Validator.types_mapping['datetime.date'] = datetime_date_type
datetime_time_type = TypeDefinition('datetime.time', (time,), ())
Validator.types_mapping['datetime.time'] = datetime_time_type


class BadDataVal(Exception):
    pass


class Jasonable(object):
    def __init__(self, kwargs):
        commonKeys = [x for x in list(kwargs.keys()) if x in list(self.schema.keys())]
        if 'extension' in list(kwargs.keys()):
            commonKeys.append('extension')
        self.data = {}
        for k in commonKeys:
            setattr(self, k, kwargs[k])
            self.data[k] = kwargs[k]
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)

    def __iter__(self):
        keys = list(self.schema.keys())
        extraKeys = ['id', 'meta', 'contained', 'resourceType', 'extension']
        keys.extend(extraKeys)
        for k in keys:
            attr = k
            try:
                value = getattr(self, k)  # not all objects support ref, contained
            except:
                continue
            # skip empty strings
            if k not in extraKeys:
                if self.schema[k].get('type') == 'string':
                    if not value:
                        continue
            # omit data construct
            if k == 'data':
                continue
            elif k == 'meta':
                yield attr, value
            elif k == 'resourceType':
                if hasattr(self, "id"):
                    yield attr, self.resourceType
                    continue
                if self.resourceType == 'Patient':
                    yield attr, self.resourceType
                    continue
                else:
                    continue
            elif isinstance(value, date):
                try:
                    yield attr, datetime(value.year, value.month, value.day, value.hour, value.minute, value.second)
                except AttributeError:
                    yield attr, datetime(value.year, value.month, value.day)
            elif isinstance(value, decimal.Decimal):
                yield attr, str(value)
            elif (hasattr(value, '__iter__')):
                if (hasattr(value, 'pop')):
                    a = []
                    for subval in value:
                        if (hasattr(subval, '__iter__')):
                            try:
                                a.append(dict(subval))
                            except ValueError:
                                raise
                        else:
                            a.append(subval)
                    yield attr, a
                else:
                    yield attr, (value)
            else:
                yield attr, value

    def getdict(self):
        return dict(self)

    def getjson(self):
        return json.dumps(dict(self), sort_keys=True, indent=2)

    def getdict(self):
        return dict(self)

    def getjson(self):
        return json.dumps(dict(self), sort_keys=True, indent=2)

    def appendField(self, fieldName, value):
        attrib = getattr(self, fieldName)
        attrib.append(value)


class Resource(Jasonable):
    """
    Resource level objects support the meta tag.
    Right now, our meta tag only supports lastUpdated.
    The format of the datetime must be YYYY-MM-DDTHH:MM:SS
    """

    def __init__(self, kwargs):
        super(Resource, self).__init__(kwargs)
        lastUpdated = kwargs.get('lastUpdated')
        if not lastUpdated:
            lastUpdated = datetime.now()
        self.meta = {'lastUpdated': lastUpdated}


class Link:
    LinkType = ['replaced-by', 'replaces', 'refer', 'seealso']

    def __init__(self, person, linktype):
        self.other = person
        self.type = linktype


class CodeableConcept(Jasonable):
    schema = {
        'text': {'type': 'string', 'maxlength': 50}
    }
    V = Validator(schema)
    url = 'https://www.hl7.org/fhir/datatypes.html#CodeableConcept'
    resourceType = 'CodeableConcept'

    def __init__(self, **kwargs):
        super(CodeableConcept, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['CodeableConcept'] = TypeDefinition('CodeableConcept', (CodeableConcept,), ())


class Condition(Jasonable):
    schema = {
        "language": {"type": "string"},
        "expression": {"type": "boolean"}
    }
    V = Validator(schema)
    url = 'https://www.hl7.org/fhir/extensibility.html'
    resourceType = 'Condition'

    def __init__(self, **kwargs):
        super(Condition, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Condition'] = TypeDefinition('Condition', (Condition,), ())


class ValueTriggerDefinition(Jasonable):
    schema = {
        'type': {'type': 'string'},
        'name': {'type': 'string'},
        'timingDateTime': {'type': 'datetime.datetime'},
        'condition': {'type': 'Condition'},
    }
    V = Validator(schema)
    url = 'https://www.hl7.org/fhir/extensibility.html'
    resourceType = 'ValueTriggerDefinition'

    def __init__(self, **kwargs):
        super(ValueTriggerDefinition, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['ValueTriggerDefinition'] = \
    TypeDefinition('ValueTriggerDefinition', (ValueTriggerDefinition,), ())


class ExtensionBool(Jasonable):
    schema = {
        'url': {'type': 'string'},
        'valueBoolean': {'type': 'boolean'}
    }
    V = Validator(schema)
    resourceType = "ExtensionBool"

    def __init__(self, **kwargs):
        super(ExtensionBool, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['ExtensionBool'] = \
    TypeDefinition('ExtensionBool', (ExtensionBool,), ())


class ExtensionNested(Jasonable):
    schema = {
        'url': {'type': 'string'},
        'extension': {'type': 'list', 'schema': {'type': 'Extension'}}
    }
    V = Validator(schema)
    resourceType = "ExtensionNested"

    def __init__(self, **kwargs):
        super(ExtensionNested, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['ExtensionNested'] = \
    TypeDefinition('ExtensionNested', (ExtensionNested,), ())


class ExtensionValueDateTime(Jasonable):  # this valueDateTime allows real datetime, not string
    schema = {
        'url': {'type': 'string'},
        'valueDateTime': {'type': 'datetime.datetime'}
    }
    V = Validator(schema)
    url = 'https://www.hl7.org/fhir/extensibility.html'
    resourceType = 'ExtensionValueDateTime'

    def __init__(self, **kwargs):
        super(ExtensionValueDateTime, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['ExtensionValueDateTime'] = \
    TypeDefinition('ExtensionValueDateTime', (ExtensionValueDateTime,), ())


class ValueIdentifier(Jasonable):
    schema = {
        "value": {'type': 'string'},
        "period": {'type': 'Period'}
    }
    V = Validator(schema)
    url = 'https://www.hl7.org/fhir/extensibility.html'
    resourceType = 'ValueIdentifier'

    def __init__(self, **kwargs):
        super(ValueIdentifier, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['ValueIdentifier'] = \
    TypeDefinition('ValueIdentifier', (ValueIdentifier,), ())


class ExtensionValueIdentifier(Jasonable):
    schema = {
        'url': {'type': 'string'},
        'valueIdentifier': {'type': 'ValueIdentifier'}
    }
    V = Validator(schema)
    url = 'https://www.hl7.org/fhir/extensibility.html'
    resourceType = 'ExtensionValueIdentifier'

    def __init__(self, **kwargs):
        super(ExtensionValueIdentifier, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['ExtensionValueIdentifier'] = \
    TypeDefinition('ExtensionValueIdentifier', (ExtensionValueIdentifier,), ())


class ExtensionValueTriggerDefinition(Jasonable):
    schema = {
        'url': {'type': 'string'},
        'valueTriggerDefinition': {'type': 'ValueTriggerDefinition'}
    }
    V = Validator(schema)
    url = 'https://www.hl7.org/fhir/extensibility.html'
    resourceType = 'ExtensionValueTriggerDefinition'

    def __init__(self, **kwargs):
        super(ExtensionValueTriggerDefinition, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['ExtensionValueTriggerDefinition'] = \
    TypeDefinition('ExtensionValueTriggerDefinition', (ExtensionValueTriggerDefinition,), ())


class Extension(Jasonable):
    """
  Support for various extentions in our data model.
  Currently we only support two fields: url, and valueCode
  """
    schema = {
        'url': {'type': 'string'},
        'valueCode': {'type': 'string'}
    }
    V = Validator(schema)
    url = 'https://www.hl7.org/fhir/extensibility.html'
    resourceType = 'Extension'

    def __init__(self, **kwargs):
        super(Extension, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Extension'] = TypeDefinition('Extension', (Extension,), ())


class Reference(Jasonable):
    """
  We support references to ensure proper FHIR communication.
  The structure of the data pipeline MongoDB is embedded, to avoid many queries.
  So, the information which would be referenced, must be embedded.
  To accomplish this, we leverage the FHIR "contained" concept
  """

    schema = {
        'reference': {'type': 'string'},
        'display': {'nullable': True, 'type': 'string'},
        'type': {'nullable': True, 'type': 'string'}  # a FHIR class, e.g. "Patient"
    }
    V = Validator(schema)
    url = 'https://www.hl7.org/fhir/datatypes.html#Reference'
    resourceType = 'Reference'

    def __init__(self, **kwargs):
        super(Reference, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Reference'] = TypeDefinition('Reference', (Reference,), ())


class Address(Jasonable):
    schema = {
        'line': {'type': 'list', 'schema': {'type': 'string', 'maxlength': 30}},  # street1, street2, etc.
        'city': {'type': 'string', 'maxlength': 30},
        'state': {'type': 'string', 'maxlength': 20},
        'postalCode': {'type': 'string', 'maxlength': 10}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/datatypes.html#Address'
    resourceType = 'Address'

    def __init__(self, **kwargs):
        super(Address, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Address'] = TypeDefinition('Address', (Address,), ())


class Period(Jasonable):
    schema = {
        'start': {'nullable': True, 'type': 'datetime.date'},
        'end': {'nullable': True, 'type': 'datetime.date'}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/datatypes.html#Period'
    resourceType = 'Period'

    def __init__(self, **kwargs):
        super(Period, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Period'] = TypeDefinition('Period', (Period,), ())


class Communication(Jasonable):
    schema = {
        'language': {'type': 'CodeableConcept'},
        'preferred': {'type': 'boolean'}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/patient-definitions.html#Patient.communication.language'
    resourceType = 'Communication'

    def __init__(self, **kwargs):
        super(Communication, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Communication'] = TypeDefinition('Communication', (Communication,), ())


class Identifier(Jasonable):
    schema = {
        'use': {'type': 'string', 'allowed': ['usual', 'official', 'temp', 'secondary', 'old']},
        'type': {'type': 'CodeableConcept'},
        'system': {'nullable': True, 'type': 'string'},
        'value': {'type': 'string'},
        'period': {'type': 'Period'},
        'assigner': {'type': 'Reference', 'schema': {'type': 'Organization'}}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/datatypes.html#Identifier'
    resourceType = 'Identifier'

    def __init__(self, **kwargs):
        super(Identifier, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Identifier'] = TypeDefinition('Identifier', (Identifier,), ())


class HumanName(Jasonable):
    schema = {
        'use': {'type': 'string', 'allowed': ['usual', 'official', 'temp', 'nickname', 'anonymous', 'old', 'maiden']},
        'text': {'type': 'string', 'maxlength': 40},
        'family': {'type': 'string', 'maxlength': 40},
        'given': {'type': 'list', 'schema': {'type': 'string', 'maxlength': 20}},
        'prefix': {'type': 'list', 'schema': {'type': 'string', 'maxlength': 20}},
        'suffix': {'type': 'list', 'schema': {'type': 'string', 'maxlength': 20}},
        'period': {'type': 'Period'}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/datatypes.html#HumanName'
    resouceType = 'HumanName'

    def __init__(self, **kwargs):
        super(HumanName, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['HumanName'] = TypeDefinition('HumanName', (HumanName,), ())


# Details for all kinds of technology-mediated contact points for a person or organization, including telephone, email, etc.
class ContactPoint(Jasonable):
    schema = {
        'system': {'type': 'string', 'allowed': ['phone', 'fax', 'email', 'pager', 'url', 'sms', 'other']},
        'value': {'type': 'string', 'maxlength': 80},
        'use': {'type': 'string', 'allowed': ['home', 'work', 'temp', 'old', 'mobile']},
        'rank': {'type': 'integer', 'allowed': [1, 2, 3, 4, 5]},  # 1 is highest/best rank
        'period': {'type': 'Period'}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/datatypes.html#ContactPoint'
    resourceType = 'ContactPoint'

    # def __init__(self, system, value, use, period, rank=1, extension=[]):
    def __init__(self, **kwargs):
        super(ContactPoint, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['ContactPoint'] = TypeDefinition('ContactPoint', (ContactPoint,), ())


class PatientContact(Jasonable):
    schema = {
        'relationship': {'type': 'CodeableConcept'},
        'name': {'type': 'HumanName'},
        'telecom': {'type': 'list', 'schema': {'type': 'ContactPoint'}},
        'address': {'type': 'Address'},
        'gender': {'type': 'string', 'allowed': ['male', 'female', 'other', 'unknown']},
        'period': {'type': 'Period'},
        'organization': {'type': 'Reference', 'schema': {'type': 'Organization'}}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/patient-definitions.html#Patient.contact'
    resourceType = 'PatientContact'

    def __init__(self, **kwargs):
        super(PatientContact, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['PatientContact'] = TypeDefinition('PatientContact', (PatientContact,), ())


class OrganizationContact(Jasonable):
    schema = {
        'purpose': {'type': 'CodeableConcept'},
        'name': {'type': 'HumanName'},
        'telecom': {'type': 'list', 'schema': {'type': 'ContactPoint'}},
        'address': {'type': 'Address'}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/organization-definitions.html#Organization.contact'
    resourceType = 'OrganizationContact'

    def __init__(self, **kwargs):
        super(OrganizationContact, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['OrganizationContact'] = TypeDefinition('OrganizationContact', (OrganizationContact,), ())


# This resource may be used in a shared registry of contact and other information for various organizations or it can be used merely as a 
# support for other resources that need to reference organizations, perhaps as a document, message or as a contained resource. If using a 
# registry approach, it's entirely possible for multiple registries to exist, each dealing with different types or levels of organization.
class Organization(Jasonable):
    schema = {
        'identifier': {'type': 'list', 'schema': {'type': 'Identifier'}},
        'active': {'nullable': True, 'type': 'boolean'},
        'type': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'name': {'type': 'string', 'maxlength': 80},
        'telecom': {'type': 'list', 'schema': {'type': 'ContactPoint'}},
        'address': {'type': 'list', 'schema': {'type': 'Address'}},
        'contact': {'type': 'list', 'schema': {'type': 'OrganizationContact'}}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/organization.html#Organization'
    resourceType = 'Organization'

    def __init__(self, **kwargs):
        super(Organization, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Organization'] = TypeDefinition('Organization', (Organization,), ())


class PractitionerQualification(Jasonable):
    schema = {
        'identifier': {'type': 'list', 'schema': {'type': 'Identifier'}},
        'code': {'type': 'CodeableConcept'},
        'period': {'type': 'Period'},
        'issuer': {'type': 'Reference', 'schema': {'type': 'Organization'}}
    }
    V = Validator(schema)
    url = 'https://hl7.org/fhir/R4/practitioner-definitions.html#Practitioner.qualification'
    resourceType = 'PractitionerQualification'

    def __init__(self, **kwargs):
        super(PractitionerQualification, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['PractitionerQualification'] = TypeDefinition('PractitionerQualification',
                                                                      (PractitionerQualification,), ())


class AvailableTime(Jasonable):
    schema = {
        'daysOfWeek': {'type': 'list',
                       'schema': {'type': 'string', 'allowed': ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']}},
        'allDay': {'type': 'boolean'},
        'availableStartTime': {'type': 'datetime.time'},
        'availableEndTime': {'type': 'datetime.time'}
    }
    V = Validator(schema)
    url = 'https://hl7.org/fhir/R4/practitionerrole-definitions.html#PractitionerRole.availableTime'
    resourceType = 'AvailableTime'

    def __init__(self, **kwargs):
        super(AvailableTime, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['AvailableTime'] = TypeDefinition('AvailableTime', (AvailableTime,), ())


class NotAvailable(Jasonable):
    schema = {
        'description': {'type': 'string', 'maxlength': 30},
        'during': {'type': 'Period'}
    }
    V = Validator(schema)
    url = 'https://hl7.org/fhir/R4/practitionerrole-definitions.html#PractitionerRole.notAvailable'
    resourceType = 'NotAvailable'

    def __init__(self, **kwargs):
        super(NotAvailable, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['NotAvailable'] = TypeDefinition('NotAvailable', (NotAvailable,), ())


class HoursOfOperation(Jasonable):
    schema = {
        'daysOfWeek': {'type': 'list',
                       'schema': {'type': 'string', 'allowed': ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']}},
        'allDay': {'type': 'boolean'},
        'openingTime': {'type': 'datetime.time'},
        'closingTime': {'type': 'datetime.time'}
    }
    V = Validator(schema)
    url = 'https://hl7.org/fhir/R4/location-definitions.html#Location.hoursOfOperation'
    resourceType = 'HoursOfOperation'

    def __init__(self, **kwargs):
        super(HoursOfOperation, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['HoursOfOperation'] = TypeDefinition('HoursOfOperation', (HoursOfOperation,), ())


class Position(Jasonable):
    schema = {
        'longitude': {'type': 'float', 'min': -124.44, 'max': -66.57},  # Continental US East and West
        'latitude': {'type': 'float', 'min': 24.5, 'max': 49.23},  # Continental US North and South
        'altitude': {'type': 'float', 'min': -279, 'max': 20320},  # Continental US lowest and highest in feet
    }
    V = Validator(schema)
    url = 'https://hl7.org/fhir/R4/location-definitions.html#Location.position'
    resourceType = 'Position'

    def __init__(self, **kwargs):
        super(Position, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Position'] = TypeDefinition('Position', (Position,), ())


# An endpoint describes the technical details of a location that can be connected to for the delivery/retrieval of information. 
# Sufficient information is required to ensure that a connection can be made securely, and appropriate data transmitted as 
# defined by the endpoint owner. This is not a description of details of the current system, as found in CapabilityStatement, 
# but of another (potentially external) system.
class Endpoint(Jasonable):
    schema = {
        'identifier': {'type': 'list', 'schema': {'type': 'Identifier'}},
        'status': {'type': 'string', 'allowed': ['active', 'suspended', 'error', 'off', 'entered-in-error', 'test']},
        'name': {'type': 'string', 'maxlength': 30},
        'managingOrganization': {'type': 'Reference', 'schema': {'type': 'Organization'}},
        'contact': {'type': 'list', 'schema': {'type': 'ContactPoint'}},
        'period': {'type': 'Period'},
        'address': {'type': 'string', 'maxlength': 2000}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/endpoint.html#Endpoint'
    resourceType = 'Endpoint'

    connectionType = 'RESTful'  # Protocol/Profile/Standard to be used with this Endpoint connection
    payloadType = ['FHIR-JSON',
                   'FHIR-XML']  # The type of content that may be used at this Endpoint (e.g. XDS Discharge summaries)
    payloadMimeType = []  # Mimetype to send. If not specified, the content could be anything, including no payload
    header = []  # Usage depends on the channel type

    def __init__(self, **kwargs):
        super(Endpoint, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Endpoint'] = TypeDefinition('Endpoint', (Endpoint,), ())


# A Location includes both incidental locations (a place which is used for healthcare without prior designation or authorization) 
# and dedicated, formally appointed locations. Locations may be private, public, mobile or fixed and scale from small freezers to 
# full hospital buildings or parking garages.
class Location(Jasonable):
    schema = {
        'identifier': {'type': 'list', 'schema': {'type': 'Identifier'}},
        'status': {'type': 'string', 'allowed': ['active', 'suspended', 'inactive']},
        'name': {'type': 'string', 'maxlength': 30},
        'description': {'type': 'string', 'maxlength': 30},
        'mode': {'type': 'string', 'allowed': ['instance', 'kind']},
        'type': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'telecom': {'type': 'list', 'schema': {'type': 'ContactPoint'}},
        'address': {'type': 'Address'},
        'endpoint': {'type': 'list', 'schema': {'type': 'Reference', 'schema': {'type': 'Endpoint'}}}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/location.html#Location'
    ResourceType = 'Location'
    operationalStatus = None  # The operational status of the Location (typically only for a bed/room)

    def __init__(self, **kwargs):
        super(Location, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Location'] = TypeDefinition('Location', (Location,), ())


# Practitioner covers all individuals who are engaged in the healthcare process and healthcare-related services as part of their formal
# responsibilities and this Resource is used for attribution of activities and responsibilities to these individuals. Practitioners 
# include (but are not limited to):
#   physicians, dentists, pharmacists, physician assistants, nurses, scribes, midwives, dietitians, therapists, optometrists, paramedics
#   medical technicians, laboratory scientists, prosthetic technicians, radiographers, social workers, professional homecare providers, 
#   official volunteers, receptionists handling patient registration, IT personnel merging or unmerging patient records,
#   Service animal (e.g., ward assigned dog capable of detecting cancer in patients)
class Practitioner(Jasonable):
    schema = {
        'identifier': {'type': 'list', 'schema': {'type': 'Identifier'}},
        'active': {'type': 'boolean'},
        'name': {'type': 'list', 'schema': {'type': 'HumanName'}},
        'gender': {'type': 'string', 'allowed': ['male', 'female', 'other', 'unknown']},
        'telecom': {'type': 'list', 'schema': {'type': 'ContactPoint'}},
        'address': {'type': 'list', 'schema': {'type': 'Address'}},
        'qualification': {'type': 'list', 'schema': {'type': 'PractitionerQualification'}},
        'communication': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/practitioner.html#Practitioner'
    resourceType = 'Practitioner'

    def __init__(self, **kwargs):
        super(Practitioner, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Practitioner'] = TypeDefinition('Practitioner', (Practitioner,), ())


# Specific eligibility requirements required to use the HealthCareService
class Eligibility(Jasonable):
    schema = {
        'code': {'type': 'CodeableConcept'},
        'comment': {'type': 'string', 'maxlength': 30}
    }
    V = Validator(schema)
    url = 'https://hl7.org/fhir/R4/healthcareservice-definitions.html#HealthcareService.eligibility'
    resourceType = 'Eligibility'

    def __init__(self, **kwargs):
        super(Eligibility, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Eligibility'] = TypeDefinition('Eligibility', (Eligibility,), ())


# The HealthcareService resource is used to describe a single healthcare service or category of services that are 
# provided by an organization at a location. The location of the services could be virtual, as with telemedicine 
# services. Common examples of HealthcareServices resources are:
#   Allied Health, Clinical Neuropsychologist, Podiatry Service, Smallville Hospital Emergency Services,
#   Respite care provided at a nursing home or hostel, 24hr crisis telephone counseling service,
#   Information, advice and/or referral services; Disability, Telecommunications, Rural TeleHealth Services,
#   Hospital in the home, Yellow Cabs, Pharmacy, Active Rehab, Social Support, Drug and/or alcohol counseling
#   Day Programs, Adult Training & Support Services, Consulting psychologists and/or psychology services,
#   Group Hydrotherapy, Little River Home Maintenance

class HealthCareService(Jasonable):
    schema = {
        'identifier': {'type': 'list', 'schema': {'type': 'Identifier'}},
        'active': {'type': 'boolean'},
        'category': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'type': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'specialty': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'name': {'type': 'string', 'maxlength': 20},
        'comment': {'type': 'string', 'maxlength': 20},
        'program': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'characteristic': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'communication': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'serviceProvisionCode': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'providedBy': {'type': 'Reference', 'schema': {'type': 'Organization'}},
        'referralMethod': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'location': {'type': 'list', 'schema': {'type': 'Reference', 'schema': {'type': 'Location'}}},
        'telecom': {'type': 'list', 'schema': {'type': 'ContactPoint'}},
        'coverageArea': {'type': 'list', 'schema': {'type': 'Reference', 'schema': {'type': 'Location'}}},
        'eligibility': {'type': 'list', 'schema': {'type': 'Eligibility'}},  # eligibility requirements to use service
        'availableTime': {'type': 'list', 'schema': {'type': 'AvailableTime'}},
        'appointmentRequired': {'type': 'boolean'}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/healthcareservice.html#HealthcareService'
    resourceType = 'HealthcareService'

    def __init__(self, **kwargs):
        super(HealthCareService, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['HealthCareService'] = TypeDefinition('HealthCareService', (HealthCareService,), ())


# PractitionerRole covers the recording of the location and types of services that Practitioners are able to provide for an organization.
# The role, specialty, Location, telecom, and HealthcareService properties can be repeated if required in other instances of the 
# PractitionerRole. Some systems record a collection of service values for a single location, others record the single service and 
# the list of locations it is available. Both are acceptable options for representing this data.
# Where availability, telecom, or other details are not the same across all healthcare services, or locations a seperate PractitionerRole
# instance should be created.
class PractitionerRole(Jasonable):
    schema = {
        'identifier': {'type': 'list', 'schema': {'type': 'Identifier'}},
        'active': {'type': 'boolean'},
        'practitioner': {'type': 'Reference', 'schema': {'type': 'Practitioner'}},
        'organization': {'type': 'Reference', 'schema': {'type': 'Organization'}},
        'code': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'specialty': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'healthcareService': {'type': 'list', 'schema': {'type': 'Reference', 'schema': {'type': 'HealthCareService'}}},
        'telecom': {'type': 'list', 'schema': {'type': 'ContactPoint'}},
        'availableTime': {'type': 'list', 'schema': {'type': 'AvailableTime'}}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/practitionerrole.html#PractitionerRole'
    resourceType = 'PractitionerRole'

    def __init__(self, **kwargs):
        super(PractitionerRole, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['PractitionerRole'] = TypeDefinition('PractitionerRole', (PractitionerRole,), ())


class Patient(Resource):
    schema = {
        'identifier': {'type': 'list', 'schema': {'type': 'Identifier'}},
        'active': {'type': 'boolean'},
        'name': {'type': 'list', 'schema': {'type': 'HumanName'}},
        'telecom': {'type': 'list', 'schema': {'type': 'ContactPoint'}},
        'address': {'type': 'list', 'schema': {'type': 'Address'}},
        'contact': {'type': 'list', 'schema': {'type': 'PatientContact'}},
        'communication': {'type': 'list', 'schema': {'type': 'Communication'}},
        'generalPractitioner': {'type': 'list', 'schema': {'type': 'Reference', 'schema': {'oneof_schema':
            [
                {'type': 'Practitioner'},
                {'type': 'Organization'},
                {'type': 'PractitionerRole'}
            ]}}},
        'gender': {'type': 'string', 'allowed': ['male', 'female', 'other', 'unknown']},
        'birthDate': {'type': 'datetime.date'},
        'maritalStatus': {'type': 'CodeableConcept'},
        'managingOrganization': {'type': 'Reference', 'schema': {'type': 'Organization'}}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/patient.html'
    resourceType = 'Patient'

    def __init__(self, **kwargs):
        Resource.__init__(self, kwargs)
        if 'contained' in list(kwargs.keys()):
            setattr(self, 'contained', kwargs.get('contained'))
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Patient'] = TypeDefinition('Patient', (Patient,), ())


# RelatedPersons typically have a personal or non-healthcare-specific professional relationship to the patient. A RelatedPerson resource is primarily 
# used for attribution of information, since RelatedPersons are often a source of information about the patient. For keeping information about people 
# for contact purposes for a patient, use a Patient's Contact element. Some individuals may serve as both a Patient's Contact and a Related Person.
# Example RelatedPersons are:
#   A patient's wife or husband, a patient's relatives or friends, a neighbor bringing a patient to the hospital, 
#   the owner or trainer of a horse, a patient's attorney or guardian, a Guide Dog
class RelatedPerson(Jasonable):
    schema = {
        'identifier': {'type': 'list', 'schema': {'type': 'Identifier'}},
        'active': {'type': 'boolean'},
        'patient': {'type': 'Patient'},
        'name': {'type': 'list', 'schema': {'type': 'HumanName'}},
        'telecom': {'type': 'list', 'schema': {'type': 'ContactPoint'}},
        'relationship': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'gender': {'type': 'string', 'allowed': ['male', 'female', 'other', 'unknown']},
        'address': {'type': 'list', 'schema': {'type': 'Address'}},
        'communication': {'type': 'list', 'schema': {'type': 'Communication'}}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/R4/relatedperson.html#RelatedPerson'
    resourceType = 'RelatedPerson'

    def __init__(self, **kwargs):
        super(RelatedPerson, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['RelatedPerson'] = TypeDefinition('RelatedPerson', (RelatedPerson,), ())


# An interaction between a patient and healthcare provider(s) for the purpose of providing healthcare service(s) or assessing the health status of a patient.
# A patient encounter is further characterized by the setting in which it takes place. Amongst them are ambulatory, emergency, home health, inpatient and 
# virtual encounters. An Encounter encompasses the lifecycle from pre-admission, the actual encounter (for ambulatory encounters), and admission, stay and 
# discharge (for inpatient encounters). During the encounter the patient may move from practitioner to practitioner and location to location.

# class Encounter (Jasonable):
#   schema = {
#     'Identifier':{'type': 'Identifier'},
#     'Patient' :  {'type': 'Patient'},
#     'name':      {'type': 'HumanName'},  
#     'telecom':   {'type': 'ContactPoint'},
#     'relationship':{'type':'string','maxlength':20},
#     'gender':    {'type': 'string', 'allowed': ['male','female','other','unknown']},
#     'Address':   {'type': 'Address'},
#     'communication': {'type':'Communication'}
#     }
#   V = Validator(schema) 
# 
#   url = 'http://hl7.org/fhir/encounter.html#Encounter'
#   resourceType = 'Encounter'
# 
#   identifier : [{ Identifier }], #  Identifier(s) by which this encounter is known
#   status : <code>, #  R!  planned | arrived | triaged | in-progress | onleave | finished | cancelled +
#   
#   statusHistory : [{ #  List of past encounter statuses
#     status : <code>, #  R!  planned | arrived | triaged | in-progress | onleave | finished | cancelled +
#     period : { Period } #  R!  The time that the episode was in the specified status
#   }],
#  
#   class : { Coding }, #  R!  Classification of patient encounter
#  
#   classHistory : [{ #  List of past encounter classes
#     class : { Coding }, #  R!  inpatient | outpatient | ambulatory | emergency +
#     period : { Period } #  R!  The time that the episode was in the specified class
#   }],
#  
#   type : [{ CodeableConcept }], #  Specific type of encounter
#   serviceType : { CodeableConcept }, #  Specific type of service
#   priority : { CodeableConcept }, #  Indicates the urgency of the encounter
#   subject : { Reference(Patient|Group) }, #  The patient or group present at the encounter
#   episodeOfCare : [{ Reference(EpisodeOfCare) }], #  Episode(s) of care that this encounter should be recorded against
#   basedOn : [{ Reference(ServiceRequest) }], #  The ServiceRequest that initiated this encounter
#  
#   participant : [{ #  List of participants involved in the encounter
#     type : [{ CodeableConcept }], #  Role of participant in encounter
#     period : { Period }, #  Period of time during the encounter that the participant participated
#     individual : { Reference(Practitioner|PractitionerRole|RelatedPerson) } #  Persons involved in the encounter other than the patient
#   }],
# 
#   appointment : [{ Reference(Appointment) }], #  The appointment that scheduled this encounter
#   period : { Period }, #  The start and end time of the encounter
#   length : { Duration }, #  Quantity of time the encounter lasted (less time absent)
#   reasonCode : [{ CodeableConcept }], #  Coded reason the encounter takes place
#   reasonReference : [{ Reference(Condition|Procedure|Observation|ImmunizationRecommendation) }], #  Reason the encounter takes place (reference)
# 
#   diagnosis : [{ #  The list of diagnosis relevant to this encounter
#     condition : { Reference(Condition|Procedure) }, #  R!  The diagnosis or procedure relevant to the encounter
#     use : { CodeableConcept }, #  Role that this diagnosis has within the encounter (e.g. admission, billing, discharge)
#     rank : <positiveInt> #  Ranking of the diagnosis (for each role type)
#   }],
# 
#   account : [{ Reference(Account) }], #  The set of accounts that may be used for billing for this Encounter
# 
#   hospitalization : { #  Details about the admission to a healthcare service
#     preAdmissionIdentifier : { Identifier }, #  Pre-admission identifier
#     origin : { Reference(Location|Organization) }, #  The location/organization from which the patient came before admission
#     admitSource : { CodeableConcept }, #  From where patient was admitted (physician referral, transfer)
#     reAdmission : { CodeableConcept }, #  The type of hospital re-admission that has occurred (if any). If the value is absent, then this is not identified as a readmission
#     dietPreference : [{ CodeableConcept }], #  Diet preferences reported by the patient
#     specialCourtesy : [{ CodeableConcept }], #  Special courtesies (VIP, board member)
#     specialArrangement : [{ CodeableConcept }], #  Wheelchair, translator, stretcher, etc.
#     destination : { Reference(Location|Organization) }, #  Location/organization to which the patient is discharged
#     dischargeDisposition : { CodeableConcept } #  Category or kind of location after discharge
#   },
# 
#   location : [{ #  List of locations where the patient has been
#     location : { Reference(Location) }, #  R!  Location the encounter takes place
#     status : <code>, #  planned | active | reserved | completed
#     physicalType : { CodeableConcept }, #  The physical type of the location (usually the level in the location hierachy - bed room ward etc.)
#     period : { Period } #  Time period during which the patient was present at the location
#   }],
# 
#   serviceProvider : { Reference(Organization) }, #  The organization (facility) responsible for this encounter
#   partOf : { Reference(Encounter) } #  Another Encounter this encounter is part of
# }

# Members of the CareTeam
class Participant(Jasonable):
    schema = {
        'role': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'member': {'type': 'Reference', 'schema': {'oneof_schema': [
            {'type': 'Practitioner'},
            {'type': 'PractitionerRole'},
            {'type': 'RelatedPerson'},
            {'type': 'Patient'},
            {'type': 'Organization'},
            {'type': 'CareTeam'},
        ]}},  # (Practitioner|PractitionerRole|RelatedPerson|Patient|Organization|CareTeam
        'onBehalfOf': {'type': 'Reference'},
        'period': {'type': 'Period'},
    }
    V = Validator(schema)
    url = 'https://hl7.org/fhir/R4/careteam-definitions.html#CareTeam.participant'
    resourceType = 'Participant'

    def __init__(self, **kwargs):
        super(Participant, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Participant'] = TypeDefinition('Participant', (Participant,), ())


class Annotation(Jasonable):
    schema = {
        'authorReference': {'type': 'Reference', 'schema': {'oneof_schema': [
            {'type': 'Practitioner'},
            {'type': 'Patient'},
            {'type': 'RelatedPerson'},
            {'type': 'Organization'},
        ]}},
        'authorString': {'type': 'string'},
        'time': {'type': 'datetime.time'},
        'text': {'type': 'string'}
    }
    V = Validator(schema)
    url = 'https://hl7.org/fhir/R4/datatypes.html#Annotation'
    resourceType = 'Annotation'

    def __init__(self, **kwargs):
        super(Annotation, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['Annotation'] = TypeDefinition('Annotation', (Annotation,), ())


# The CareTeam includes all the people, teams, and organizations who plan to participate in the coordination and delivery of care for a single patient
# or a group (such as a married couple in therapy or a support group). CareTeam can also be organizationally assigned without a subject in context, 
# such as a code blue team or emergency response team. This is not limited to practitioners, but may include other caregivers such as family members, 
# guardians, the patient themself, or others. The Care Team, depending on where used, may include care team members specific to a particular care plan, 
# an episode, an encounter, or may reflect all known team members across these perspectives. An individual's CareTeam can be dynamic over time, such 
# that there can be transience of team members, such as a rehabilitation team.
class CareTeam(Jasonable):
    schema = {
        'identifier': {'type': 'list', 'schema': {'type': 'Identifier'}},
        'status': {'type': 'string', 'allowed': ['proposed', 'active', 'suspended', 'inactive', 'entered-in-error']},
        'category': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'name': {'type': 'string'},
        'subject': {'type': 'Reference'},  # 'oneof_schema':[{'type':'Practitioner'},{'type':'PractitionerRole'}]},
        'period': {'type': 'Period'},
        'participant': {'type': 'list', 'schema': {'type': 'Participant'}},
        'reasonCode': {'type': 'list', 'schema': {'type': 'CodeableConcept'}},
        'reasonReference': {'type': 'list', 'schema': {'type': 'Reference', 'schema': {'type': 'Condition'}}},
        'managingOrganization': {'type': 'list', 'schema': {'type': 'Reference', 'schema': {'type': 'Organization'}}},
        'telecom': {'type': 'list', 'schema': {'type': 'ContactPoint'}},
        'note': {'type': 'list', 'schema': {'type': 'Annotation'}}
    }
    V = Validator(schema)
    url = 'http://hl7.org/fhir/careteam.html'
    resourceType = 'CareTeam'

    def __init__(self, **kwargs):
        super(CareTeam, self).__init__(kwargs)
        if self.V.validate(self.data) == False:
            raise BadDataVal(self.V.errors)


Validator.types_mapping['CareTeam'] = TypeDefinition('CareTeam', (CareTeam,), ())