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

Whoisdl v0.1
- Tool developed in BASH and Python that downloads newly registered domain information to allow analysis and searching for malicious domains.
- BASH script component can be added to cron (crontab -e at the command line) in order to automate.  For instance:
  30 5 * * * /opt/whoisdl/whoisdl.sh
  This will trigger the tool to run each morning at 05:30 AM.  It's suggested running the tool early in the morning as the analysis on a large registration day can be lengthy.
- In the event a day is missed and data is downloaded externally (https://whoisds.com/whois-database/newly-registered-domains/2018-XX-XX.zip/nrd) and extracted, the Python component of the tool can be executed against this dataset. 

Due to some hardcoding, the tool should be deposited in the /opt/whoisdl directory.  I'd also recommend putting a whoisdl folder in the /home/<user>/ to put the keywords.txt file.

Usage - whoisdl.sh:
/opt/whoisdl/whoisdl.sh

Usage - whoisdl.py:
Usage: [required] --domainlist --outputdir [optional] --debug --help
Example: /opt/whoisdl/whoisdl.py --domainlist /home/scalp/whoisdl/2018-06-21/domain-names2018-06-21.csv --outputdir /home/scalp/whoisdl/output --debug
Required Arguments:
--domainlist - The list of domains to be reviewed
--outputdir - Location where keyword matches are to be deposited
--debug - Prints verbose logging to the screen to troubleshoot issues with a recon installation.
--help - You're looking at it!


CHANGELOG VERSION V0.1:
- First iteration of the tool
