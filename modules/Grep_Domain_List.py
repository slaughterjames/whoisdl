#python imports
import sys
import os
import subprocess
from termcolor import colored

#third-party imports
#No third-party imports

#programmer generated imports
from fileio import fileio

'''
***BEGIN DESCRIPTION***
Greps the domain list based on a read in set of keywords
***END DESCRIPTION***
'''
def POE(POE):

    FLOG = fileio()
    grepq_data = ''
    grepq_output_data = ''
    grep_data = ''
    grep_output_data = ''
    grep_domain_list_dir = 'grep_domain_list'
    keyword_count = len(POE.keyword_list)
    Count = 0

    FI = fileio()
    
    print '[*] Running grep against: ' + POE.domainlist
    FLOG.WriteLogFile(POE.logfile, '[*] Running grep against: ' + POE.domainlist + '\n')

    # Cheeky way to create the output file initially with two columns as a csv...
    subproc = subprocess.Popen('echo Keyword,Domain >> ' + POE.outputdir + '/' + 'output.csv', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)    
   
    #Cycle through each keyword in our list...
    for i in POE.keyword_list:         
        #Reduce the amount of search time by checking for any results of a particular keyword first before doing the grep...
        subproc = subprocess.Popen('if grep -q ' + POE.keyword_list[Count] + ' ' + POE.domainlist + '; then echo "found"; else echo "not located"; fi', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for grepq_data in subproc.stdout.readlines():
            grepq_output_data += grepq_data
            if (POE.debug == True):
                print '[DEBUG] ' + grepq_output_data
            if (grepq_data.find('found') != -1):
                print '[*] Matches for keyword: ' + POE.keyword_list[Count] + ' found...'
                FLOG.WriteLogFile(POE.logfile.strip(), '[*] Matches for keyword: ' + POE.keyword_list[Count] + ' found...\n') 
                if (POE.debug == True):
                    print '[DEBUG] grep command: ' + 'grep ' + POE.keyword_list[Count] + ' ' + POE.domainlist + ' >> ' + POE.outputdir + '/' + grep_domain_list_dir + '/' + POE.keyword_list[Count] + '.txt'        #If results are found, then do the actual grep, followed by a sed to insert the search term in the previous column.
                subproc = subprocess.Popen('grep ' + POE.keyword_list[Count] + ' ' + POE.domainlist + '| sed \'s/^/' + POE.keyword_list[Count] + ',/\'' + ' >> ' + POE.outputdir + '/' + 'output.csv', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                grep_output_data += grep_data
                
                if (POE.debug == True):
                    print '[DEBUG] ' + grep_output_data

                FI.WriteLogFile(POE.logfile, grep_output_data) 
                grep_output_data = ''

            else:
                print '[*] No matches for keyword: ' + POE.keyword_list[Count] + ' found.  Checking next enty...'
                FLOG.WriteLogFile(POE.logfile, '[*] No matches for keyword: ' + POE.keyword_list[Count] + ' found.  Checking next enty...\n') 

            Count += 1                              

    return 0
