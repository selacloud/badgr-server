import os
import boto3
import json
import socket

def settings_source():
    if "secret_id" in os.environ:
        get_secret()
    else:
        write_settings(os.environ)

def get_secret():
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager'
    )
    # try:
    secret = client.get_secret_value(
        SecretId=os.environ['secret_id']
        )
    secret_value = json.loads(secret['SecretString'])
    print("Secret Retrieved Successfully")
    with open('/etc/environment', 'r') as file:
        environment = file.read()
    environment = environment + "\nENGINE=" + secret_value['ENGINE']
    environment = environment + "\nNAME=" + secret_value['NAME']
    environment = environment + "\nUSER=" + secret_value['USER']
    environment = environment + "\nPASSWORD=" + secret_value['PASSWORD']
    environment = environment + "\nHOST=" + secret_value['HOST']
    environment = environment + "\nPORT=" + secret_value['PORT']
    environment = environment + "\nBACKEND=" + secret_value['BACKEND']
    environment = environemnt + "\nLOCATION=" + secret_value['LOCATION']
    environment = environment + "\nKEY_FUNCITON=" + secret_value['KEY_FUNCTION']
        if "mysql" in secret_value:
            environment = environment + "\nSET character set connection=utf8mb3, collation_connection=utf8_unicode_ci"
    with open('/etc/environment', 'w') as file:
        file.write(environment)
    write_settings(secret_value)
    
def write_settings(settings):

    env_vars=['ENGINE',
            'NAME',
            'USER',
            'PASSWORD',
            'HOST',
            'PORT',
            'BACKEND',
            'LOCATION',
            'KEY_FUNCTION',
            'DEFAULT_FROM_EMAIL',
            'EMAIL_BACKEND',
            'ALLOWED_HOSTS',
            'SECRET_KEY',
            'UNSUBSCRIBE_KEY']

    # Creating dictionary to hold enviroment variables
    env_dict = {}
    for x in env_vars:
        if x in settings:
            env_dict[x] = settings[x]
        elif x in os.environ:
            env_dict[x] = settings[x]
        else:
            pass

    original = '.docker/etc/settings_local.dev.py'
    new_local = '.docker/etc/settings/temp_settings'

    # Creating a new file, checking for variables in the line
    # If variables are found, apply the variables to the line
    # and write to the new file, else write the original line
    # then delete the old file, rename the new file to the old
    
    with open(original, 'r') as old_file:
        with open(new_local, 'w') as new_file:
            for lines in old_file:
                found = False
                #print(lines)
                for x in env_vars:
                    if x in lines:
                        found = True
                        print('Found : '+x)
                        new_file.write(lines.replace(x, "'"+x+"':'"+env_dict[x]+"'"))
                        break
                if found == False:
                    new_file.write(lines)
                else:
                    pass
            os.remove(original)
            os.rename(new_local, original)
    print("Settings updated.")

settings_source()

