# -*- coding: UTF-8 -*-

#########################################################
# Name: main_frame.py
# Porpose: top window main frame
# Author: Gianluca Pernigoto <jeanlucperni@gmail.com>
# Copyright: (c) 2018/2019) Gianluca Pernigoto <jeanlucperni@gmail.com>
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

# Rev (01) 09/july/2018
# Rev (02) 11/October/2018
#########################################################

import wx
import wx.lib.agw.gradientbutton as GB
import webbrowser
from vdms_DIALOGS import dialog_tools, settings, infoprg
from vdms_PANELS import dragNdrop, presets_mng_panel, video_conv, audio_conv
from vdms_IO import IO_tools

# set widget colours in some case with html rappresentetion:
azure = '#d9ffff' # rgb form (wx.Colour(217,255,255))
yellow = '#a29500'
red = '#ea312d'
orange = '#f28924'
greenolive = '#8aab3c'

########################################################################
class MainFrame(wx.Frame):
    """
    This is the main frame top window for panels implementation.
    Currently it host four panels, three of which are instantiated 
    in the init constructor. The fourth panel is instantiated in an 
    appropriate instance method. (see switch_Process method doc strings)
    """
    def __init__(self, setui, fileconf, path_confdir, PWD, 
                 ffmpeg_link, ffprobe_link, ffplay_link,
                 pathicons):
        """
        NOTE: 'path_srcShare' is a current work directory of Videomass2 
               program. How it can be localized depend if Videomass2 is 
               run as portable program or installated program.
        """

        self.videomass_icon = pathicons[0]
        self.icon_presets = pathicons[1]
        self.icon_switchvideomass = pathicons[2]
        self.icon_process = pathicons[3]
        self.icon_help = pathicons[4]
        self.icon_headphones = pathicons[5]
        self.icon_import = pathicons[6]
        #self.helping = setui[5]# path contestual help for helping:
        self.OS = setui[0]# ID of the operative system:
        path_srcShare = setui[1]# share dir (are where the origin files?):
        
        #---------------------------#
        self.threads = fileconf[2]#ffmpeg option, set the cpu threads
        self.cpu_used = fileconf[3]
        self.ffmpeg_log = ''#fileconf[3]
        self.save_log = fileconf[4]
        self.path_log = fileconf[5]
        self.loglevel_type = fileconf[6]# marks as single process
        self.loglevel_batch = ''#fileconf[7]# marks as batch process
        self.ffmpeg_check = fileconf[7]
        self.ffprobe_check = fileconf[9]
        self.ffplay_check = fileconf[11]
        self.ffmpeg_link = ffmpeg_link
        self.ffprobe_link = ffprobe_link
        self.ffplay_link = ffplay_link
        self.writeline_exec = fileconf[13]
        self.iconset = fileconf[14]
        #-------------------------------#
        self.import_clicked = ''#when clicking on item in list control self-set 
        self.post_process = []# at the end of any process put file for play/metadata
        self.file_sources = []# list of items in list control
        self.file_destin = ''# path name for file saved destination
        self.panelshown = '' # gives current (previusly) panel shown
        self.time_seq = ''
        self.duration = []

        wx.Frame.__init__(self, None, -1, style=wx.DEFAULT_FRAME_STYLE)
        #----------- panel toolbar buttons
        self.btnpanel = wx.Panel(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        
        infoIbmp = wx.Bitmap(pathicons[7], wx.BITMAP_TYPE_ANY)
        previewbmp = wx.Bitmap(pathicons[8], wx.BITMAP_TYPE_ANY)
        cutbmp = wx.Bitmap(pathicons[9], wx.BITMAP_TYPE_ANY)
        saveprfbmp = wx.Bitmap(pathicons[12], wx.BITMAP_TYPE_ANY)
        newprfbmp = wx.Bitmap(pathicons[13], wx.BITMAP_TYPE_ANY)
        delprfbmp = wx.Bitmap(pathicons[14], wx.BITMAP_TYPE_ANY)
        editprfbmp = wx.Bitmap(pathicons[15], wx.BITMAP_TYPE_ANY)
        
        
        
        self.btn_metaI = GB.GradientButton(self.btnpanel,
                                           size=(-1,25),
                                           bitmap=infoIbmp, 
                                           label="Show Metadata")
        self.btn_metaI.SetBaseColours(startcolour=wx.Colour(158,201,232), 
                                      foregroundcolour=wx.Colour(28,28,28))
        self.btn_metaI.SetBottomEndColour(wx.Colour(255,255,255))
        self.btn_metaI.SetBottomStartColour(wx.Colour(255,255,255))
        self.btn_metaI.SetTopStartColour(wx.Colour(255,255,255))
        self.btn_metaI.SetTopEndColour(wx.Colour(255,255,255))
        
        self.btn_playO = GB.GradientButton(self.btnpanel,
                                           size=(-1,25),
                                           bitmap=previewbmp, 
                                           label="Preview")
        self.btn_playO.SetBaseColours(startcolour=wx.Colour(158,201,232), 
                                      foregroundcolour=wx.Colour(28,28,28))
        self.btn_playO.SetBottomEndColour(wx.Colour(255,255,255))
        self.btn_playO.SetBottomStartColour(wx.Colour(255,255,255))
        self.btn_playO.SetTopStartColour(wx.Colour(255,255,255))
        self.btn_playO.SetTopEndColour(wx.Colour(255,255,255))
        
        self.btn_duration = GB.GradientButton(self.btnpanel,
                                              size=(-1,25),
                                              bitmap=cutbmp, 
                                              label="Duration")
        self.btn_duration.SetBaseColours(startcolour=wx.Colour(158,201,232), 
                                    foregroundcolour=wx.Colour(28,28,28))
        self.btn_duration.SetBottomEndColour(wx.Colour(255,255,255))
        self.btn_duration.SetBottomStartColour(wx.Colour(255,255,255))
        self.btn_duration.SetTopStartColour(wx.Colour(255,255,255))
        self.btn_duration.SetTopEndColour(wx.Colour(255,255,255))
        
        self.btn_saveprf = GB.GradientButton(self.btnpanel,
                                              size=(-1,25),
                                              bitmap=saveprfbmp, 
                                              label="Save As Profile")
        self.btn_saveprf.SetBaseColours(startcolour=wx.Colour(158,201,232), 
                                    foregroundcolour=wx.Colour(28,28,28))
        self.btn_saveprf.SetBottomEndColour(wx.Colour(255,255,255))
        self.btn_saveprf.SetBottomStartColour(wx.Colour(255,255,255))
        self.btn_saveprf.SetTopStartColour(wx.Colour(255,255,255))
        self.btn_saveprf.SetTopEndColour(wx.Colour(255,255,255))
        
        self.btn_newprf = GB.GradientButton(self.btnpanel,
                                              size=(-1,25),
                                              bitmap=newprfbmp, 
                                              label="New..")
        self.btn_newprf.SetBaseColours(startcolour=wx.Colour(158,201,232), 
                                    foregroundcolour=wx.Colour(28,28,28))
        self.btn_newprf.SetBottomEndColour(wx.Colour(255,255,255))
        self.btn_newprf.SetBottomStartColour(wx.Colour(255,255,255))
        self.btn_newprf.SetTopStartColour(wx.Colour(255,255,255))
        self.btn_newprf.SetTopEndColour(wx.Colour(255,255,255))
        
        self.btn_delprf = GB.GradientButton(self.btnpanel,
                                              size=(-1,25),
                                              bitmap=delprfbmp, 
                                              label="Delete..")
        self.btn_delprf.SetBaseColours(startcolour=wx.Colour(158,201,232), 
                                    foregroundcolour=wx.Colour(28,28,28))
        self.btn_delprf.SetBottomEndColour(wx.Colour(255,255,255))
        self.btn_delprf.SetBottomStartColour(wx.Colour(255,255,255))
        self.btn_delprf.SetTopStartColour(wx.Colour(255,255,255))
        self.btn_delprf.SetTopEndColour(wx.Colour(255,255,255))
        
        self.btn_editprf = GB.GradientButton(self.btnpanel,
                                              size=(-1,25),
                                              bitmap=editprfbmp, 
                                              label="Edit..")
        self.btn_editprf.SetBaseColours(startcolour=wx.Colour(158,201,232), 
                                    foregroundcolour=wx.Colour(28,28,28))
        self.btn_editprf.SetBottomEndColour(wx.Colour(255,255,255))
        self.btn_editprf.SetBottomStartColour(wx.Colour(255,255,255))
        self.btn_editprf.SetTopStartColour(wx.Colour(255,255,255))
        self.btn_editprf.SetTopEndColour(wx.Colour(255,255,255))

        #self.btnpanel.SetBackgroundColour(wx.Colour(97, 204, 199))
        self.btnpanel.SetBackgroundColour(wx.Colour(205, 235, 222))
        #---------- others panel instances:
        self.PrstsPanel = presets_mng_panel.PresetsPanel(self, path_srcShare, 
                                                         path_confdir, PWD, 
                                                         self.threads, 
                                                         self.cpu_used,
                                                         self.loglevel_type, 
                                                         self.ffmpeg_link, 
                                                         self.writeline_exec,
                                                         self.OS,
                                                         )
        self.VconvPanel = video_conv.Video_Conv(self, self.ffmpeg_link,
                                                self.ffplay_link,
                                                self.threads, 
                                                self.cpu_used,
                                                self.loglevel_type,
                                                self.OS,
                                                pathicons[10],# icon playfilters
                                                pathicons[11],# icon resetfilters
                                                pathicons[16],# icon resize
                                                pathicons[17],# icon crop
                                                pathicons[18],# icon rotate
                                                pathicons[19],# icon deinterlace
                                                pathicons[20],# icon ic_denoiser
                                                pathicons[21],# icon analyzes
                                                pathicons[22],# icon settings
                                                )
        self.AconvPanel = audio_conv.Audio_Conv(self, self.ffmpeg_link, 
                                                self.threads,
                                                self.cpu_used,
                                                self.loglevel_type, 
                                                self.ffprobe_link,
                                                self.OS,
                                                pathicons[21],# icon analyzes
                                                pathicons[22],# icon settings
                                                )

        self.DnD = dragNdrop.DnDPanel(self, self.ffprobe_link) # dragNdrop panel
        
        self.PrstsPanel.Hide()
        self.VconvPanel.Hide()
        self.AconvPanel.Hide()
        # Layout toolbar buttons:
        self.DnDsizer = wx.BoxSizer(wx.VERTICAL) # sizer base global
        grid_pan = wx.FlexGridSizer(1, 7, 0, 0)
        grid_pan.Add(self.btn_metaI, 0, wx.CENTER|wx.ALL, 5)
        grid_pan.Add(self.btn_playO, 0, wx.CENTER|wx.ALL, 5)
        grid_pan.Add(self.btn_duration, 0, wx.CENTER|wx.ALL, 5)
        grid_pan.Add(self.btn_saveprf, 0, wx.CENTER|wx.ALL, 5)
        grid_pan.Add(self.btn_newprf, 0, wx.CENTER|wx.ALL, 5)
        grid_pan.Add(self.btn_delprf, 0, wx.CENTER|wx.ALL, 5)
        grid_pan.Add(self.btn_editprf, 0, wx.CENTER|wx.ALL, 5)
        self.btnpanel.SetSizer(grid_pan) # set panel
        self.DnDsizer.Add(self.btnpanel, 0, wx.EXPAND, 0)
        # Layout externals panels:
        self.DnDsizer.Add(self.DnD, 1, wx.EXPAND|wx.ALL, 0)
        self.DnDsizer.Add(self.PrstsPanel, 1, wx.EXPAND|wx.ALL, 0)
        self.DnDsizer.Add(self.VconvPanel, 1, wx.EXPAND|wx.ALL, 0)
        self.DnDsizer.Add(self.AconvPanel, 1, wx.EXPAND|wx.ALL, 0)
        
        #----------------------Set Properties----------------------#
        self.SetTitle("Videomass2")
        self.btn_playO.Hide()
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap(self.videomass_icon, wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)
        if self.OS == 'Darwin':
            self.SetSize((920, 435))
        elif self.OS == 'Linux':
            self.SetSize((900, 530))
        elif self.OS == 'Windows':
            self.SetSize((900, 530))
        #self.Centre()
        #self.CentreOnScreen() # se lo usi, usa CentreOnScreen anziche Centre
        self.SetSizer(self.DnDsizer)
        self.Layout()
        
        # Tooltips:
        self.btn_duration.SetToolTipString('Sets a global time sequences to '
                                        'apply at any media file with duration.'
                                           )
        self.btn_metaI.SetToolTipString("Show information about the metadata "
                                        "of the selected imported file." 
                                        )
        self.btn_playO.SetToolTipString("Preview exported files. Reproduction "
                                        "exported file when finish encoding."
                                        )
        self.btn_saveprf.SetToolTipString("Save as profile with the current "
                                        "settings of this panel."
                                        )
        self.btn_newprf.SetToolTipString("Create a new profile from yourself "
                                        "and save it in the selected preset."
                                        )
        self.btn_delprf.SetToolTipString("Delete the selected profile."
                                        )
        self.btn_editprf.SetToolTipString("Edit the selected profile."
                                          )
        # menu bar
        self.videomass_menu_bar()
        ## tool bar main
        self.videomass_tool_bar()
        self.Setup_items_bar()
        # status bar
        self.sb = self.CreateStatusBar(1)
        
        #---------------------- Binding (EVT) ----------------------#
        self.DnD.ckbx_dir.Bind(wx.EVT_CHECKBOX, self.onCheckBox)
        self.DnD.btn_save.Bind(wx.EVT_BUTTON, self.onCustomSave)
        self.Bind(wx.EVT_BUTTON, self.Cut_range, self.btn_duration)
        self.Bind(wx.EVT_BUTTON, self.Saveprofile, self.btn_saveprf)
        self.Bind(wx.EVT_BUTTON, self.Newprofile, self.btn_newprf)
        self.Bind(wx.EVT_BUTTON, self.Delprofile, self.btn_delprf)
        self.Bind(wx.EVT_BUTTON, self.Editprofile, self.btn_editprf)
        self.Bind(wx.EVT_BUTTON, self.ImportInfo, self.btn_metaI)
        self.Bind(wx.EVT_BUTTON, self.ExportPlay, self.btn_playO)
        #self.Bind(wx.EVT_SHOW, self.panelShown)
        #self.DnDPanel.fileListCtrl.Bind(wx.EVT_LIST_INSERT_ITEM, self.new_isertion)
        self.Bind(wx.EVT_CLOSE, self.on_close) # controlla la chiusura (x)
        #-----------------------------------------------------------#
        self.statusbar_msg('Drag and Drop - panel',None)#set default statusmsg
        
    #-------------------Status bar popolate--------------------#
    def statusbar_msg(self, msg, color):
        """
        set the status-bar with messages and color types
        """
        if color == None:
            self.sb.SetBackgroundColour(wx.NullColour)
        else:
            self.sb.SetBackgroundColour(color)
        self.sb.SetStatusText(msg)
        self.sb.Refresh()
    
    #---------------------- Used Methods ----------------------#
    # The Used Methods are called from the dragNdrop panel
    def Disable_ToolBtn(self):
        """
        Start with default or by deleting listcontrol from dragNdrop panel
        """
        self.toolbar.EnableTool(wx.ID_FILE3, False)
        self.toolbar.EnableTool(wx.ID_FILE5, False)
        self.toolbar.EnableTool(wx.ID_FILE6, False)
        self.toolbar.EnableTool(wx.ID_FILE7, False)
        self.toolbar.EnableTool(wx.ID_OK, False)
    #------------------------------------------------------------------#
    def Enable_ToolBtn(self):
        """
        Enable preset manager, video converter and 
        audio converter buttons
        """
        self.toolbar.EnableTool(wx.ID_FILE5, True)
        self.toolbar.EnableTool(wx.ID_FILE6, True)
        self.toolbar.EnableTool(wx.ID_FILE7, True)
    #------------------------------------------------------------------#
    def Setup_items_bar(self):
        """
        When switch between panels, disable/enable some item on menu bar 
        and tool bar. Also at the program start, the DnDPanel is show and 
        then take its setting
        """
        if self.DnD.IsShown():
            self.file_open.Enable(False), self.saveme.Enable(False), 
            self.restore.Enable(False), self.default.Enable(False), 
            self.default_all.Enable(False), self.refresh.Enable(False), 
            self.btn_newprf.Hide(), self.btn_saveprf.Hide(), 
            self.btn_delprf.Hide(), self.btn_editprf.Hide(),
            
        elif self.PrstsPanel.IsShown():
            self.file_open.Enable(True), self.saveme.Enable(True), 
            self.restore.Enable(True), self.default.Enable(True), 
            self.default_all.Enable(True), self.refresh.Enable(True), 
            self.btn_newprf.Show(), self.btn_saveprf.Hide(), 
            self.btn_delprf.Show(), self.btn_editprf.Show(), 
            self.toolbar.EnableTool(wx.ID_FILE3, True)
            self.toolbar.EnableTool(wx.ID_FILE6, True)
            self.toolbar.EnableTool(wx.ID_FILE7, True)
            self.toolbar.EnableTool(wx.ID_FILE5, False)
            self.toolbar.EnableTool(wx.ID_OK, True)
            self.Layout()
            
        elif self.VconvPanel.IsShown():
            self.file_open.Enable(True), self.saveme.Enable(False),
            self.restore.Enable(False), self.default.Enable(False), 
            self.default_all.Enable(False), self.refresh.Enable(False), 
            self.btn_newprf.Hide(), self.btn_saveprf.Show(), 
            self.btn_delprf.Hide(), self.btn_editprf.Hide(), 
            self.toolbar.EnableTool(wx.ID_FILE3, True)
            self.toolbar.EnableTool(wx.ID_FILE5, True)
            self.toolbar.EnableTool(wx.ID_FILE7, True)
            self.toolbar.EnableTool(wx.ID_FILE6, False)
            self.toolbar.EnableTool(wx.ID_OK, True)
            self.Layout()
            
        elif self.AconvPanel.IsShown():
            self.file_open.Enable(True), self.saveme.Enable(False),
            self.restore.Enable(False), self.default.Enable(False), 
            self.default_all.Enable(False), self.refresh.Enable(False), 
            self.btn_newprf.Hide(), self.btn_saveprf.Show(), 
            self.btn_delprf.Hide(), self.btn_editprf.Hide(), 
            self.toolbar.EnableTool(wx.ID_FILE3, True)
            self.toolbar.EnableTool(wx.ID_FILE5, True)
            self.toolbar.EnableTool(wx.ID_FILE6, True)
            self.toolbar.EnableTool(wx.ID_FILE7, False)
            self.toolbar.EnableTool(wx.ID_OK, True)
            self.Layout()
            
        elif self.ProcessPanel.IsShown():
            self.file_open.Enable(False), self.saveme.Enable(False), 
            self.restore.Enable(False), self.default.Enable(False), 
            self.default_all.Enable(False), self.refresh.Enable(False), 
            #Disable all top menu bar :
            [self.menuBar.EnableTop(x, False) for x in range(0,3)]
            #Disable the tool bar
            self.toolbar.EnableTool(wx.ID_FILE3, False)
            self.toolbar.EnableTool(wx.ID_FILE5, False)
            self.toolbar.EnableTool(wx.ID_FILE6, False)
            self.toolbar.EnableTool(wx.ID_FILE7, False)
            self.toolbar.EnableTool(wx.ID_OK, False)

    #------------------------------------------------------------------#
    def importClicked_enable(self, path):
        """
        when click with the mouse on a control list item, 
        enable Metadata Info and file reproduction menu
        """
        self.btn_metaI.SetBottomEndColour(wx.Colour(0, 240, 0))
        self.import_clicked = path# used for play and metadata
        
    #------------------------------------------------------------------#
    def importClicked_disable(self):
        """
        Disable streams imported menu
        """
        self.btn_metaI.SetBottomEndColour(wx.Colour(255,255,255))
        self.import_clicked = ''
        
    #------------------------------------------------------------------#
    def postExported_enable(self):
        """
        Enable menu Streams items for output play and metadata
        info
        """
        if not self.btn_playO.IsShown():
            self.btn_playO.Show()
            self.Layout()
        self.btn_playO.SetBottomEndColour(wx.Colour(0, 240, 0))

    #---------------------- Event handler (callback) ------------------#
    # This series of events are interceptions of the dragNdrop panel
    #-------------------------------- Options ----------------------------#
    def Cut_range(self, event):
        """
        Call dialog for Set a time selection cutting on all imported
        media. The values persist so that they are not reset.
        """
        data = ''

        dial = dialog_tools.Cut_Range(self, self.time_seq)
        retcode = dial.ShowModal()
        if retcode == wx.ID_OK:
            data = dial.GetValue()
            if data == '-ss 00:00:00 -t 00:00:00':
                data = ''
                self.btn_duration.SetBottomEndColour(wx.Colour(255,255,255))
            else:
                self.btn_duration.SetBottomEndColour(wx.Colour(0, 240, 0))
            self.time_seq = data
        else:
            dial.Destroy()
            return
    #------------------------------ Menu  Streams -----------------------#
    def ImportPlay(self):
        """
        Redirect input file clicked at stream_play for playback feature.
        This feature is available by context menu in drag n drop panel only.
        """
        filepath = self.import_clicked
        IO_tools.stream_play(filepath, 
                             self.time_seq, 
                             self.ffplay_link, 
                             self.loglevel_type, 
                             self.OS,
                             )
    #------------------------------------------------------------------#
    def ImportInfo(self, event):
        """
        Redirect input file clicked at stream_info for metadata display
        """
        filepath = self.import_clicked
        if not filepath:
            wx.MessageBox("No file selected into Drag and Drop list", 
                          'Videomass2', wx.ICON_EXCLAMATION, self)
            return
        title = 'Metadata of selected media - Videomass2'
        IO_tools.stream_info(title, 
                             filepath, 
                             self.ffprobe_link,
                             )
    #------------------------------------------------------------------#
    def ExportPlay(self, event):
        """
        Playback functionality for exported files, useful for result 
        testing. The first one exported of the list will be reproduced.
        """
        if not self.post_process:
            wx.MessageBox("No files exported with `Start Encoding` yet", 
                          'Videomass2', wx.ICON_EXCLAMATION, self)
            return

        IO_tools.stream_play(self.post_process,
                             '', 
                             self.ffplay_link, 
                             self.loglevel_type,
                             self.OS,
                             )
    #------------------------------------------------------------------#
    def Saveprofile(self, event):
        """
        Store new profile with same current settings of the panel shown 
        (Video Conversion & Audio Conversion)..
        Every modification on the panel shown will be reported when saving 
        a new profile.
        """
        if self.VconvPanel.IsShown():
            self.VconvPanel.Addprof()
        elif self.AconvPanel.IsShown():
            self.AconvPanel.Addprof()
        else:
            print 'Error, no panels shown - Videomass2'
    #------------------------------------------------------------------#
    def Newprofile(self, event):
        """
        Store new profile in the selected preset of the presets manager
        panel. The list is reloaded automatically after pressed ok button 
        in the dialog for update view.
        """
        if self.PrstsPanel.IsShown():
            self.PrstsPanel.Addprof()
        else:
            print 'Error, no presets manager panel shown - Videomass2'
    #------------------------------------------------------------------#
    def Delprofile(self, event):
        """
        Delete the selected preset of the presets manager
        panel.
        """
        if self.PrstsPanel.IsShown():
            self.PrstsPanel.Delprof()
    #------------------------------------------------------------------#
    def Editprofile(self, event):
        """
        Edit selected item in the list control of the presets manager
        panel. The list is reloaded automatically after pressed ok button 
        in the dialog.
        """
        if self.PrstsPanel.IsShown():
            self.PrstsPanel.Editprof(self)
    #-----------------------------------------------------------------#
    def onCheckBox(self, event):
        """
        Intercept the Checkbox event in the dragNdrop panel
        and set same file sources destination path
        """
        self.DnD.same_filedest()
        self.file_destin = self.DnD.file_dest
    #------------------------------------------------------------------#
    def onCustomSave(self, event):
        """
        Intercept the button 'save' event in the dragNdrop panel
        and set file custom destination path
        """
        self.DnD.on_custom_save()
        self.file_destin = self.DnD.file_dest
    #------------------------------------------------------------------#
    def on_close(self, event):
        """
        destroy the videomass.
        """
        self.Destroy()
    #------------------------------------------------------------------#

############################### BUILD THE MENU BAR  ########################
    def videomass_menu_bar(self):
        """
        Make a menu bar. Per usare la disabilitazione di un menu item devi
        prima settare l'attributo self sull'item interessato - poi lo gestisci
        con self.item.Enable(False) per disabilitare o (True) per abilitare.
        Se vuoi disabilitare l'intero top di items fai per esempio:
        self.menuBar.EnableTop(6, False) per disabilitare la voce Help.
        """
        self.menuBar = wx.MenuBar()
        
        ####----------------------- file
        fileButton = wx.Menu()
        
        self.file_open = fileButton.Append(wx.ID_OPEN, "Add File.. ", 
                        "Files import with drag and drop")
        self.file_save = fileButton.Append(wx.ID_SAVE, "Choose a Destination " 
                                                        "folder..", 
                        "Choice a folder where save processed files")
        fileButton.AppendSeparator()
        self.saveme = fileButton.Append(wx.ID_REVERT_TO_SAVED,
                                 "Save the current preset as separated file",
                       "Make a back-up of the selected preset on combobox"
                                    )
        self.restore = fileButton.Append(wx.ID_REPLACE, "Restore a previously "
                                                "saved preset", 
                "Replace the selected preset with other saved custom preset."
                                                )
        self.default = fileButton.Append(wx.ID_ANY, "Reset the current preset ",
                            "Replace the selected preset with default values."
                                                )
        fileButton.AppendSeparator()
        
        self.default_all = fileButton.Append(wx.ID_UNDO, "Reset all presets ",
                         "Revert all presets to default values"
                                                )
        
        fileButton.AppendSeparator()
        self.refresh = fileButton.Append(wx.ID_REFRESH, "Reload presets list", 
              "It is not necessary to use this function, but sometimes it can "
              "be useful")
        fileButton.AppendSeparator()
        exitItem = fileButton.Append(wx.ID_EXIT, "Exit", "Close Videomass2")
        self.menuBar.Append(fileButton,"File")
        
        ####------------------ setup button
        setupButton = wx.Menu()

        self.showtoolbar = setupButton.Append(wx.ID_ANY, "Show Tool Bar", 
                                       "Show tool bar view", wx.ITEM_CHECK)
        setupButton.Check(self.showtoolbar.GetId(), True)
        
        self.showpanelbar = setupButton.Append(wx.ID_ANY, "Show Buttons Bar", 
                                "Show or hide buttons bar view", wx.ITEM_CHECK)
        setupButton.Check(self.showpanelbar.GetId(), True)

        setupButton.AppendSeparator()
        setupItem = setupButton.Append(wx.ID_PREFERENCES, "Setup", 
                                       "General Settings")
        
        self.menuBar.Append(setupButton,"Preferences")
        
        ####------------------ help buton
        helpButton = wx.Menu()
        helpItem = helpButton.Append( wx.ID_HELP, "User Guide", "Guide")
        infoItem = helpButton.Append(wx.ID_ABOUT, "About Videomass2", "About")
        self.menuBar.Append(helpButton,"Help")

        self.SetMenuBar(self.menuBar)
        
        #-----------------------Binding menu bar-------------------------#
        #----FILE----
        self.Bind(wx.EVT_MENU, self.File_Open, self.file_open)
        self.Bind(wx.EVT_MENU, self.File_Save, self.file_save)
        self.Bind(wx.EVT_MENU, self.Saveme, self.saveme)
        self.Bind(wx.EVT_MENU, self.Restore, self.restore)
        self.Bind(wx.EVT_MENU, self.Default, self.default)
        self.Bind(wx.EVT_MENU, self.Default_all, self.default_all)
        self.Bind(wx.EVT_MENU, self.Refresh, self.refresh)
        self.Bind(wx.EVT_MENU, self.Quiet, exitItem)
        #----SETUP----
        self.Bind(wx.EVT_MENU, self.Show_toolbar, self.showtoolbar)
        self.Bind(wx.EVT_MENU, self.Show_panelbar, self.showpanelbar)
        self.Bind(wx.EVT_MENU, self.Setup, setupItem)
        #----HELP----
        self.Bind(wx.EVT_MENU, self.Helpme, helpItem)
        self.Bind(wx.EVT_MENU, self.Info, infoItem)

    #-------------------Menu Bar Event handler (callback)----------------------#
    #-------------------------- Menu  File -----------------------------#
    def File_Open(self, event):
        """
        Open choice dialog input
        """
        self.File_import(self)
    #--------------------------------------------------#
    def File_Save(self, event):
        """
        Open choice dialog output
        """
        self.DnD.on_custom_save()
    #--------------------------------------------------#
    def Saveme(self, event):
        """
        call method for save a single file copy of preset.
        """
        if self.PrstsPanel.IsShown():
            self.PrstsPanel.Saveme()
    #--------------------------------------------------#
    def Restore(self, event):
        """
        call restore a single preset file in the path presets of the program
        """
        if self.PrstsPanel.IsShown():
            self.PrstsPanel.Restore()
    #--------------------------------------------------#
    def Default(self, event):
        """
        call copy the single original preset file into the configuration
        folder. This replace new personal changes make at profile.
        """ 
        if self.PrstsPanel.IsShown():
            self.PrstsPanel.Default()
    #--------------------------------------------------#
    def Default_all(self, event):
        """
        call restore all preset files in the path presets of the program
        """
        if self.PrstsPanel.IsShown():
            self.PrstsPanel.Default_all()
    #--------------------------------------------------#
    def Refresh(self, event):
        """ 
        call Pass to reset_list function for re-charging list
        """
        if self.PrstsPanel.IsShown():
            self.PrstsPanel.Refresh()
    #--------------------------------------------------#
    def Quiet(self, event):
        """
        destroy the videomass.
        """
        self.Destroy()
                
    #------------------------ Menu  Preferences -------------------------#
    def Show_toolbar(self, event):
        """
        Show the tool bar and disable Show toolbar menu item
        """
        if self.showtoolbar.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()
            
        self.Layout()
    #--------------------------------------------------------------------#
    def Show_panelbar(self, event):
        """
        Show or Hide the buttons bar
        """
        if self.showpanelbar.IsChecked():
            self.btnpanel.Show()
        else:
            self.btnpanel.Hide()
            
        self.Layout()
    #------------------------------------------------------------------#
    def Setup(self, event):
        """
        Call the module setup for setting preferences
        """
        #self.parent.Setup(self)
        setup_dlg = settings.Setup(self, self.threads, self.cpu_used,
                                     self.save_log, self.path_log, 
                                     self.ffmpeg_link, self.ffmpeg_check,
                                     self.ffprobe_link, self.ffprobe_check, 
                                     self.ffplay_link, self.ffplay_check, 
                                     self.writeline_exec, self.OS, 
                                     self.iconset,
                                     )
        setup_dlg.ShowModal()
        
    #---------------------------- Menu Edit ----------------------------#
    def Helpme(self, event):
        """ """
        #wx.MessageBox("La guida al programma deve venire sviluppata a breve.")
        #self.on_manual(self)
        #self.parent.on_help(self)
        page = 'https://jeanslack.github.io/Videomass2/videomass2_use.html'
        webbrowser.open(page)

    #------------------------------------------------------------------#
    def Info(self, event):
        """
        Display the program informations and developpers
        """
        infoprg.info(self, self.videomass_icon)
        
###############################  BUILD THE TOOL BAR  ########################
    def videomass_tool_bar(self):
        """
        Makes and attaches the view toolsBtn bar
        """
        #--------- Properties
        self.toolbar = self.CreateToolBar(style=(wx.TB_HORZ_LAYOUT | wx.TB_TEXT))
        self.toolbar.SetToolBitmapSize((32,32))
        self.toolbar.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        
        #-------- Import button
        icn_import = self.toolbar.AddLabelTool(wx.ID_FILE3, 'Add File',
                                         wx.Bitmap(self.icon_import),
                                                )
        self.toolbar.EnableTool(wx.ID_FILE3, False)
        self.toolbar.AddSeparator()
        
        #-------- Switch at preset manager
        prs_mng = self.toolbar.AddLabelTool(wx.ID_FILE5, 'Presets Manager', 
                                    wx.Bitmap(self.icon_presets)
                                                )
        self.toolbar.EnableTool(wx.ID_FILE5, False)
        self.toolbar.AddSeparator()
        
        #-------- Switch at videomass
        switch_video = self.toolbar.AddLabelTool(wx.ID_FILE6, 
                    'Video Conversions', wx.Bitmap(self.icon_switchvideomass)
                                                )
        self.toolbar.EnableTool(wx.ID_FILE6, False)
        self.toolbar.AddSeparator()

        #-------- Switch Advanced audio
        switch_audio = self.toolbar.AddLabelTool(wx.ID_FILE7, 
                    'Audio Conversions',  wx.Bitmap(self.icon_headphones)
                                                )
        self.toolbar.EnableTool(wx.ID_FILE7, False)
        self.toolbar.AddSeparator()
        
        # ------- Run process button
        run_coding = self.toolbar.AddLabelTool(wx.ID_OK, 'Start Encoding', 
                                    wx.Bitmap(self.icon_process)
                                                )
        self.toolbar.EnableTool(wx.ID_OK, False)
        self.toolbar.AddSeparator()
        
        #------- help button
        help_contest = self.toolbar.AddLabelTool(wx.ID_ANY, 'Help', 
                                    wx.Bitmap(self.icon_help)
                                                )
        # finally, create it
        self.toolbar.Realize()
        
        #----------------- Tool Bar Binding (evt)-----------------------#
        self.Bind(wx.EVT_TOOL, self.File_import, icn_import)
        self.Bind(wx.EVT_TOOL, self.Preset_Mng, prs_mng)
        self.Bind(wx.EVT_TOOL, self.switch_video_conv, switch_video)
        self.Bind(wx.EVT_TOOL, self.switch_audio_conv, switch_audio)
        self.Bind(wx.EVT_TOOL, self.Run_Coding, run_coding)
        self.Bind(wx.EVT_TOOL, self.Helpme, help_contest)

    #--------------- Tool Bar Callback (event handler) -----------------#
    #------------------------------------------------------------------#
    def File_import(self, event):
        """
        Show files import panel.
        """
        self.PrstsPanel.Hide(), self.VconvPanel.Hide(), self.AconvPanel.Hide()
        self.DnD.Show()
        self.Layout()
        self.statusbar_msg('Drag and Drop - panel', None)
        
        self.toolbar.EnableTool(wx.ID_FILE5, True)
        self.toolbar.EnableTool(wx.ID_FILE6, True)
        self.toolbar.EnableTool(wx.ID_FILE7, True)
        self.toolbar.EnableTool(wx.ID_FILE3, False)
        self.toolbar.EnableTool(wx.ID_OK, False)
        
        self.Setup_items_bar()
    #------------------------------------------------------------------#
    
    def Preset_Mng(self, event):
        """
        Show presets manager panel
        """
        self.panelshown = 'presets manager'
        self.file_sources = self.DnD.fileList[:]
        self.file_destin = self.DnD.file_dest
        
        self.DnD.Hide(), self.VconvPanel.Hide(), self.AconvPanel.Hide()
        self.PrstsPanel.Show(), self.Layout()

        self.statusbar_msg('Presets Manager - panel', None)
        self.Setup_items_bar()
    
        self.PrstsPanel.file_destin = self.file_destin
        if self.file_sources != self.PrstsPanel.file_sources:
            self.PrstsPanel.file_sources = self.file_sources
            self.duration = self.DnD.duration
    #------------------------------------------------------------------#
    def switch_video_conv(self, event):
        """
        Show Video converter panel
        """
        self.panelshown = 'video conversions'
        self.file_sources = self.DnD.fileList[:]
        self.file_destin = self.DnD.file_dest
        
        self.DnD.Hide(), self.PrstsPanel.Hide(), self.AconvPanel.Hide()
        self.VconvPanel.Show(), self.Layout()
        
        self.statusbar_msg('Video Conversion - panel', None)
        self.Setup_items_bar()

        self.VconvPanel.file_destin = self.file_destin
        if self.file_sources != self.VconvPanel.file_sources:
            self.VconvPanel.file_sources = self.file_sources
            self.VconvPanel.normalize_default()
            #self.VconvPanel.audio_default()
            self.duration = self.DnD.duration
    #------------------------------------------------------------------#
    #def switch_audio_conv(self, event):
    def switch_audio_conv(self, event):
        """
        Show Audio converter panel
        """
        self.panelshown = 'audio conversions'
        self.file_sources = self.DnD.fileList[:]
        self.file_destin = self.DnD.file_dest

        self.DnD.Hide(), self.PrstsPanel.Hide(), self.VconvPanel.Hide()
        self.AconvPanel.Show(), self.Layout()
        
        self.statusbar_msg('Audio Conversion - panel', None)
        self.Setup_items_bar()

        self.AconvPanel.file_destin = self.file_destin
        if self.file_sources != self.AconvPanel.file_sources:
            self.AconvPanel.file_sources = self.file_sources
            self.AconvPanel.normalization_disabled()
            self.duration = self.DnD.duration
            
    #------------------------------------------------------------------#
    def switch_Process(self, *varargs):
        """
        Show a panel for processing task only. 
        This is a panel that should not be instantiated at the beginning 
        of the main frame (as others) because otherwise it would immediately
        start running.
        """
        duration = self.DnD.duration[:] # the streams duration list
        
        if self.showpanelbar.IsChecked():
            self.btnpanel.Hide()# hide buttons bar if the user has shown it:

        IO_tools.process(self, varargs, 
                         self.path_log, 
                         self.panelshown, 
                         duration,
                         self.OS)
        #make the positioning:
        self.DnDsizer.Add(self.ProcessPanel, 1, wx.EXPAND|wx.ALL, 0)
        #Hide all others panels:
        self.DnD.Hide(), self.PrstsPanel.Hide(), self.VconvPanel.Hide()
        self.AconvPanel.Hide()
        #Show the panel:
        self.ProcessPanel.Show()
        self.Layout()
        self.SetTitle('..Start Encoding - Videomass2')

        self.Setup_items_bar()# call set default layout method
    #------------------------------------------------------------------#
    def Run_Coding(self, event):
        """
        By clicking the Start encoding button on the main frame, calls 
        the on_ok method of the corresponding panel shown, which calls 
        the 'switch_Process' method above.
        """
        if self.PrstsPanel.IsShown():
            self.PrstsPanel.on_ok()
        elif self.VconvPanel.IsShown():
            self.VconvPanel.on_ok()
        elif self.AconvPanel.IsShown():
            self.AconvPanel.on_ok()
            
    #------------------------------------------------------------------#
    def panelShown(self, panelshown):
        """
        When clicking 'close button' of the processing panel
        (see switch_Process method above), Retrieval at previous 
        panel showing and re-enables the functions provided by 
        the menu bar.
        """
        if panelshown == 'presets manager':
            self.ProcessPanel.Hide()
            self.Preset_Mng(self)
        elif panelshown == 'video conversions':
            self.ProcessPanel.Hide()
            self.switch_video_conv(self)
        elif panelshown == 'audio conversions':
            self.ProcessPanel.Hide()
            self.switch_audio_conv(self)
        # Enable all top menu bar:
        [self.menuBar.EnableTop(x, True) for x in range(0,3)]
        self.SetTitle("Videomass2")# set the appropriate title
        # show buttons bar if the user has shown it:
        if self.showpanelbar.IsChecked():
            self.btnpanel.Show()
            self.Layout()
        
        
        
