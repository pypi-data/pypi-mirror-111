#!/usr/bin/env python3
'''
 ss.py - A script to get secrets from a Thycotic Secret Server system.

 Originally from :- https://infotechbrain.com/2018/09/thycotic-python-api/

'''

import logging
import json
import getpass
import getopt
import sys
import os
from collections import namedtuple
import requests

SECRETSERVERURL = 'secretserver.eng.citrite.net'
SECRETSERVERAPPPATH = ''
DEFAULTDOMAIN = 'CITRITE'
# Just use one of the default templates set up in secret server.
# If you want to identify a custom one or other default and use it then you
# may need to change some of the data structure.
DEFAULTTEMPLATEID = '2'

log = logging.getLogger("secretserver")

def usage():
    ''' Display the usage for the program '''
    print(" ./ss.py -i 1234 ( retrieve secret id 1234 )")
    print(" ./ss.py -s 'string' (search for string)")
    print(" ./ss.py -v (verbose output/debug)")
    print(" ./ss.py (prompt for options)")
    print(" ./ss.py -d domain (specify auth domain - defaults to CITRITE)")
    print(" ./ss.py -t <token> (use existing auth token instead of creds)")
    print(" ./ss.py -g (get token) ** THIS TOKEN IS EQUIVILENT TO YOUR USER CREDENTIALS **")
    print(" ")
    print(" --search [string]")
    print(" --add [name of secret to add]")
    print(" --download [name for the file downloaded]")
    print(" --folder [folder ID for add]")
    print(" --secretusername [secret username for add]")
    print(" --secretpassword [secret password for add]")
    print(" --tokenfile [file] - use with -g to create a file, then with -t ")
    print("")
    print("Do not allow anyone to access a stored token!")

class Secure:
    ''' Class to connect to Secret Server provide a mechanism to auth, get
    a token and then allow searching for secrets/passwords.

    Initialisation takes - string: user, string: password, string: domain
    '''

    #server fully qualified domain name
    serverFQDN = SECRETSERVERURL
    # Where your trycotic server application is installed
    appPath = SECRETSERVERAPPPATH

    def set_token(self, token):
        ''' set the token from something that is passed into us '''
        self.token = token

    def get_token(self):
        ''' get a token from the object and return it as a string '''
        return self.token

    def __init__(self, username=None, password=None, domain=DEFAULTDOMAIN):

        # Read environment variables for Jenkins (SECRETSERVER_CREDS_XXXX) or secretserver_lookup_plugin (SSXXXX)
        username = os.environ.get('SECRETSERVER_CREDS_USR') or os.environ.get('SSUSER') or username
        password = os.environ.get('SECRETSERVER_CREDS_PSW') or os.environ.get('SSPASSWORD') or password
        domain = os.environ.get('SSDOMAIN') or domain
        
        self.token = None
        self.secretpw = None
        self.allsecrets = None
        
        if username and password:
            self.set_auth(username, password, domain)


    def set_auth(self, username, password, domain):
        ''' Auth againts the Secret Server host '''

        self.username = username
        self.password = password
        self.domain = domain

        url = "https://{}{}/oauth2/token".format(self.serverFQDN, self.appPath)

        payload = {'username': self.username,
                   'password': self.password,
                   'domain': self.domain,
                   'grant_type': 'password'

                  }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            # Request and resubmit with VIP token
            if response.json()['error'] == 'RADIUS Authentication Failed.':
                headers['OTP'] = getpass.getpass("Secret Server OTP: ")

                response = requests.request("POST", url, data=payload, headers=headers)
            else:
                raise error

        self.token = json.loads(response.text)['access_token']

    def get_secret_by_id(self, secret_id):
        ''' Search for a Secret by ID and display the password '''
        url = "https://{}{}/api/v1/secrets/{}".format(self.serverFQDN, self.appPath, secret_id)
        headers = {
            'authorization': "Bearer {}".format(self.token),
            'Accept': 'application/json'
        }
        log.debug(self.token)

        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()

        secret = json.loads(response.text)
        fields = {str.lower(x['fieldName']).replace(" ", "_"): x['itemValue'] for x in secret['items']}
        return namedtuple('Secret', sorted(fields))(**fields)


    def get_search_secrets(self, search_text):
        ''' Search secrets via a search string rather than by a specific ID '''
        search_filter = '?filter.includeRestricted=true&' + \
                         'filter.includeSubFolders=true&' + \
                         'filter.searchtext={}'.format(search_text)

        url = "https://{}{}/api/v1/secrets{}".format(self.serverFQDN, self.appPath, search_filter)
        headers = {
            'authorization': "Bearer {}".format(self.token),
            'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers)

        self.allsecrets = json.loads(response.text)

        return self.allsecrets


    def download_secret(self, secret_id, filename=None, field="cert"):

        #''' Download a file stored within a secret '''
        url = "https://{}{}/api/v1/secrets/{}/fields/{}".format(self.serverFQDN, self.appPath, secret_id, field)
        headers = {
            'authorization': "Bearer {}".format(self.token),
            'Accept': 'application/json'
        }
        log.debug(self.token)

        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()

        if filename:
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            return response.content


    def add_secret(self, secret_name, secret_username, folder_id, password, notes=u''):
        ''' Add a secret to secret server  - takes details to add
        If this gets invoked multiple times then multiple secrets will be created
        '''

        url = "https://{}{}/api/v1/secrets".format(self.serverFQDN, self.appPath)
        headers = {
            'authorization': "Bearer {}".format(self.token),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        log.debug(self.token)

        template_id = DEFAULTTEMPLATEID

        # The API structure is defined at - https://updates.thycotic.net/secretserver/restapiguide/
        # There is an example (which the following data structure was borrowed from) at
        # https://infotechbrain.com/2018/11/thycotic-python-rest-api-create-new-secret
        data = {u'requiresComment': False,
                u'enableInheritPermissions': True,
                u'isOutOfSync': False,
                u'checkOutEnabled': False,
                u'allowOwnersUnrestrictedSshCommands': False,
                u'checkOutChangePasswordEnabled': False,
                u'enableInheritSecretPolicy': True,
                u'autoChangeEnabled': False,
                u'sessionRecordingEnabled': False,
                u'lastHeartBeatStatus': u'Pending',
                u'restrictSshCommands': False,
                u'active': True,
                u'isDoubleLock': False,
                u'siteId': 1,
                u'folderId': folder_id,
                u'items': [
                    {u'isNotes': False,
                     u'fieldDescription': u'The URL/location where information is being secured.',
                     u'isPassword': False,
                     u'isFile': False,
                     u'filename': None,
                     u'fieldName': u'Resource',
                     u'itemValue': u'',
                     u'fileAttachmentId': None,
                     u'fieldId': 60,
                     u'slug': u'resource'},
                    {u'isNotes': False,
                     u'fieldDescription': u'The name assocated with the password.',
                     u'isPassword': False,
                     u'isFile': False, u'filename': None, u'fieldName': u'Username',
                     u'itemValue': secret_username,
                     u'fileAttachmentId': None, u'fieldId': 61, u'slug': u'username'},
                    {u'isNotes': False,
                     u'fieldDescription': u'The password used to access information.',
                     u'isPassword': True,
                     u'isFile': False,
                     u'filename': None,
                     u'fieldName': u'Password',
                     u'itemValue': password,
                     u'fileAttachmentId': None,
                     u'fieldId': 7,
                     u'slug': u'password'},
                    {u'isNotes': True,
                     u'fieldDescription': u'Any comments or additional information for the secret.',
                     u'isPassword': False, u'isFile': False, u'filename': None,
                     u'fieldName': u'Notes',
                     u'itemValue': notes,
                     u'fileAttachmentId': None, u'fieldId': 8, u'slug': u'notes'}],
                u'name': secret_name,
                u'secretTemplateId': template_id}

        response = requests.request("POST", url, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        return 0

if __name__ == '__main__':

    SSUSERNAME = None
    SSPASSWORD = None
    SSDOMAIN = None
    SSSECRETID = None
    SSTOKEN = None
    DEBUG = None
    SSDISPLAYTOKEN = False
    SEARCHSTRING = None
    ADDSECRETNAME = None
    DOWNLOADSECRETNAME = None
    SECRETFOLDER = None
    ADDSECRETUSERNAME = None
    ADDSECRETPASSWORD = None
    TOKENFILE = None

    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:], "hi:u:d:t:vgs:a:x:f:e:j:", \
                ["help", "id=", "user=", "domain=", "token=", "gettoken",
                 "search=", "add=", "folder=", "secretusername=",
                 "secretpassword=", "tokenfile="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in OPTS:
        if o == "-v":
            DEBUG = True
        elif o in ("-u", "--user"):
            SSUSERNAME = a
        elif o in ("-d", "--domain"):
            SSDOMAIN = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--id"):
            SSSECRETID = a
        elif o in ("-t", "--token"):
            SSTOKEN = a
        elif o in ("-g", "--gettoken"):
            SSDISPLAYTOKEN = True
        elif o in ("-s", "--search"):
            SEARCHSTRING = a
        elif o in ("-a", "--add"):
            ADDSECRETNAME = a
        elif o in ("-x", "--download"):
            DOWNLOADSECRETNAME = a
        elif o in ("-f", "--folder"):
            SECRETFOLDER = a
        elif o in ("-e", "--secretusername"):
            ADDSECRETUSERNAME = a
        elif o in ("-j", "--secretpassword"):
            ADDSECRETPASSWORD = a
        elif o in ("-o", "--tokenfile"):
            TOKENFILE = a
        else:
            assert False, "unhandled option"

    # Lets display as much info about the http headers/requests as possible
    if DEBUG:
        import http.client as http_client
        http_client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        log.setLevel(logging.DEBUG)
        REQUESTS_LOG = logging.getLogger("requests.packages.urllib3")
        REQUESTS_LOG.setLevel(logging.DEBUG)
        REQUESTS_LOG.propagate = True

    # We need to prompt if we are either setting up a token/tokenfile
    # or if we are working as a single hit request.
    if (not SSUSERNAME and not SSTOKEN and not TOKENFILE) or SSDISPLAYTOKEN:
        SSUSERNAME = input('Username: ')

    if (not SSTOKEN and not TOKENFILE) or SSDISPLAYTOKEN:
        SSPASSWORD = getpass.getpass("Password: ")

    if SSDOMAIN is None:
        SSDOMAIN = DEFAULTDOMAIN

    # If we dont have a specific secret or search string request one.
    if SSSECRETID is None and SSDISPLAYTOKEN is None and not SEARCHSTRING:
        SSSECRETID = input('SecretID: ')

    if SSSECRETID is not None and not SSSECRETID.isdigit():
        print("Secret must be numerical")
        usage()
        sys.exit(4)

    SECUREV = Secure()

    # This will be true if we are setting up a token or working single hit.
    if (SSUSERNAME and SSPASSWORD):
        SECUREV.set_auth(SSUSERNAME, SSPASSWORD, SSDOMAIN)
    else:
        SECUREV.set_token(SSTOKEN)

    # If we are working with a token from a file
    if TOKENFILE:
        if not SSDISPLAYTOKEN:
            TFILE = open(TOKENFILE, "r")
            if TFILE.mode == 'r':
                SSTOKEN = TFILE.read()
                TFILE.close()
                SECUREV.set_token(SSTOKEN)
        else:
            with os.fdopen(os.open(TOKENFILE, os.O_WRONLY | os.O_CREAT, 0o600), 'w') as FILE:
                FILE.write(SECUREV.get_token())
            FILE.close()
            # Assume that we should stop here and the token from the file
            # will be used later.
            sys.exit(0)

    if SEARCHSTRING:
        ALLSECRETS = SECUREV.get_search_secrets(SEARCHSTRING)

        for foundsecret in ALLSECRETS['records']:
            print('Name={}->ID={}'.format(foundsecret['name'], foundsecret['id']))

    elif ADDSECRETNAME:
        SECUREV.add_secret(ADDSECRETNAME, ADDSECRETUSERNAME, SECRETFOLDER, ADDSECRETPASSWORD)
    elif DOWNLOADSECRETNAME:
        SECUREV.download_secret(SSSECRETID, DOWNLOADSECRETNAME)

    else:
        if SSSECRETID:
            RETSECRET = SECUREV.get_secret_by_id(SSSECRETID)
            print(RETSECRET.password)
