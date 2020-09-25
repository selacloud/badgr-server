import os
import boto3
import json
import socket
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

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
    new_settings = []
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
settings={'ENGINE':'engine',
        'NAME':'name',
        'USER':'user',
        'PASSWORD':'password',
        'HOST':'host',
        'PORT':'port',
        'BACKEND':'backend',
        'LOCATION':'location',
        'KEY_FUNCTION':'key_function',
        'DEFAULT_FROM_EMAIL':'default_from_email',
        'EMAIL_BACKEND':'email_backend',
        'ALLOWED_HOSTS':'allowed_hosts',
        'SECRET_KEY':'secret_key',
        'UNSUBSCRIBE_KEY':'unsub_key'}
    
    # Creating a dictionary to hold the values of the variables
new_settings = []
env_dict = {}
for x in env_vars:
    if x in settings:
        env_dict[x] = settings[x]
        new_settings.append(x + ":" + settings[x])
    elif x in os.environ:
        env_dict[x] = settings[x]
        new_settings.append(x + ":" + settings[x])
    else:
        pass

original = 'tester.py'
new_local = 'temp_settings'

with open(original, 'r') as old_file:
    with open(new_local, 'w') as new_file:
        for lines in old_file:
            found = False
            #lines.strip()
            print(lines)
            for x in env_vars:
                if x in lines:
                    found = True
                    print('found : '+x)
                    new_file.write(lines.replace(x, "'"+x+"':'"+env_dict[x]+"'"))
                    break
            if found == False:
                new_file.write(lines)
            else:
                pass
        os.remove(original)
        os.rename(new_local, original)
                
                    
                
            # for x in new_settings:
            #     y = x.split(':')
            #     z = y[0]
            #     if z in lines:
            #         print('Found: '+z)
            #         new_file.write("'"+z+"':"+"'"+env_dict[z]+"'\n")
            #     else:
            #         new_file.write(lines)

fin = open('tester.py' ,'r')
new_file = open('new_settings.py', 'wt')
fdata = fin.read()
keys = keydict.values()
for lines in fdata:
    for key in keys:
        if str(key) in line:
            print(line)
            print(key)
            #line.replace(key, "'"+key+"':'"+str(value)+"'")
        else:
            #print('not found')
            #new_file.write(line)
            pass
split_settings = settings_data.split("\n")
keys = []
for x in keydict:
    keys.append[x]
    
with open('tester.py', 'rt+') as old_file:
    with open('new_file', 'wt') as new_file:
        for lines in old_file:
            for x in keys:
                if x in lines:
                    print('found key : ' + key)
                    print(lines.replace(key, key+"':'"+str(value)+"'\n"))
                    #new_file.append("'"+key+"':'"+str(value)+"'\n")
                    pass
                else:
                    print(lines)
                    #new_file.append(lines)
                    pass
        old_file.write()
        new_file.write()
                
fh, abs_path = mkstemp()
with open(fh,'wt') as new_file:
    with open('tester.py','rt') as old_file:
        for line in old_file:
            for key, value in keydict.items():
                if key in line:
                    new_file.write("'"+key+"':'"+str(value)+"'")
                else:
                    new_file.write(line)
shutil.move(abs_path, os.getcwd())
                                   
    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)
        
    for line in new_settings:
        #print('Checking ' + line)
        if db_engine in line:
            x = line.split("=")[1].strip()
            new_tendenci_variables.append("DATABASES['default']['HOST'] = '" + x + "'")
        elif 'db_port=' in line:
            x = line.split("=")[1].strip()
            new_tendenci_variables.append("DATABASES['default']['PORT'] = " + x)
        elif 'db_user=' in line:
            x = line.split("=")[1].strip()
            new_tendenci_variables.append("DATABASES['default']['USER'] = '" + x + "'")
        elif 'db_password=' in line:
            x = line.split("=")[1].strip()
            new_tendenci_variables.append("DATABASES['default']['PASSWORD'] = '" + x + "'")
        elif 'db_name=' in line:
            x = line.split("=")[1].strip()
            new_tendenci_variables.append("DATABASES['default']['NAME'] = '" + x + "'")
        elif 'cache_host=' in line:
            x = line.split("=")[1].strip()
            new_tendenci_variables.append("CACHES['default']['LOCATION'] = '" + os.environ['ec_host'] + "'")
        elif 'ec_host=' in line:
            x = line.split("=")[1].strip()
            new_tendenci_variables.append("CACHES['default']['LOCATION'] = '" + os.environ['ec_host'] + "'")
        elif 'SECRET_KEY' in line:
            x = settings['SECRET_KEY']
            new_tendenci_variables.append("SECRET_KEY = '" + x + "'")
        elif 'SITE_SETTINGS_KEY=' in line:
            x = settings['SITE_SETTINGS_KEY']
            new_tendenci_variables.append("SITE_SETTINGS_KEY = '" + x + "'")
        elif 'ALLOWED_HOSTS=' in line:
            x = line.split("=")[1].strip()
            new_tendenci_variables.append("ALLOWED_HOSTS = ['" + socket.gethostname() + "','" + socket.gethostbyname(socket.gethostname()) + "','" + os.environ['site_urls'] + "','lb." + os.environ['site_urls'] + "']")
        elif 'time_zone=' in line:
            new_tendenci_variables.append("TIME_ZONE = 'UTC'")
        else:
            pass


    
    
    
    
    # Checking for debug and disable_template_cache settings and enabling them
    # Opening the original settings file and splitting it to a list so we can append
    # new settings to the file before the required ending of the file.
    settings_file = open('/var/www/mysite/conf/settings.py', 'rt')
    settings_data = settings_file.read()
    if "debug" in os.environ:
        settings_data = settings_data.replace("#DEBUG = True", "DEBUG = True")
        print("Enabling debug...")
    if "disable_template_cache" in os.environ:
        settings_data = settings_data.replace("#DEBUG = True", "#DEBUG = True\n\ndisable_template_cache()")
        print('Disabling template cache...')
    split_settings = settings_data.split("\n")
    settings_file.close()

    # Inserting new settings before required end of file
    for x in new_tendenci_variables:
        #print("Adding " + x + " to settings file...")
        split_settings.insert(-7, x)

    separator = "\n"
    new_data = separator.join(split_settings)

    # Deleting all text from the original file and re-writing with new settings
    fin = open('/var/www/mysite/conf/settings.py', 'wt')
    fin.truncate(0)
    fin.write(new_data)
    fin.close()
    print("Settings updated.")

settings_source()



