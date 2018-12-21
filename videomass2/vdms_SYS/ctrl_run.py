# -*- coding: UTF-8 -*-

#########################################################
# Name: ctrl_run.py
# Porpose: Program boot data
# Writer: Gianluca Pernigoto <jeanlucperni@gmail.com>
# Copyright: (c) 2015-2018/2019 Gianluca Pernigoto <jeanlucperni@gmail.com>
# license: GPL3

# This file is part of Videomass2.

#    Videomass2 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Videomass2 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Videomass2.  If not, see <http://www.gnu.org/licenses/>.

# Rev December 14 2018
#########################################################

import sys
import os
import shutil
import platform

PWD = os.getcwd() # work current directory (where is Videomsass?)
DIRNAME = os.path.expanduser('~') # /home/user (current user directory)

#------------------------------------------------------------------------#

def parsing_fileconf():
    """
    - called by bootstrap on_init -
    Make a parsing of the configuration file localized on 
    ``~/.videomass2/videomass2.conf`` and return values list of the current 
    program settings. If this file is not present or is damaged, it is marked 
    as corrupt.
    """
    filename = '%s/.videomass2/videomass2.conf' % (DIRNAME)

    with open (filename, 'r') as f:
        fconf = f.readlines()
    lst = [line.strip() for line in fconf if not line.startswith('#')]
    curr_conf = [x for x in lst if x]# list without empties values
    if not curr_conf:
        return 'corrupted'
    else:
        return curr_conf
#------------------------------------------------------------------------#

def system_check():
    """
    - called by bootstrap on_init -
    Assignment of the appropriate paths for sharing the configuration folder.
    This function checks the integrity of the Videomass2 configuration folder 
    located in each user's home directory. If this folder does not exist in 
    the user space it will be recovered from the source or installation folder 
    (this depends if local or system installation) and will be saved in 
    the user's home.  
    """
    copyerr = False
    existfileconf = True # il file conf esiste (True) o non esite (False)
    
    # What is the OS ??
    #OS = [x for x in ['Darwin','Linux','Windows'] if platform.system() in x ][0]
    OS = platform.system()

    if os.path.isdir('%s/art' % PWD):
        localepath = 'locale'
        path_srcShare = '%s/share' % PWD
        IS_LOCAL = True
        
    else: # Path system installation (usr, usr/local, ~/.local, \python27\)
        if OS == 'Windows':
            #Installed with 'pip install videomass2' command
            pythonpath = os.path.dirname(sys.executable)
            localepath = pythonpath + '\\share\\locale'
            path_srcShare = pythonpath + '\\share\\videomass2\\config'
            IS_LOCAL = False
            
        else:
            from videomass2.vdms_SYS.whichcraft import which
            binarypath = which('videomass2')
            if binarypath == '/usr/local/bin/videomass2':
                #usually Linux,MacOs,Unix
                localepath = '/usr/local/share/locale'
                path_srcShare = '/usr/local/share/videomass2/config'
                IS_LOCAL = False
            elif binarypath == '/usr/bin/videomass2':
                #usually Linux
                localepath = '/usr/share/locale'
                path_srcShare = '/usr/share/videomass2/config'
                IS_LOCAL = False
            else:
                #installed with 'pip install --user videomass2' command
                import site
                userbase = site.getuserbase()
                localepath = userbase + 'share/locale'
                path_srcShare = userbase + '/share/videomass2/config'
                IS_LOCAL = False

    #### check videomass.conf and config. folder
    if os.path.exists('%s/.videomass2' % DIRNAME):#if exist folder ~/.videomass
        if os.path.isfile('%s/.videomass2/videomass2.conf' % DIRNAME):
            fileconf = parsing_fileconf() # fileconf data
            if fileconf == 'corrupted':
                print 'videomass2.conf is corrupted! try to restore..'
                existfileconf = False
            if float(fileconf[0]) < 1.2:
                existfileconf = False
        else:
            existfileconf = False
        
        if not existfileconf:
            try:
                if OS == ('Linux') or OS == ('Darwin'):
                    shutil.copyfile('%s/videomass2.conf' % path_srcShare, 
                                    '%s/.videomass2/videomass2.conf' % DIRNAME)
                elif OS == ('Windows'):
                    shutil.copyfile('%s/videomassWin32.conf' % path_srcShare, 
                                    '%s/.videomass2/videomass2.conf' % DIRNAME)
                fileconf = parsing_fileconf() # fileconf data, reread the file
            except IOError:
                copyerr = True
                fileconf = 'corrupted'
    else:
        try:
            shutil.copytree(path_srcShare,'%s/.videomass2' % DIRNAME)
            if OS == ('Windows'):
                os.remove("%s/.videomass2/videomass2.conf" % (DIRNAME))
                os.rename("%s/.videomass2/videomassWin32.conf" % (DIRNAME),
                          "%s/.videomass2/videomass2.conf" % (DIRNAME))
            fileconf = parsing_fileconf() # fileconf data, reread the file
        except OSError:
            copyerr = True
            fileconf = 'corrupted'
        except IOError:
            copyerr = True
            fileconf = 'corrupted'

    return (OS, path_srcShare, copyerr, IS_LOCAL, fileconf, localepath)

#------------------------------------------------------------------------#
