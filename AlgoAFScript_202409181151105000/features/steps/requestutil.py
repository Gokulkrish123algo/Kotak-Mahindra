# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-timeout
import base64
import json
import requests



def set_api_endpoint(context, text):
    context.api_url = text
    context.eachStepMessage.append(context.api_url)


def set_apimethod(context, text):
    context.method_type = text
    context.eachStepMessage.append(context.method_type)


def set_requestpayload(context, text):
    context.request_payload = text
    context.eachStepMessage.append(context.request_payload)


def set_api_headers(context, header):
    my_dict = {}
    input_parameters = str(header).split(',')
    for parameter in input_parameters:
        header_text = parameter.split(':')
        if len(header_text) > 1:
            header_value = str(header_text[1])
            if '@colon' in str(header_value):
                header_value = header_value.replace('@colon', ':')
            my_dict[header_text[0]] = header_value
    context.api_header = my_dict
    context.eachStepMessage.append(str(context.api_header))


def set_api_response_dictionary(context, text, key):
    split_text = text.split(',')
    data = json.loads(context.api_response)
    for i in range(len(split_text)):
        value = ""
        if '.' in split_text[i]:
            splitdot = split_text[i].split(".")
            if len(splitdot) == 2:
                value = data[splitdot[0]][splitdot[1]]
            elif len(splitdot) == 3:
                value = data[splitdot[0]][splitdot[1]][splitdot[2]]
            elif len(splitdot) == 4:
                value = data[splitdot[0]][splitdot[1]][splitdot[2]][splitdot[3]]
        else:
            value = data[split_text[i]]
        dict_key = key + "." + split_text[i]
        context.dict_api_response[dict_key] = value
        context.eachStepMessage.append("key: " + str(dict_key) + ",value: " + str(value))


def get_api_response_value(context, text):
    for key, value in context.dict_api_response.items():
        searchstring = "@" + key
        if searchstring in text:
            text = text.replace(searchstring, value)
    return text


def execute_api_and_verify_response(context, execute_api_and_verify_response):
    verified = False
    apiurl, methodtype, requestparameter, apiheaders = None, None, None, None
    oauth2, basicauth = None, None
    if context.api_url is not None:
        apiurl = context.api_url
    if context.method_type is not None:
        methodtype = context.method_type
    if context.request_payload is not None:
        requestparameter = context.request_payload
    if context.api_header is not None:
        apiheaders = context.api_header
    if apiheaders is not None and 'IMAGE / PNG' in apiheaders and methodtype.upper() == 'GET':
        try:
            response = requests.request('GET', apiurl, headers=apiheaders)
            res_code = response.status_code
            if res_code in (200, 201, 202):
                verified = True
                print('Refer to the attached image to check output.')
            image = response.content
            base64_string = base64.b64encode(image).decode('utf-8')
            print(base64_string)
        except Exception as e:
            print('Error------------', e)
            verified = False
        return verified
    else:
        headers = {}
        if basicauth is not None:
            basic_auth_split = basicauth.split(',')
            auth = (basic_auth_split[0], basic_auth_split[1])
            print(auth)
            headers['Authorization'] = 'Basic ' + (basic_auth_split[0] + ':' + basic_auth_split[1]).encode(
                'base64').rstrip()
        if str(methodtype.lower()) == 'post':
            response = requests.post(apiurl, data=requestparameter, headers=apiheaders)
        elif str(methodtype.lower()) == 'get':
            response = requests.get(apiurl, headers=apiheaders)
        elif str(methodtype.lower()) == 'put':
            response = requests.put(apiurl, data=requestparameter, headers=apiheaders)
        elif str(methodtype.lower()) == 'delete':
            response = requests.delete(apiurl, headers=apiheaders)
        numeric_status_code = response.status_code
        allheaders = str(response.headers)
        context.api_all_headers = allheaders
        context.api_response = response.text
        context.eachStepMessage.append(context.api_response)
        if execute_api_and_verify_response.upper() == 'VERIFY_NEGATIVE'.upper() and numeric_status_code in [400, 500,
                                                                                                            401, 415,
                                                                                                            000]:
            context.eachStepMessage.append(str(numeric_status_code))
            verified = True
        elif numeric_status_code in [201, 200, 202, 204]:
            context.eachStepMessage.append(str(numeric_status_code))
            verified = True
        else:
            print('Unsuccessful response. Status code:', numeric_status_code)
            verified = False
        return verified
