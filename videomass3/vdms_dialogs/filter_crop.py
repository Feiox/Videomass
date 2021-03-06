# -*- coding: UTF-8 -*-
# Name: filter_crop.py
# Porpose: Show dialog to get video crop values based on FFmpeg syntax
# Compatibility: Python3, wxPython Phoenix
# Author: Gianluca Pernigoto <jeanlucperni@gmail.com>
# Copyright: (c) 2018/2020 Gianluca Pernigoto <jeanlucperni@gmail.com>
# license: GPL3
# Rev: November.18.2020 *PEP8 compatible*
#########################################################

# This file is part of Videomass.

#    Videomass is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Videomass is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Videomass.  If not, see <http://www.gnu.org/licenses/>.

#########################################################
import wx
import webbrowser
# import wx.lib.masked as masked  # not work on macOSX
import wx.lib.statbmp
import os
import time
from videomass3.vdms_threads.generic_task import FFmpegGenericTask


class Actor(wx.lib.statbmp.GenStaticBitmap):
    """
    inspired from Robin Dunn discussion
    <https://discuss.wxpython.org/t/questions-about-rotation/34064>

    """
    def __init__(self, parent, bitmap,
                 idNum,  imgFile, **kwargs):
        """
        """
        wx.lib.statbmp.GenStaticBitmap.__init__(self, parent, -1,
                                                bitmap, **kwargs)
        self._parent = parent  ## if needed
        self._original_bmp = self._current_bmp = bitmap

        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def OnPaint(self, evt=None):
        """
        """
        dc = wx.PaintDC(self)  ## draw window boundary
        dc.Clear()
        dc.DrawBitmap(self._current_bmp, 0, 0, True)


    def onRedraw(self, x, y, width, height, w_ratio, h_ratio, pict):
        """
        Update Drawing: A transparent background rectangle in a bitmap
        for selections

        """
        self._original_bmp = wx.Bitmap(pict)
        img = self._original_bmp.ConvertToImage()
        img = img.Scale(w_ratio, h_ratio, wx.IMAGE_QUALITY_NORMAL)  ## use original size
        self._current_bmp = img.ConvertToBitmap()
        dc = wx.MemoryDC(self._current_bmp)
        dc.SetPen(wx.Pen('red', 1, wx.PENSTYLE_SOLID))
        r, g, b = (30,  30,  30)
        dc.SetBrush(wx.Brush(wx.Colour(r, g, b, 128)))
        dc.DrawRectangle(x, y, width, height)
        dc.SelectObject(wx.NullBitmap)
        self.Refresh(False)

    def makeBox(w_ratio, h_ratio, pict):
        """
        Create box with wx.dc (device context) and return a bitmap.
        This function is called only once during the instance of this class

        """
        bitmap = wx.Bitmap(pict)
        img = bitmap.ConvertToImage()
        img = img.Scale(w_ratio, h_ratio, wx.IMAGE_QUALITY_NORMAL)  ## use original size
        bmp = img.ConvertToBitmap()
        dc = wx.MemoryDC(bmp)
        dc.SelectObject(wx.NullBitmap)
        return wx.Bitmap(bmp)


class Crop(wx.Dialog):
    """
    A dialog tool to get data filtergraph for cropping
    videos or images with FFmpeg.

    """
    get = wx.GetApp()
    OS = get.OS
    TMP = get.TMP

    if get.THEME == 'Breeze-Blues':
        # breeze-blues
        #BACKGROUND = '#11303eff'  # solarized
        BACKGROUND = '#1b0413'
        PEN = 'green'

    elif get.THEME in get.DARKicons:
        # dark
        BACKGROUND = '#0c1217'  # dark deep blue
        PEN = 'green'
    else:
        # light
        BACKGROUND = '#e6e6faff'  # lavender
        PEN = 'green'

    # ------------------------------------------------------------------#

    def __init__(self, parent, fcrop, v_width, v_height, fname, duration):
        """
        self.panelrect is always set at height 360 px, in fact the width is
        adjusted accordingly but preserving the video aspect ratio.
        This fundamental ratio is given by the `self.h_ratio`
        attribute where the cropping rectangle adjustment will always
        be scaled to this constant. The values returned in the GetValue
        callback are the actual values for cropping.

        """
        # virtual cropping values for monitor preview
        self.width_dc = 0
        self.height_dc = 0
        self.y_dc = 0
        self.x_dc = 0
        # current video size
        self.v_width = v_width
        self.v_height = v_height
        # resizing values preserving aspect ratio for monitor
        self.h_ratio = (self.v_height / self.v_width) * 360  # get height
        self.w_ratio = (self.v_width / self.v_height) * self.h_ratio  #  get width

        self.video = fname
        name = os.path.splitext(os.path.basename(self.video))[0]
        self.frame = os.path.join('%s' % Crop.TMP, '%s.png' % name)

        if os.path.exists(self.frame):
            self.image = self.frame
        else:
            self.image = wx.Bitmap(self.w_ratio, self.h_ratio)  # make empty
        t = duration.split(':')
        h, m , s = ("%02d" % int(t[0]), "%02d" % int(t[1]),
                    "%02d" % float(t[2]))

        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)
        sizerBase = wx.BoxSizer(wx.VERTICAL)
        self.panelrect = wx.Panel(self, wx.ID_ANY,
                                  size=(self.w_ratio + 2, self.h_ratio + 2),
                                  style=wx.BORDER_SUNKEN
                                  )  # + 2 is the BORDER_SUNKEN offset
        self.bob = Actor(self.panelrect, Actor.makeBox(self.w_ratio,
                                                       self.h_ratio,
                                                       self.image), 1, "")
        sizerBase.Add(self.panelrect, 0, wx.TOP | wx.CENTER, 10)
        sizersize = wx.BoxSizer(wx.VERTICAL)
        sizerBase.Add(sizersize, 0, wx.ALL | wx.CENTER, 10)
        msg = _("Source size: {0} x {1} pixels").format(self.v_width,
                                                        self.v_height)
        label1 = wx.StaticText(self, wx.ID_ANY,(msg))
        sizersize.Add(label1, 0, wx.CENTER, 10)

        msg = _("Search for a specific frame [hours : minutes : seconds], max "
                "duration {}:{}:{}").format(h, m, s)
        sizer_load = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, (msg)),
                                       wx.HORIZONTAL)
        sizerBase.Add(sizer_load, 0, wx.ALL | wx.CENTRE, 10)
        self.hour = wx.SpinCtrl(self, wx.ID_ANY, '0', min=0, max=23,
                                style=wx.TE_PROCESS_ENTER)
        sizer_load.Add(self.hour, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        lab1 = wx.StaticText(self, wx.ID_ANY, (":"))
        lab1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        sizer_load.Add(lab1, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.minute = wx.SpinCtrl(self, wx.ID_ANY, '0', min=0, max=59,
                                  style=wx.TE_PROCESS_ENTER)
        sizer_load.Add(self.minute, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        lab2 = wx.StaticText(self, wx.ID_ANY, (":"))
        lab2.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        sizer_load.Add(lab2, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.seconds = wx.SpinCtrl(self, wx.ID_ANY, '0', min=0, max=59,
                                   style=wx.TE_PROCESS_ENTER)
        sizer_load.Add(self.seconds, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        btn_load = wx.Button(self, wx.ID_ANY, _("Load"))
        sizer_load.Add(btn_load, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        sizerLabel = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, (
                        _("Area selection and position setting in pixels"))),
                                       wx.VERTICAL)
        sizerBase.Add(sizerLabel, 1, wx.ALL | wx.EXPAND, 10)
        boxctrl = wx.BoxSizer(wx.VERTICAL)
        sizerLabel.Add(boxctrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        label_height = wx.StaticText(self, wx.ID_ANY, (_("Height")))
        boxctrl.Add(label_height, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL, 5
                    )
        self.crop_height = wx.SpinCtrl(self, wx.ID_ANY, "0",
                                       min=0, max=self.v_height, size=(-1, -1),
                                       style=wx.TE_PROCESS_ENTER
                                       )
        boxctrl.Add(self.crop_height, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL, 5
                    )
        grid_sizerBase = wx.FlexGridSizer(1, 5, 0, 0)
        boxctrl.Add(grid_sizerBase, 1, wx.EXPAND, 0)
        label_Y = wx.StaticText(self, wx.ID_ANY, ("Y"))
        grid_sizerBase.Add(label_Y, 0, wx.ALL |
                           wx.ALIGN_CENTER_HORIZONTAL |
                           wx.ALIGN_CENTER_VERTICAL, 5
                           )
        self.axis_Y = wx.SpinCtrl(self, wx.ID_ANY, "0",
                                  min=-1, max=self.v_height, size=(-1, -1),
                                  style=wx.TE_PROCESS_ENTER
                                  )
        grid_sizerBase.Add(self.axis_Y, 0, wx.ALL |
                           wx.ALIGN_CENTER_HORIZONTAL |
                           wx.ALIGN_CENTER_VERTICAL, 5
                           )
        self.btn_centre = wx.Button(self, wx.ID_ANY, _("Center"))
        grid_sizerBase.Add(self.btn_centre, 0, wx.ALL | wx.CENTRE , 35
                           )
        self.crop_width = wx.SpinCtrl(self, wx.ID_ANY, "0",
                                      min=0,  max=self.v_width, size=(-1, -1),
                                      style=wx.TE_PROCESS_ENTER
                                      )
        grid_sizerBase.Add(self.crop_width, 0, wx.ALL |
                           wx.ALIGN_CENTER_HORIZONTAL |
                           wx.ALIGN_CENTER_VERTICAL, 5
                           )
        label_width = wx.StaticText(self, wx.ID_ANY, (_("Width")))
        grid_sizerBase.Add(label_width, 0, wx.ALL |
                           wx.ALIGN_CENTER_HORIZONTAL |
                           wx.ALIGN_CENTER_VERTICAL, 5
                           )
        self.axis_X = wx.SpinCtrl(self, wx.ID_ANY, "0",
                                  min=-1, max=self.v_width, size=(-1, -1),
                                  style=wx.TE_PROCESS_ENTER
                                  )
        boxctrl.Add(self.axis_X, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL |
                    wx.ALIGN_CENTER_VERTICAL, 5
                    )
        label_X = wx.StaticText(self, wx.ID_ANY, ("X"))
        boxctrl.Add(label_X, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL |
                    wx.ALIGN_CENTER_VERTICAL, 5
                    )
        # bottom layout
        gridBtn = wx.GridSizer(1, 2, 0, 0)
        gridhelp = wx.GridSizer(1, 1, 0, 0)
        gridBtn.Add(gridhelp)
        gridexit = wx.BoxSizer(wx.HORIZONTAL)
        btn_help = wx.Button(self, wx.ID_HELP, "")
        gridhelp.Add(btn_help, 0, wx.ALL, 5)
        btn_close = wx.Button(self, wx.ID_CANCEL, "")
        gridexit.Add(btn_close, 0, wx.ALL, 5)
        self.btn_ok = wx.Button(self, wx.ID_OK, _("Apply"))
        gridexit.Add(self.btn_ok, 0, wx.ALL, 5)
        btn_reset = wx.Button(self, wx.ID_CLEAR, _("Reset"))
        gridexit.Add(btn_reset, 0, wx.ALL, 5)
        gridBtn.Add(gridexit, 0, wx.ALL | wx.ALIGN_RIGHT | wx.RIGHT, 0)

        sizerBase.Add(gridBtn, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizerBase)
        sizerBase.Fit(self)
        self.Layout()

        # ----------------------Properties-----------------------#
        self.panelrect.SetBackgroundColour(wx.Colour(Crop.BACKGROUND))
        if Crop.OS == 'Darwin':
            label1.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL))
        else:
            label1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.SetTitle(_("Crop Filter"))

        self.crop_width.SetToolTip(_('Width crop setting'))

        self.axis_Y.SetToolTip(_('The vertical position of the top edge '
                                 'of the left corner. Set to -1 to center '
                                 'the vertical axis'))

        self.axis_X.SetToolTip(_('The horizontal position of the '
                                 'left edge. Set to -1 to center '
                                 'the horizontal axis'))

        self.crop_height.SetToolTip(_('Height crop setting'))

        # ----------------------Binding (EVT)------------------------#
        self.Bind(wx.EVT_SPINCTRL, self.onWidth, self.crop_width)
        self.Bind(wx.EVT_SPINCTRL, self.onHeight, self.crop_height)
        self.Bind(wx.EVT_SPINCTRL, self.onX, self.axis_X)
        self.Bind(wx.EVT_SPINCTRL, self.onY, self.axis_Y)
        self.Bind(wx.EVT_BUTTON, self.onCentre, self.btn_centre)
        self.Bind(wx.EVT_BUTTON, self.onLoad, btn_load)

        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.btn_ok)
        self.Bind(wx.EVT_BUTTON, self.on_reset, btn_reset)
        self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)

        if duration == '0:0:0':
            self.hour.Disable(), self.minute.Disable(),
            self.seconds.Disable(), btn_load.Disable()
            if not os.path.exists(self.frame):
                self.onLoad(self)

        if fcrop:  # previusly values
            self.default(fcrop)
    # ------------------------------------------------------------------#

    def default(self, fcrop):
        """
        Set controls to previous settings

        """
        s = fcrop.split(':')
        s[0] = s[0][5:]  # removing `crop=` word on first item
        self.crop_width.SetValue(int(s[0][2:]))
        self.crop_height.SetValue(int(s[1][2:]))

        x, y = None, None
        for i in s:
            if i.startswith('x'):
                x = i[2:]
            if i.startswith('y'):
                y = i[2:]
        if x:
            self.axis_X.SetValue(int(x))
        else:
            self.axis_X.SetValue(-1)

        if y:
            self.axis_Y.SetValue(int(y))
        else:
            self.axis_Y.SetValue(-1)

        self.onWidth(self)  # set min/max horizontal axis
        self.onHeight(self) # set min/max vertical axis
    # ------------------------------------------------------------------#

    def onLoad(self, event):
        """
        Build FFmpeg argument to get a specific video frame for
        loading in a wx.dc (device context)
        """
        h = '%02d' % int(self.hour.GetValue())
        m = '%02d' % int(self.minute.GetValue())
        s = '%02d' % int(self.seconds.GetValue())
        arg = ('-ss %s:%s:%s -i "%s" -vframes 1 -y "%s"' % (h, m, s,
                                                            self.video,
                                                            self.frame
                                                            ))
        thread = FFmpegGenericTask(arg)
        thread.join()  # wait end thread
        error = thread.status
        if error:
            wx.MessageBox('%s' % error, 'ERROR', wx.ICON_ERROR)
            return

        time.sleep(1.0)  # need to wait end task for saving
        self.image = self.frame  # update with new frame
        self.onDrawing(self)
    # ------------------------------------------------------------------#

    def onDrawing(self, event, dc=None):
        """
        Updating computation and call onRedraw to update
        rectangle position of the bob actor

        """
        self.height_dc = (self.crop_height.GetValue() / self.v_width) * 360
        self.width_dc = (self.crop_width.GetValue() / self.v_height) * self.h_ratio

        if self.axis_Y.GetValue() == -1:
            self.y_dc = (self.h_ratio / 2) - (self.height_dc / 2)
        else:
            self.y_dc = (self.axis_Y.GetValue() / self.v_width) * 360

        if self.axis_X.GetValue() == -1:
            self.x_dc = (360 / 2) - (self.width_dc / 2)
        else:
            self.x_dc = (self.axis_X.GetValue() / self.v_height) * self.h_ratio

        self.bob.onRedraw(self.x_dc,
                          self.y_dc,
                          self.width_dc,
                          self.height_dc,
                          self.w_ratio,
                          self.h_ratio,
                          self.image
                          )
    # ------------------------------------------------------------------#

    def onWidth(self, event):
        """
        Sets the limit to the minimum and maximum values for the
        horizontal X axis in relation to the values set for the
        width of the crop.
        If the maximum allowed value is set to the width of the crop,
        the X axis will be set to `min, max = 0, 0` i.e. disabled.

        The maximum allowed value for the width of the crop is
        established in the `self.v_width` attribute

        """
        if self.crop_width.GetValue() == self.v_width:
            self.axis_X.SetMax(0), self.axis_X.SetMin(0)
        else:
            self.axis_X.SetMax(self.v_width - self.crop_width.GetValue())
            self.axis_X.SetMin(-1)

        self.onDrawing(self)
    # ------------------------------------------------------------------#

    def onHeight(self, event):
        """
        Sets the limit to the minimum and maximum values for the
        vertical Y axis in relation to the values set for the
        height of the crop.
        If the maximum allowed value is set to the height of the crop,
        the Y axis will be set to `min, max = 0, 0` i.e. disabled.

        The maximum allowed value for the height of the crop is
        established in the `self.v_height` attribute

        """
        if self.crop_height.GetValue() == self.v_height:
            self.axis_Y.SetMax(0), self.axis_Y.SetMin(0)
        else:
            self.axis_Y.SetMax(self.v_height - self.crop_height.GetValue())
            self.axis_Y.SetMin(-1)

        self.onDrawing(self)
    # ------------------------------------------------------------------#

    def onX(self, event):
        """
        self.axis_X callback
        """
        self.onDrawing(self)

    # ------------------------------------------------------------------#
    def onY(self, event):
        """
        self.axis_Y callback
        """
        self.onDrawing(self)

    # ------------------------------------------------------------------#
    def onCentre(self, event):
        """
        Sets coordinates X, Y to center if not `GetMax == 0` .
        `GetMax == 0` means that the maximum size of the crop
        has been setted and the X or Y axes cannot be setted anymore.

        """
        if self.axis_Y.GetMax() != 0:
            self.axis_Y.SetValue(-1)

        if self.axis_X.GetMax() != 0:
            self.axis_X.SetValue(-1)

        if self.axis_Y.GetMax() or self.axis_X.GetMax():
            self.onDrawing(self)

    # ------------------------------------------------------------------#

    def on_help(self, event):
        """
        Open default browser to official help page
        """
        page = ('https://jeanslack.github.io/Videomass/Pages/Main_Toolbar/'
                'VideoConv_Panel/Filters/FilterCrop.html')
        webbrowser.open(page)
    # ------------------------------------------------------------------#

    def on_reset(self, event):
        """
        Reset all control values
        """
        self.axis_Y.SetMin(-1), self.axis_Y.SetMax(self.v_height)
        self.axis_X.SetMin(-1), self.axis_X.SetMax(self.v_width)
        self.crop_width.SetValue(0), self.axis_X.SetValue(0)
        self.crop_height.SetValue(0), self.axis_Y.SetValue(0)
        self.onDrawing(self)
    # ------------------------------------------------------------------#

    def on_close(self, event):

        event.Skip()
    # ------------------------------------------------------------------#

    def on_ok(self, event):
        """
        if you enable self.Destroy(), it delete from memory all data
        event and no return correctly. It has the right behavior if not
        used here, because it is called in the main frame.

        Event.Skip(), work correctly here. Sometimes needs to disable it for
        needs to maintain the view of the window (for exemple).
        """
        self.GetValue()
        # self.Destroy()
        event.Skip()
    # ------------------------------------------------------------------#

    def GetValue(self):
        """
        This method return values via the interface GetValue().
        Note: -1 for X and Y coordinates means center, which are
        empty values for FFmpeg syntax.
        """
        w = self.crop_width.GetValue()
        h = self.crop_height.GetValue()
        x = self.axis_X.GetValue()
        y = self.axis_Y.GetValue()

        if w and h:
            x_axis = 'x=%s:' % x if x > -1 else ''
            y_axis = 'y=%s:' % y if y > -1 else ''
            val = 'w=%s:h=%s:%s%s' % (w, h, x_axis, y_axis)
            return val[:len(val) - 1]  # remove last ':' string
        else:
            return None
