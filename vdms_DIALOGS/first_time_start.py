# -*- coding: UTF-8 -*-
#
#########################################################
# Name: first_time_start.py
# Porpose: Automatize settings first time start
# Author: Gianluca Pernigoto <jeanlucperni@gmail.com>
# Copyright: (c) 2013-2018/2019 Gianluca Pernigoto <jeanlucperni@gmail.com>
# license: GNU GENERAL PUBLIC LICENSE (see COPYING)

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

# Rev (00) Sett 15 2018
#########################################################
#
import wx
import os
import platform

from vdms_SYS.whichcraft import which

dirname = os.path.expanduser('~/') # /home/user/
filename = '%s/.videomass2/videomass2.conf' % (dirname)
PWD = os.getcwd()
OS = platform.system()

class FirstStart(wx.Dialog):
    
    def __init__(self, img):
        """
        """
        wx.Dialog.__init__(self, None, -1, style=wx.DEFAULT_DIALOG_STYLE)
        
        msg = ("This wizard automatically searches for FFmpeg in your system.\n"
               "You can also manually specify your customs paths of FFmpeg.\n"
               "However, you can always change these settings later in the\n"
               "Setup dialog.\n\n"
               "- If you want start the search now, press the 'Search' button."
               "\n\n"
               "- If you want to set your custom paths, check the\n"
               "  'Enable Custom Paths', then enter the paths of FFmpeg\n"
               "  and press the 'Confirm' button."
               )
        # widget:
        bitmap_drumsT = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(
                                        img,wx.BITMAP_TYPE_ANY))
        lab_welc2 = wx.StaticText(self, wx.ID_ANY, (msg))
        lab_welc1 = wx.StaticText(self, wx.ID_ANY, (
                                              "Welcome to Videomass2 Wizard!"))
        self.searchBtn = wx.Button(self, wx.ID_ANY, ("Search"))
        self.ckbx_paths = wx.CheckBox(self, wx.ID_ANY, ("Enable Custom Paths"))
        self.customBtn = wx.Button(self, wx.ID_ANY, ("Confirm"))
        lab_ffmpeg = wx.StaticText(self, wx.ID_ANY, ("ffmpeg pathname:"))
        self.txtctrl_ffmpeg = wx.TextCtrl(self, wx.ID_ANY, "")
        lab_ffprobe = wx.StaticText(self, wx.ID_ANY, ("ffprobe pathname:"))
        self.txtctrl_ffprobe = wx.TextCtrl(self, wx.ID_ANY, "")
        lab_ffplay = wx.StaticText(self, wx.ID_ANY, ("ffplay pathname:"))
        self.txtctrl_ffplay = wx.TextCtrl(self, wx.ID_ANY, "")
        
        close_btn = wx.Button(self, wx.ID_EXIT, "")
        
        # properties
        self.SetTitle("Wizard - Videomass2")
        lab_welc1.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL,wx.BOLD, 0, ""))
        # layout:
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        grd_base = wx.FlexGridSizer(2, 1, 0, 0)
        grd_1 = wx.FlexGridSizer(1, 2, 0, 0)
        grd_ext = wx.FlexGridSizer(2, 1, 0, 0)
        grd_2 = wx.FlexGridSizer(6, 2, 0, 0)
        grd_base.Add(grd_1)
        grd_1.Add(bitmap_drumsT,0,wx.ALL, 10)
        grd_1.Add(grd_ext)
        grd_base.Add(grd_2)
        grd_ext.Add(lab_welc1,0,  wx.ALL, 10)
        grd_ext.Add(lab_welc2,0, wx.ALIGN_CENTER | wx.ALL, 10)
        grd_2.Add(self.searchBtn,0, wx.ALL|wx.EXPAND, 15)
        grd_2.Add(self.ckbx_paths,0, wx.ALIGN_CENTER | wx.ALL, 15)
        grd_2.Add(lab_ffmpeg,0, wx.ALIGN_CENTER | wx.ALL, 15)
        grd_2.Add(self.txtctrl_ffmpeg,0, wx.ALL, 15)
        grd_2.Add(lab_ffprobe,0, wx.ALIGN_CENTER | wx.ALL, 15)
        grd_2.Add(self.txtctrl_ffprobe,0, wx.ALL, 15)
        grd_2.Add(lab_ffplay,0, wx.ALIGN_CENTER | wx.ALL, 15)
        grd_2.Add(self.txtctrl_ffplay,0, wx.ALL, 15)
        grd_2.Add((260,0), 0, wx.ALL, 15)
        grd_btn = wx.FlexGridSizer(1, 2, 0, 0)
        
        grd_btn.Add(self.customBtn,0, flag=wx.ALL, border=5)
        grd_btn.Add(close_btn,0, flag=wx.ALL, border=5)
        grd_2.Add(grd_btn,0, flag=wx.ALL|wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        #properties
        self.txtctrl_ffmpeg.SetMinSize((250, -1))
        self.txtctrl_ffplay.SetMinSize((250, -1))
        self.txtctrl_ffprobe.SetMinSize((250, -1))
        self.txtctrl_ffmpeg.Disable()
        self.txtctrl_ffprobe.Disable()
        self.txtctrl_ffplay.Disable()
        self.customBtn.Disable()
        
        sizer_base.Add(grd_base)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        
        ######################## bindings #####################
        self.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_BUTTON, self.search, self.searchBtn)
        self.Bind(wx.EVT_CHECKBOX, self.enablePaths, self.ckbx_paths)
        self.Bind(wx.EVT_BUTTON, self.on_Custom, self.customBtn)
        self.Bind(wx.EVT_CLOSE, self.on_close) # controlla la chiusura (x)
        
    # EVENTS:
    #-------------------------------------------------------------------#
    def on_close(self, event):
        self.Destroy()
    #-------------------------------------------------------------------#
    def on_Custom(self, event):
        """
        """
        ffmpeg = self.txtctrl_ffmpeg.GetValue()
        ffprobe = self.txtctrl_ffprobe.GetValue()
        ffplay = self.txtctrl_ffplay.GetValue()
        array = [ffmpeg,ffprobe,ffplay]
        empty = False
        noexists = False
        nobin = False
        
        if OS == 'Windows':
            biname = ['ffmpeg.exe','ffprobe.exe','ffplay.exe']
        else:
            biname = ['ffmpeg','ffprobe','ffplay']
            
        # gli eseguibili si trovano nei giusti campi di testo?
        # esempio: ffmpeg deve trovarsi dove la label corrisponde a ffmpeg
        # altrimenti sai che casino poi???
        match = [i for i, j in zip(array, biname) if os.path.basename(i) == j]
        
        if len(match) < 3:
            wx.MessageBox("Wrong entries on text fields:\n\n"
                          "ffmpeg: invalid pathname\n"
                          "ffprobe: invalid pathname\n"
                          "ffplay: invalid pathname\n\n",
                          'Entry errors', wx.ICON_ERROR, self)
            return

        for x in array:
            if not x:
                empty = True
                break
            if not os.path.isfile(x):
                noexists = x
                break
            if not os.path.basename(x) in biname:
                nobin = x
                break
        if empty:
            wx.MessageBox("You have not completed all the assignment fields.\n"
                          "Please, continue with settings.",
                          'Warning', wx.ICON_EXCLAMATION, self)
            return
        if noexists:
            wx.MessageBox("No such file '%s'.\n"
                          "Please, continue with settings." % x,
                          'Error', wx.ICON_ERROR, self)
            return
        if nobin:
            wx.MessageBox("'%s'\ndoes not match with:\n"
                          "%s\n"
                          "Please, continue with settings." % (x, biname),
                          'Error', wx.ICON_ERROR, self)
            return

        self.completion(ffmpeg, ffprobe, ffplay)

    #-------------------------------------------------------------------#
    def enablePaths(self, event):
        """
        """
        if self.ckbx_paths.IsChecked():
            self.txtctrl_ffmpeg.Enable()
            self.txtctrl_ffprobe.Enable()
            self.txtctrl_ffplay.Enable()
            self.searchBtn.Disable()
            self.customBtn.Enable()
        else:
            self.txtctrl_ffmpeg.Disable()
            self.txtctrl_ffprobe.Disable()
            self.txtctrl_ffplay.Disable()
            self.searchBtn.Enable()
            self.customBtn.Disable()
    #-------------------------------------------------------------------#
    def search(self, event):
        """
        Check for dependencies into your system (compatible with Linux, 
        MacOsX, Windows)
        [https://stackoverflow.com/questions/11210104/check-if-a-program-exists-
        from-a-python-script]
        Search the executable in the system, if fail stop the search, 
        otherwise write the executable pathname in the configuration file.
        """
        local = False
        if OS == 'Windows':
            biname = ['ffmpeg.exe','ffprobe.exe','ffplay.exe']
        elif OS == 'Darwin':
            biname = ['ffmpeg','ffprobe','ffplay']
            
        for required in biname:
            if which(required):
                print ("Check for: '%s' ..Ok" % required)
                no_which = False
            else:
                print ("Check for: '%s' ..Not Installed" % required)
                if OS == 'Darwin':
                    if os.path.isfile("/usr/local/bin/%s" % required):
                        local = True
                        no_which = False
                        break
                    else:
                        local = False
                        no_which = True
                        break
                elif OS == 'Windows':
                    no_which = True
                    break
        if no_which:
            for x in biname:
                if not os.path.isfile("%s/FFMPEG_BIN/bin/%s" % (PWD, x)):
                    noexists = True
                    break
                else:
                    noexists = False
            if noexists:
                wx.MessageBox("'%s' is not installed on the system.\n"
                          "Please, install it or set a new custom path." 
                          % required, 'Warning', wx.ICON_EXCLAMATION, self)
                return
            else:
                if wx.MessageBox("The Videomass2 system folder already "
                        "includes the binary executables of FFmpeg, "
                        "FFprobe and FFplay.\n\nDo you want to use them?", 
                        'Please Confirm - Videomass2',
                        wx.ICON_QUESTION |
                        wx.YES_NO, 
                        None) == wx.YES:
                    ffmpeg = "%s/FFMPEG_BIN/bin/%s" % (PWD, biname[0])
                    ffprobe = "%s/FFMPEG_BIN/bin/%s" % (PWD, biname[1])
                    ffplay = "%s/FFMPEG_BIN/bin/%s" % (PWD, biname[2])
                else:
                    return
        else:
            if local:
                ffmpeg = "/usr/local/bin/ffmpeg"
                ffprobe = "/usr/local/bin/ffprobe"
                ffplay = "/usr/local/bin/ffplay"
            else:
                ffmpeg = which(biname[0])
                ffprobe = which(biname[1])
                ffplay = which(biname[2])
        
        self.completion(ffmpeg, ffprobe, ffplay)
    #-------------------------------------------------------------------#
    
    def completion(self, ffmpeg, ffprobe, ffplay):
        """
        """
        rowsNum = []#rows number list
        dic = {} # used for debug
        with open (filename, 'r') as f:
            full_list = f.readlines()
        for a,b in enumerate(full_list):
            if not b.startswith('#'):
                if not b == '\n':
                    rowsNum.append(a)

        full_list[rowsNum[8]] = '%s\n' % ffmpeg
        full_list[rowsNum[10]] = '%s\n' % ffprobe
        full_list[rowsNum[12]] = '%s\n' % ffplay
        
        with open (filename, 'w') as fileconf:
            for i in full_list:
                fileconf.write('%s' % i)
            
        wx.MessageBox(u"\nWizard completed successfully.\n"
                       "Restart Videomass2 now.\n\nThank You!", 
                       "That's all folks!")   
        self.Destroy()
        
