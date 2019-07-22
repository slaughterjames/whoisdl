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

'''
whoisdlclass.py - This file is responsible maintaining the whoisdl object as it moves from module to module
'''

#python imports
#from array import *

#programmer generated imports
#No third-party imports

'''
whoisdlclass - This file is responsible maintaining the whoisdl object as it moves from module to module
'''
class whoisdlclass:
    '''
    Constructor
    '''
    def __init__(self, logfile, debug, domainlist, keyword_list, outputdir):

        self.logfile = logfile
        self.debug = debug
        self.domainlist = domainlist
        self.keyword_list = keyword_list
        self.outputdir = outputdir   
                     
