#!/usr/bin/python
'''
whoisdl v0.1 - Copyright 2018 James Slaughter,
This file is part of whoisdl v0.1.

whoisdl v0.1 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

whoisdl v0.1 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with whoisdl v0.1.  If not, see <http://www.gnu.org/licenses/>.
'''

#python import
import sys
import os
import subprocess
import datetime
import time
from array import *
from termcolor import colored

#programmer generated imports
from controller import controller
from fileio import fileio

'''
Usage()
Function: Display the usage parameters when called
'''
def Usage():
    print 'Usage: [required] --domainlist --outputdir [optional] --debug --help'
    print 'Example: /opt/whoisdl/whoisdl.py --domainlist /home/scalp/whoisdl/2018-06-21/domain-names2018-06-21.csv --outputdir /home/scalp/whoisdl/output --debug'
    print 'Required Arguments:'
    print '--domainlist - The list of domains to be reviewed'
    print '--outputdir - Location where keyword matches are to be deposited'
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
    print '[*] Executing whoisdl.py v0.1... '
    FLOG.WriteLogFile(CON.logfile, '[*] Executing whoisdl.py v0.1...\n')

    try:
        #Conf file hardcoded here
    	FConf.ReadFile('/opt/whoisdl/whoisdl.conf')
    except:
        print '[x] Unable to read configuration file!  Terminating...'
        FLOG.WriteLogFile(CON.logfile, '[x] Unable to read configuration file!  Terminating...\n')
        return -1
    
    for line in FConf.fileobject:
        intLen = len(line)            
        if (CON.debug == True):
            print '[DEBUG]: ' + line
        if (line.find('keywords') != -1):                
            CON.keywords = line[9:intLen] 
        elif (line.find('logfile') != -1): 
            CON.logfile = line[8:intLen]               
            CON.logfile.strip()             
        else:
            if (CON.debug == True): 
                print ''

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
        print '[x] Unable to read keywords file: ' + CON.keywords
        FLOG.WriteLogFile(CON.logfile, '[x] Unable to read keywords file: ' + CON.keywords)
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

            if option == 'debug':
                CON.debug = True
                print option + ': ' + str(CON.debug)

    if len(CON.domainlist) < 3:
        print '[x] domainlist is a required argument'           
        print ''
        return -1

    if len(CON.outputdir) < 3:
        print '[x] outputdir is a required argument'           
        print ''
        return -1

'''
grep_domain_list()
Function: - calls grep to execute against the keyword list
'''
def grep_domain_list():

    FLOG = fileio()
    grepq_data = ''
    grepq_output_data = ''
    grep_data = ''
    grep_output_data = ''
    keyword_count = len (CON.keyword_list)
    Count = 0

    FI = fileio()
    
    print '[*] Running grep against: ' + CON.domainlist
    FLOG.WriteLogFile(CON.logfile, '[*] Running grep against: ' + CON.domainlist + '\n')

    for i in CON.keyword_list:         

        subproc = subprocess.Popen('if grep -q ' + CON.keyword_list[Count] + ' ' + CON.domainlist + '; then echo "found"; else echo "not located"; fi', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for grepq_data in subproc.stdout.readlines():
            grepq_output_data += grepq_data
            if (CON.debug == True):
                print '[DEBUG] ' + grepq_output_data
            if (grepq_data.find('found') != -1):
                print '[*] Matches for keyword: ' + CON.keyword_list[Count] + ' found...'
                FLOG.WriteLogFile(CON.logfile.strip(), '[*] Matches for keyword: ' + CON.keyword_list[Count] + ' found...\n') 
                if (CON.debug == True):
                    print '[DEBUG] grep command: ' + 'grep ' + CON.keyword_list[Count] + ' ' + CON.domainlist + ' >> ' + CON.outputdir + '/' + CON.keyword_list[Count] + '.txt'
                subproc = subprocess.Popen('grep ' + CON.keyword_list[Count] + ' ' + CON.domainlist + ' >> ' + CON.outputdir + '/' + CON.keyword_list[Count] + '.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                grep_output_data += grep_data
                
                if (CON.debug == True):
                    print '[DEBUG] ' + grep_output_data

                FI.WriteLogFile(CON.logfile, grep_output_data) 
                grep_output_data = ''

            else:
                print '[*] No matches for keyword: ' + CON.keyword_list[Count] + ' found.  Checking next enty...'
                FLOG.WriteLogFile(CON.logfile, '[*] No matches for keyword: ' + CON.keyword_list[Count] + ' found.  Checking next enty...\n') 

            Count += 1
                               
    return 0

'''
pipe_to_mirage()
Function: - Builds a query based on the keywords that are read in             
'''
def pipe_to_mirage():

    FLOG = fileio()
    mirage_data = ''
    mirage_output_data = ''
    Count = 0
    
    print '[*] Piping to Mirage...'
    FLOG.WriteLogFile(CON.logfile, '[*] Piping to Mirage...\n')

    targetlists = os.listdir(CON.outputdir)

    for i in targetlists:
        print '[*] Running mirage against targetlist: ' + CON.outputdir  + '/' +targetlists[Count]
        FLOG.WriteLogFile(CON.logfile, '[*] Running mirage against targetlist: ' + CON.outputdir  + '/' +targetlists[Count] + '\n') 
        if (CON.debug == True):
            print '[DEBUG] mirage command: ' + '/opt/mirage/mirage.py --domain --targetlist ' + CON.outputdir  + '/' +targetlists[Count] + ' --type info --modules whois --output ' + CON.outputdir + '/mirage/' + targetlists[Count] + '--sleeptime 2 --csv'
        
        subproc = subprocess.Popen('/opt/mirage/mirage.py --domain --targetlist ' + CON.outputdir  + '/' + targetlists[Count] + ' --type info --modules whois --output ' + CON.outputdir + '/mirage/' + targetlists[Count] + ' --sleeptime 2 --csv', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for mirage_data in subproc.stdout.readlines():
            mirage_output_data += mirage_data
            if (CON.debug == True): 
                print '[DEBUG] ' + mirage_output_data
        
        Count+=1
                    
    return 0

'''
Terminate()
Function: - Attempts to exit the program cleanly when called  
'''     
def Terminate(exitcode):
    sys.exit(exitcode)

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

    FLOG.WriteLogFile(CON.logfile, '[*] Executing whoisdl.py v0.1...\n')
    ret = ConfRead()
    # Something bad happened...bail
    if (ret != 0):
        Terminate(ret)  

    if not os.path.exists(CON.outputdir):
        print '[*] Creating output directory...' + CON.outputdir
        FLOG.WriteLogFile(CON.logfile, '[*] Creating output directory...' + CON.outputdir + '\n')
        os.mkdir(CON.outputdir)
                  
    else:
        print '[-] Output directory already exists...'
        FLOG.WriteLogFile(CON.logfile, '[-] Output directory already exists...\n')

    # Execute grep against the list of ingested keywords
    grep_domain_list()

    # Execute mirage against the lists results from grep_domain_list()
    pipe_to_mirage()

'''
END OF LINE
'''

