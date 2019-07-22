#!/usr/bin/python
'''
whoisdl v0.2 - Copyright 2019 James Slaughter,
This file is part of whoisdl v0.2.

whoisdl v0.2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

whoisdl v0.2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with whoisdl v0.2.  If not, see <http://www.gnu.org/licenses/>.
'''

#python import
import sys
import os
import datetime
import time
import json
import simplejson
import smtplib
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
from array import *
from termcolor import colored

#programmer generated imports
from controller import controller
from whoisdlclass import whoisdlclass
from fileio import fileio
from mms import mms

'''
Usage()
Function: Display the usage parameters when called
'''
def Usage():
    print 'Usage: [required] --domainlist --type --modules --outputdir [optional] --debug --help'
    print 'Example: /opt/whoisdl/whoisdl.py --domainlist /home/scalp/whoisdl/2018-06-21/domain-names2018-06-21.csv --type info --modules Grep_Domain_List --outputdir /home/scalp/whoisdl/output --debug'
    print 'Required Arguments:'
    print '--domainlist - The list of domains to be reviewed'
    print '--type - info should be used by default but additional types can be set in the whoisdl.conf.'
    print '--modules - all or specific'
    print '--outputdir - Location where keyword matches are to be deposited'
    print '--listmodules - Prints a list of available modules and their descriptions.'
    print '--debug - Prints verbose logging to the screen to troubleshoot issues with a recon installation.'
    print '--help - You\'re looking at it!'
    sys.exit(-1)

'''
ConfRead()
Function: - Reads in the whoisdl.conf config file and assigns some of the important
            variables
'''
def ConfRead():
        
    ret = 0
    intLen = 0
    FConf = fileio()
    FLOG = fileio()

    try:
        #Conf file hardcoded here
        with open('/opt/whoisdl/whoisdl.conf', 'r') as read_file:
            data = json.load(read_file)
    except:
        print '[x] Unable to read configuration file  Terminating...\n'
        return -1    

    CON.keywords = data['keywords']
    CON.logfile = data['logfile']   
    CON.modulesdir = data['modulesdir']
    CON.types = data['addintypes']
    CON.addins = data['addins']
    CON.emailalerting = data['emailalerting']
    CON.recipients = data['recipients']
    CON.email = data['email']
    CON.password = data['password']
    CON.email_subject = data['subject']    
  
    if (CON.debug == True):
        print '[DEBUG] data: ', data
        print '[DEBUG] CON.keywords: ' + str(CON.keywords)
        print '[DEBUG] CON.logroot: ' + str(CON.logfile)
        print '[DEBUG] CON.modulesdir: ' + str(CON.modulesdir)
        print '[DEBUG] CON.types: ' + str(CON.types)
        print '[DEBUG] CON.addins: ' + str(CON.addins)
        print '[DEBUG] CON.emailalerting: ' + str(CON.emailalerting)
        print '[DEBUG] CON.recipients: ' + str(CON.recipients)
        print '[DEBUG] CON.email: ' + str(CON.email)
        print '[DEBUG] CON.email_subject: ' + str(CON.email_subject)
 
        for a_addins in CON.addins: 
            for key, value in a_addins.iteritems():
                print '[DEBUG] CON.addins key: ' + key + ' value: ' + value

    if (CON.emailalerting == True):
        print '[*] E-mail alerting is active...'
        FLOG.WriteLogFile(CON.logfile, '[*] E-mail alerting is active...\n') 

        if (len(CON.email) < 3):
            print '[x] Please enter a valid sender e-mail address in the whoisdl.conf file.  Terminating...'
            FLOG.WriteLogFile(CON.logfile, '[x] Please enter a valid sender e-mail address in the whoisdl.conf file.  Terminating...\n')            
            print ''
            return -1    

        if (len(CON.password) < 3):
            print '[x] Please enter a valid sender e-mail password in the whoisdl.conf file.  Terminating...'
            FLOG.WriteLogFile(CON.logfile, '[x] Please enter a valid sender e-mail password in the whoisdl.conf file.  Terminating...\n')            
            print ''
            return -1

        if (len(CON.recipients) < 3):
            print '[x] Please enter a valid recipients file in the whoisdl.conf file.  Terminating...' 
            FLOG.WriteLogFile(CON.logfile, '[x] Please enter a valid recipients file in the whoisdl.conf file.  Terminating...\n')           
            print ''
            return -1

        if (len(CON.email_subject) < 3):
            print '[-] No custom e-mail subject entered.  Using: "Whoisdl Alert"'
            FLOG.WriteLogFile(CON.logfile, '[-] No custom e-mail subject entered.  Using: \"Whoisdl Alert\"\n')
            CON.email_subject == 'Whoisdl Alert'            
            print ''
            
    if (CON.debug == True):
       print '[*] Finished configuration.'
       print ''

    print '[*] Executing whoisdl.py v0.2... '
    FLOG.WriteLogFile(CON.logfile, '[*] Executing whoisdl.py v0.2...\n')

    if (len(CON.keywords) < 3):
        print '[x] Please enter a valid keywords file in the whoisdl.conf file.  Terminating...'
        FLOG.WriteLogFile(CON.logfile, '[x] Please enter a valid keywords file in the whoisdl.conf file.  Terminating...\n')            
        print ''
        return -1

    try:
        # Read in our list of keywords
        with open(CON.keywords.strip(),"r") as fd:
            file_contents = fd.read()
            CON.keyword_list      = file_contents.splitlines()

    except:
        # Keywords list read failed, bail!
        print '[x] Unable to read keywords file: ' + CON.keywords
        FLOG.WriteLogFile(CON.logfile, '[x] Unable to read keywords file: ' + CON.keywords)
        return -1

    if (CON.emailalerting == 'True'):
        try:
            # Read in our list of recipients
            with open(CON.recipients.strip(),"r") as fd:
                file_contents2 = fd.read()
                CON.recipient_list    = file_contents2.splitlines()
        except:
            # Recipients list read failed, bail!
            print '[x] Unable to read recipients file: ' + CON.recipients
            FLOG.WriteLogFile(CON.logfile, '[x] Unable to read recipients file: ' + CON.recipients) 
            return -1
         
    print '[*] Finished configuration successfully.\n'
    FLOG.WriteLogFile(CON.logfile, '[*] Finished configuration successfully.\n')

    return 0

'''
Parse() - Parses program arguments
'''
def Parse(args):        
    option = ''
                    
    print '[*] Arguments: \n'
    for i in range(len(args)):
        if args[i].startswith('--'):
            option = args[i][2:]  

            if option == 'domainlist':
                CON.domainlist = args[i+1]
                print option + ': ' + str(CON.domainlist)

            if option == 'outputdir':
                CON.outputdir = args[i+1]
                print option + ': ' + str(CON.outputdir)

            if option == 'type':
                CON.type = args[i+1]
                print option + ': ' + CON.type

            if option == 'modules':
                CON.modules = args[i+1]
                print option + ': ' + CON.modules                       

            if option == 'debug':
                CON.debug = True
                print option + ': ' + str(CON.debug)

    #listmodules will cause all other params to be ignored
    if (option == 'listmodules'):
        CON.listmodules = True
        print option + ': ' + str(CON.listmodules)
        print ''
        return 0
    elif (len(CON.type) < 3):
        print '[x] type is a required argument'           
        print ''
        return -1
    else:
        #These are required params so length needs to be checked after all 
        #are read through  
        if (len(CON.domainlist) < 3):
            print '[x] domainlist is a required argument'           
            print ''
            return -1

        if (len(CON.outputdir) < 3):
            print '[x] outputdir is a required argument'           
            print ''
            return -1

        if (len(CON.modules) < 3):
            print '[x] modules is a required argument'           
            print ''
            return -1

'''
send_alert()
Function: - Sends the alert e-mail from the address specified
            in the configuration file to potentially several addresses
            specified in the "recipients.txt" file.
'''
def send_alert():

    FLOG = fileio()

    #Jiggery pokery to get the input domainlist to switch to a .zip extention 
    domainlist = CON.domainlist
    domainlist = domainlist.split('.csv')
    domainlist = str(domainlist[0]) + '.zip'

    print '[-] Domainlist set as: ' + str(domainlist) + '\n'
    
    #Build the e-mail body
    email_body = 'WhoisDL has completed a run ' + str(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")) + '\n'
    email_body += '\n'
    email_body += 'Attachments: \n'
    email_body += str(domainlist) + ': Full downloaded list of newly registered domains.\n'
    email_body += 'output.csv: Grepped output of domains based on keyword searches.\n'

    #Loop through each recipient in the list and send them each an e-mail
    for recipient_entry in CON.recipient_list:
        print '\r\n[-] Sending e-mail to: ' + recipient_entry                        
        FLOG.WriteLogFile(CON.logfile, '[-] Sending e-mail to: ' + recipient_entry + '\n')

        # Build the email message
        msg = MIMEMultipart()
        msg['Subject'] = CON.email_subject.strip()
        msg['From']    = CON.email.strip()
        msg['To']      = recipient_entry
        msg.attach(MIMEText(email_body))

        #Build attachment 1, the full domain list, zipped...
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(str(domainlist), "rb").read())
        Encoders.encode_base64(part)        

        part.add_header('Content-Disposition', 'attachment; filename=' + str(domainlist))

        msg.attach(part)

        #Build attachment 2, the actual application output
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(CON.outputdir + '/' + 'output.csv', "rb").read())
        Encoders.encode_base64(part)        

        part.add_header('Content-Disposition', 'attachment; filename=' + CON.outputdir + '/' + 'output.csv')

        msg.attach(part)
    
        #We're all Google fans...
        server = smtplib.SMTP("smtp.gmail.com",587)
    
        #Fire when rdy...
        server.ehlo()
        server.starttls()
        server.login(CON.email.strip(),CON.password.strip())
        server.sendmail(recipient_entry,recipient_entry,msg.as_string())
        server.quit()    
    
        print '[*] Alert email sent!'
        FLOG.WriteLogFile(CON.logfile, '[*] Alert email sent!\n')  
    
    return 0

'''
ListModules()
Function: - List all available modules and their descriptions
'''
def ListModules():
    FConf = fileio()
    count = 0
    addins = ''

    for addins in CON.addins: 
        for key, value in addins.iteritems():
            FConf.ReadFile(CON.modulesdir.strip() + value.strip() + '.py')
            for line in FConf.fileobject:
                if (count == 1):
                    print '[*] ' + value + ': ' + line
                    count = 0
                    break
                if (line.find('***BEGIN DESCRIPTION***') != -1):
                    count = 1              

    return 0

'''
Terminate()
Function: - Attempts to exit the program cleanly when called  
'''     
def Terminate(exitcode):
    sys.exit(exitcode)

'''
Execute()
Function: - Does the doing
'''
def Execute():

    ret = MMS.OrganizeModules(CON.whoisdlobject)
    if (ret !=0 ):
        print '[x] Unable to continue module execution.  Terminating...'
        Terminate(ret)  
 
    send_alert()
       
    return 0

'''
This is the mainline section of the program and makes calls to the 
various other sections of the code
'''
if __name__ == '__main__':

    ret = 0 
    count = 0  

    CON = controller()
    FLOG = fileio() 

    ret = Parse(sys.argv)
    if (ret == -1):
        Usage()
        Terminate(ret) 

    ret = ConfRead()
    # Something bad happened...bail
    if (ret != 0):
        Terminate(ret) 

    if (CON.listmodules == True):
        ListModules()
        Terminate(0) 

    #We should likely already have an output directory if whoisdl.sh has been run first...
    if not os.path.exists(CON.outputdir):
        print '[*] Creating output directory...' + CON.outputdir
        FLOG.WriteLogFile(CON.logfile, '[*] Creating output directory...' + CON.outputdir + '\n')
        os.mkdir(CON.outputdir)
                  
    else:
        print '[-] Output directory already exists...'
        FLOG.WriteLogFile(CON.logfile, '[-] Output directory already exists...\n')

    if (CON.type == 'all'):
        for addins in CON.addins: 
            for key, value in addins.iteritems():
                CON.module_manifest.append(value)
            MMS = mms(CON.module_manifest, CON.modulesdir, CON.modules, CON.debug)
    else:
        if (CON.type in CON.types):
            print '[*] Type is ' + CON.type
            for addins in CON.addins: 
                for key, value in addins.iteritems():
                    if (key == CON.type):
                        CON.module_manifest.append(value)
                MMS = mms(CON.module_manifest, CON.modulesdir, CON.modules, CON.debug) 
        else:
            print '[x] Type ' + CON.type + ' is not recognized...\n'
            print 'Type must be one of the following:'
            for types in CON.types:
                print types
            print '[x] Terminating...'
            Terminate(-1)   

    if (CON.debug == True):
        print '[DEBUG]: ', CON.module_manifest

    CON.whoisdlobject = whoisdlclass(CON.logfile, CON.debug, CON.domainlist, CON.keyword_list, CON.outputdir)
    Execute()
    del CON.whoisdlobject

    print '[*] Program Complete'        

    Terminate(0)

'''
END OF LINE
'''

