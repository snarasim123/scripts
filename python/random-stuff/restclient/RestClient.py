from typing import Any

import csv
import json
import requests
import time
import concurrent.futures
import base64
import timeit
import datetime

num_threads = 10
filename = "/Users/snarasimhan/Code/python/restclient/test2.csv"
output_file = ""
# TODO remove after debugging
# Debugging only, remove for real run
fake_api = True


def get_token():
    url: str = 'https://login.thrio.com/provider/token-with-authorities'
    creds: str = base64.b64encode(b'api2@catasys.com:Password2')
    # api2@catasys.com
    # api2@stayontrak.com
    response = requests.get(url,
                            headers={'Content-Type': 'application/json',
                                     'accept': 'application/json',
                                     'Authorization': 'Basic {0}'.format(creds.decode("utf-8"))})
    # TODO remove after debugging
    # if fake_api:
    #     return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJjYjhhODdjZS0wNjMxLTRjZWItOTZmMC1jZWZkMTM3MDJiZWIiLCJpc3MiOiJodHRwczovL3d3dy5obmRsYmFyLmNvbSIsImlhdCI6MTU4OTkyNjM1OCwiYXVkIjoiaG5kbGJhci5jb20iLCJzdWIiOiJhcGkyQGNhdGFzeXMuY29tIiwidGVuYW50SWQiOiJjYXRhc3lzIiwidXNlcklkIjoiNWRmM2MwYWM1NjMyNzYwMDAxNjBmYjkxIiwidXNlcm5hbWUiOiJhcGkyQGNhdGFzeXMuY29tIiwiYXV0aG9yaXRpZXMiOlsiW3R5cGVdOlsqXTpbKl0iLCJbdHlwZS5jbHVzdGVyXTpbXTpbXSIsIlt0eXBlLmNvbnRhY3RdOltjb250YWN0XTpbc2VhcmNoLCB2aWV3LCB2aWV3LW1pbmUsIHNob3ddIiwiW3R5cGUuemlwY29kZSwgdHlwZS5hcmVhY29kZV06W3ppcGNvZGUsIGFyZWFjb2RlXTpbdmlldywgc2VhcmNoXSIsIlt0eXBlLnRlbmFudF06W3RlbmFudF06W3ZpZXctbWluZSwgbG9jYWxpemUsIHVwZGF0ZS1taW5lXSIsIlt0eXBlLndvcmtpdGVtXTpbd29ya2l0ZW1dOlt2aWV3LCB2aWV3LW1pbmUsIHNlYXJjaCwgZXh0ZW5zaW9uLCBvdXRib3VuZCwgc2VhcmNoLWFsbCwgdXBkYXRlLW1pbmVdIiwiW3R5cGUuc2hhcmVkc2VydmljZV06W106W10iLCJbdHlwZS5idXNpbmVzc2FjdGl2aXR5c3VtbWFyeSwgdHlwZS5idXNpbmVzc2FjdGl2aXR5c3VtbWFyeWNoYW5uZWxdOltidXNpbmVzc2FjdGl2aXR5c3VtbWFyeWNoYW5uZWwsIGJ1c2luZXNzYWN0aXZpdHlzdW1tYXJ5XTpbdmlldywgc2VhcmNoXSIsIlt1aV06WypdOlsqXSJdLCJleHAiOjE1ODk5ODM5NTh9.wNVF7vyeUjIcRf_9JDvJMyV2X0iJLzRHKtvsM4eTYrI'
    api_token = response.json()["token"]
    return api_token


def get_lines(input_file, line_from, line_to):
    phone_num_list = []
    rehab_id_list = []
    return_dict = {}
    file = open(input_file)
    total_lines = len(file.readlines())
    file.close()

    if line_to < line_from:
        return phone_num_list, rehab_id_list, return_dict, -1
    if line_from <= 0 or line_to <= 0:
        return phone_num_list, rehab_id_list, return_dict, -1
    if total_lines < line_from:
        return phone_num_list, rehab_id_list, return_dict, -1

    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 1
        phone_index = 9
        rehabid_index = 40

        # column names from csv
        # First Name,Last Name,Date Added,Mobile Phone,
        # Carrier,Mobile Status,Mobile Status Reason,
        # Secure Messaging Status,Push Notification Status,
        # ENROLLED DATE,CARE COACH NAME,STATUS,erehab_id
        for row in csv_reader:
            if line_from <= line_count <= line_to:
                digits = len(str(row[phone_index]))
                if digits < 9:
                    print("Phone number is not a 9 digit number -> {0} ".format(row))
                    continue
                phone_num = '+' + row[phone_index]
                phone_num_list.append(phone_num)
                rehab_id_list.append(row[rehabid_index])
                return_dict[row[rehabid_index]] = phone_num
            if line_count > line_to:
                break
            line_count += 1
    return phone_num_list, rehab_id_list, return_dict, 0


def file_length(input_file):
    file = open(input_file)
    total_lines: int = len(file.readlines())
    file.close()
    return total_lines


def do_thrio_post(phone_no, api_token):
    post_url_base = 'https://chelsea.thrio.com/'
    thrio_post_url = "{0}data/api/types/commconsent".format(post_url_base)
    address = "{\"address\" : \""
    commtype = "\",\"commType\": 33"
    reason = ",\"reason\" : \"\""
    contact_id = ",\"contactId\" : \"\""
    campaign_id = ",\"campaignId\" : \"\"}"
    payload1: str = address + phone_no + commtype + reason + contact_id + campaign_id
    headers = {
        'Content-Type': 'application/json',
        'Authorization': '{0}'.format(api_token)
    }
    file = open(output_file, 'a')

    if fake_api:
        time.sleep(1)
        file.write(
            "\nFake Posted phone number to thrio -> {0} , Payload -> {1}, Header -> {2}  , Url -> {3}".format(phone_no,
                                                                                                              payload1,
                                                                                                              headers,
                                                                                                              thrio_post_url))
        file.close()
        return None

    try:
        response = requests.request("POST", thrio_post_url, headers=headers, json=json.loads(payload1))
        file.write(
            "\nThrio Post 1 phone number -> {0} , Payload -> {1}, Header -> {2}  , Url -> {3}".format(phone_no,
                                                                                                      payload1,
                                                                                                      headers,
                                                                                                      thrio_post_url))
        file.write(
            "\nThrio Post 2 HTTP status code -> {0} , Response Json -> {1}".format(response.status_code,
                                                                                   response.text.encode(
                                                                                       'utf8')))
    except Exception as e:
        file.write("\nFailed -> exception msg: " + str(e))
        file.write(
            "\n*** Exception -> {0} , Payload -> {1}, Header -> {2}  , Url -> {3}".format(phone_no, payload1, headers,
                                                                                          thrio_post_url))
    file.close()

    return process_http_status(thrio_post_url, response)


def do_dfappl_post(patient_phoneno, patient_id, api_token):
    devbase_url = 'https://dev-westus2-dfcore-gateway-service.azurewebsites.net/api/v1/patientinfo/smsconsent'
    stagebase_url = 'https://stage-westus2-dfappl-call-center-api-service.ontrak2-staging.appserviceenvironment.net/api/v1/patientinfo/smsconsent'
    prodbase_url = 'https://prod-westus2-dfappl-call-center-api-service.ontrak2.appserviceenvironment.net/api/v1/patientinfo/smsconsent'
    post_url_base = prodbase_url
    open_parenth = "{"
    close_parenth = "}"
    erehab_id = "\"erehabId\" : \""
    phone_number = "\"phoneNumber\": \""
    sms_consent = "\"smsConsent\" : \"Opt-In\""
    payload1: str = open_parenth + erehab_id + patient_id + "\"," + phone_number + patient_phoneno + "\"," + sms_consent + close_parenth
    headers = {
        'Content-Type': 'application/json',
    }
    file = open(output_file, 'a')
    if fake_api:
        time.sleep(1)
        file.write("\nFake Posted phone number to dfApl api -> {0} , Payload -> {1}, Header -> {2} , Url -> {3} "
                   .format(patient_phoneno, payload1, headers, post_url_base))
        file.close()
        return None

    try:
        response = requests.request("POST", post_url_base, headers=headers, json=json.loads(payload1))
        file.write(
            "\nDFCore Post  1 phone number -> {0} , Payload -> {1}, Header -> {2} , Url -> {3}".format(patient_phoneno,
                                                                                                       payload1,
                                                                                                       headers,
                                                                                                       post_url_base))
        file.write("\nDFCore Post 2 HTTP status code -> {0} , Response Json -> {1}".format(
            response.status_code,
            response.text.encode('utf8')))
    except Exception as e:
        file.write("\nFailed -> exception msg: " + str(e))
        file.write(
            "\n*** Exception  -> {0} , Payload -> {1}, Header -> {2} , Url -> {3}".format(patient_phoneno, payload1,
                                                                                          headers,
                                                                                          post_url_base))
    file.close()
    return process_http_status(thrio_post_url, response)


def process_http_status(post_url, response):
    if response.status_code > 499:
        print("[!] [{0}] Server Error".format(response.status_code))
        return None
    elif response.status_code == 404:
        print("[!] [{0}] URL not found: [{1}]".format(response.status_code, post_url))
        return None
    elif response.status_code == 401:
        print("[!] [{0}] Authentication Failed".format(response.status_code))
        return None
    elif response.status_code > 399:
        print("[!] [{0}] Bad Request".format(response.status_code))
        print(response.content)
        return None
    elif response.status_code > 299:
        print("[!] [{0}] Unexpected redirect.".format(response.status_code))
        return None
    elif response.status_code == 201 or response.status_code == 200:
        post_response = json.loads(response.content)
        return post_response
    else:
        print("[?] Unexpected Error: [HTTP {0}]: Content: {1}".format(response.status_code, response.content))
        return None


def process(input_file, from_line, to_line, api_token):
    print('Processing lines {0} to {1}'.format(from_line, to_line))
    phone_number, rehab_id_list, return_dict, error = get_lines(input_file, from_line, to_line)

    total_threads = to_line - from_line + 1

    with concurrent.futures.ThreadPoolExecutor(max_workers=total_threads) as executor:
        for index in range(total_threads):
            executor.submit(do_thrio_post, return_dict[rehab_id_list[index]], api_token)
            executor.submit(do_dfappl_post, return_dict[rehab_id_list[index]], rehab_id_list[index], api_token)
    return


def main():
    start_time = datetime.datetime.now().strftime("%H:%M:%S")
    global output_file
    output_file = "./output-" + str(start_time) + ".log"
    file = open(output_file, 'w')
    file.write("\nStarting run at {0}".format(start_time))
    file.close()
    file_size = file_length(filename)
    if file_size == 0:
        return

    start = timeit.default_timer()
    # skip the first line with headers
    current_line = 2
    to_line = 2

    if to_line >= file_size:
        to_line = file_size
    api_token = get_token()
    while current_line <= file_size:
        process(filename, current_line, to_line, api_token)
        current_line = to_line + 1
        to_line = current_line + (num_threads - 1)
        if to_line >= file_size:
            to_line = file_size
    end = timeit.default_timer()
    file = open(output_file, 'a')
    # file.write("Starting run at {0}\n".format(start_time))

    file.write('\nProcessed {0} lines of {1} total lines from file {2}.'.format(current_line - 1, file_size, filename))

    total_time = end - start
    file.write("\nTime at start = {0} ".format(start_time))
    file.write("\nTime at end = {0} ".format(datetime.datetime.now().strftime("%H:%M:%S")))
    file.write(
        '\nTook {0:0.2f} minutes/{1:0.2f} seconds using {2} threads.'.format((total_time / 60), total_time,
                                                                             num_threads))

    file.close()


if __name__ == "__main__":
    main()
