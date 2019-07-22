#===============================================================================
#whoisdl v0.2 - Copyright 2019 James Slaughter,
#This file is part of whoisdl v0.2.
#
#whoisdl v0.2 is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#whoisdl v0.2 is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with whoisdl v0.2.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

Whoisdl v0.2

    Tool developed in BASH and Python that downloads newly registered domain information to allow analysis and searching for malicious domains.
    BASH script component can be added to cron (crontab -e at the command line) in order to automate. For example: 30 5 * * * /opt/whoisdl/whoisdl.sh This will trigger the tool to run each morning at 05:30 AM. It's suggested running the tool early in the morning as the analysis on a large registration day can be lengthy.
    In the event a day is missed and data is downloaded externally (https://whoisds.com) and extracted, the Python component of the tool can be executed against this dataset.

Due to some hardcoding, the tool should be deposited in the /opt/whoisdl directory. I'd also recommend putting a whoisdl folder in the /home/<your directory> to put the keywords.txt file.

Usage - whoisdl.sh: /opt/whoisdl/whoisdl.sh

Usage - whoisdl.py: [required] --domainlist --type --modules --outputdir [optional] --listmodules --debug --help
    Example: /opt/whoisdl/whoisdl.py --domainlist /home/scalp/whoisdl/2018-06-21/domain-names2018-06-21.csv --type info --modules Grep_Domain_List --outputdir /home/scalp/whoisdl/output --debug
    Required Arguments:
    --domainlist - The list of domains to be reviewed.
    --type - info should be used by default but additional types can be set in the whoisdl.conf.
    --modules - all or specific.
    --outputdir - Location where keyword matches are to be deposited
    --listmodules - Prints a list of available modules and their descriptions.
    --debug - Prints verbose logging to the screen to troubleshoot issues with a recon installation.
    --help - You\'re looking at it!

The whoisdl.conf file contains all of the settings needed to run the tool.  The tool is formatted as JSON and needs to be kept as such in order to read properly.
{
    "keywords": "<Your directory>/keywords.txt",
    "logfile": "<Your directory>/whoisdl.log",
    "modulesdir": "/opt/whoisdl/modules/",
    "emailalerting": "False",
    "recipients": "<Your directory>/recipients.txt",
    "subject": "WhoisDL E-mail Update",
    "email": "<Your e-mail address>",
    "password": "<Your e-mail password>",
    "addintypes": ["info"],
    "addins": [
        {
            "info": "Grep_Domain_List"
        }
    ]
}

Output:  E-mail functionality has been added.  To enable, change the "emailalerting": "False" line to "emailalerting": "True".
Change the "subject" line to one that suits your personal circumstances and add your personal details to "email" and "password".
The entire list will also be e-mailed out as zipped attachment.

The biggest change to this version is the addition of modularity and the ability to code custom modules.  To enable it, drop it in the /opt/whoisdl/modules/ directory
and under the "addins" heading, change it to look like this:
        {
            "info": "Grep_Domain_List"
        },
        {
            "info": "<Your new module>"
        } 

To differentiate different addin categories, you can create new ones to change the run flow by changing "addintypes": ["info"], to "addintypes": ["info", "<your new type>"],

CHANGELOG VERSION V0.2:
    - Added modular functionality
    - Added e-mail functionality
    - Changed default output to CSV file

CHANGELOG VERSION V0.1:

    First iteration of the tool


