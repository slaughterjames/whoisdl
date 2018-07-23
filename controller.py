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

'''
controller.py - 
'''

#python imports
import imp
import sys
from array import *

#programmer generated imports


'''
controller
Class: This class is responsible for maintaining key variable values globally
'''
class controller:
    '''
    Constructor
    '''
    def __init__(self):

        self.debug = False
        self.keywords = ''
        self.keyword_list = ''
        self.logfile = ''
        self.domainlist = ''
        self.outputdir = ''                     