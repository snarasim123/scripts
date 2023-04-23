from datetime import datetime, MINYEAR


def TypeDefinition(name, type, no):
    return type[0]


# set specific types
d = datetime(MINYEAR, 1, 1)
DateTimeType = type(d)


class BadDataVal(Exception):
    print(Exception)


class Validator:
    SKIP = ['extension']
    DISCRETE_TYPES = ['string', 'float', 'integer', 'boolean', 'list', 'dict']
    types_mapping = {'string': str, 'float': float, 'integer': int, 'boolean': bool, 'list': list, 'dict': dict,
                     'datetime.datetime': DateTimeType}

    def __init__(self, schema):

        self.schema = schema
        self.errors = ''

    def validate(self, data):

        for key in data:
            if key in self.SKIP:
                continue
            val = data[key]

            if self.schema[key]['type'] not in self.DISCRETE_TYPES:
                if val == None:
                    continue

            if self.schema[key]['type'] in self.DISCRETE_TYPES:  # classes are nullable, only discrete types are not
                try:
                    if val == None and self.schema[key]['nullable']:
                        continue
                except:
                    self.errors = str(key) + ' is None, but not nullable.'
                    return False

            if self.schema[key]['type'] == 'Reference':
                return True  # TODO validate type of reference

            textType = self.schema[key]['type']
            dataType = self.types_mapping[textType]

            if str(type(val)) != str(dataType):
                if textType == 'string':
                    pass
                else:
                    self.errors = key + ': ' + str(val) + ' not of type (1) ' + str(textType)
                    return False

            if textType == 'list':
                if 'schema' in self.schema[key]:
                    for value in val:
                        if 'oneof_schema' not in self.schema[key]['schema'].keys():
                            textType = self.schema[key]['schema']['type']
                            dataType = self.types_mapping[textType]
                            if type(value) != dataType:
                                if textType == 'string':
                                    pass
                                else:
                                    self.errors = str(value) + ' not of type (2) ' + textType + ', but of type ' + str(
                                        type(value))
                                    return False

            elif textType == 'string':
                if 'allowed' in self.schema[key]:
                    if val not in self.schema[key]['allowed']:
                        self.errors = val + ' not one of ' + str(self.schema[key]['allowed'])
                        return False

                if 'maxlength' in self.schema[key]:
                    if len(val) > self.schema[key]['maxlength']:
                        self.errors = 'length of ' + val + 'greater than ' + str(self.schema[key]['maxlength'])
                        return False

            elif textType == 'float' or textType == 'integer':
                if 'min' in self.schema[key]:
                    if val < self.schema[key]['min']:
                        self.errors = 'length of ' + val + 'less than ' + str(self.schema[key]['min'])
                        return False
                if 'max' in self.schema[key]:
                    if val > self.schema[key]['max']:
                        self.errors = 'length of ' + val + 'greater than ' + str(self.schema[key]['max'])
                        return False

            if 'oneof_schema' in self.schema[key]:
                found = False
                for Type in self.schema[key]['oneof_schema']:
                    if type(val) == Type['type']:
                        found = True
                        break
                if not found:
                    self.errors = val + ' not one of ' + self.schema[key]['oneof_schema']
                    return False

        return True
