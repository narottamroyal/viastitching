#!/usr/bin/env python

# ViaStitching for pcbnew
# This is the plugin WX dialog
# (c) Michele Santucci 2019

import wx
import pcbnew
import gettext
import math

from .viastitching_gui import viastitching_gui
from math import sqrt

_ = gettext.gettext
__version__ = "0.3.0"
__timecode__ = 1972
__viagroupname__ = "VIA_STITCHING_GROUP"


class ViaStitchingDialog(viastitching_gui):
    """Class that gathers all the GUI controls."""

    def __init__(self, board):
        """Initialize the brand new instance."""

        super(ViaStitchingDialog, self).__init__(None)
        self.SetTitle(_("Via Stitching v{0}").format(__version__))
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.m_btnCancel.Bind(wx.EVT_BUTTON, self.onCloseWindow)
        self.m_btnOk.Bind(wx.EVT_BUTTON, self.onProcessAction)
        self.m_rClear.Bind(wx.EVT_RADIOBUTTON, self.onRadioButtonCheck)
        self.m_rFill.Bind(wx.EVT_RADIOBUTTON, self.onRadioButtonCheck)
        self.m_chkRemoveAll.Disable()
        self.board = pcbnew.GetBoard()
        self.pcb_group = None

        # Search through groups
        for group in self.board.Groups():
            if group.GetName() == __viagroupname__:
                self.pcb_group = group

        if self.pcb_group is None:
            self.pcb_group = pcbnew.PCB_GROUP(None)
            self.pcb_group.SetName(__viagroupname__)
            self.board.Add(self.pcb_group)

        # Use the same unit set int PCBNEW
        self.ToUserUnit = None
        self.FromUserUnit = None
        units_mode = pcbnew.GetUserUnits()

        if units_mode == 0:
            self.ToUserUnit = pcbnew.ToMils
            self.FromUserUnit = pcbnew.FromMils
            self.m_lblUnit1.SetLabel(_("mils"))
            self.m_lblUnit2.SetLabel(_("mils"))
            self.m_lblUnit3.SetLabel(_("mils"))
            self.m_lblUnit4.SetLabel(_("mils"))
        elif units_mode == 1:
            self.ToUserUnit = pcbnew.ToMM
            self.FromUserUnit = pcbnew.FromMM
            self.m_lblUnit1.SetLabel(_("mm"))
            self.m_lblUnit2.SetLabel(_("mm"))
            self.m_lblUnit3.SetLabel(_("mm"))
            self.m_lblUnit4.SetLabel(_("mm"))
        else:
            wx.MessageBox(_("Not a valid frame"))
            self.Destroy()

        # Get current via dimensions
        settings = board.GetDesignSettings()
        self.m_txtViaSize.SetValue(
            "%.6f" % self.ToUserUnit(settings.GetCurrentViaSize())
        )
        self.m_txtViaDrillSize.SetValue(
            "%.6f" % self.ToUserUnit(settings.GetCurrentViaDrill())
        )

        # Set default spacing to double the current via width
        spacing = self.ToUserUnit(settings.GetCurrentViaSize()) * 2
        self.m_txtSpacingX.SetValue("%.6f" % spacing)
        self.m_txtSpacingY.SetValue("%.6f" % spacing)

        # Set default offsets
        self.m_txtOffsetX.SetValue("%.6f" % 0)
        self.m_txtOffsetY.SetValue("%.6f" % 0)

        # Set default clearances
        self.m_txtEdgeClearance.SetValue("0")
        self.m_txtTrackClearance.SetValue(
            "%.6f" % self.ToUserUnit(settings.GetBiggestClearanceValue())
        )

        self.area = None
        self.net = None
        self.overlappings = None

        # Check for selected area
        if not self.GetAreaConfig():
            wx.MessageBox(_("Please select a valid area"))
            self.Destroy()
        else:
            # Get overlapping items
            self.GetOverlappingItems()
            # Populate nets checkbox
            self.PopulateNets()

    def GetOverlappingItems(self):
        """Collect overlapping items.
        Every item found inside bounding box is a candidate to be inspected for overlapping.
        """

        area_bbox = self.area.GetBoundingBox()

        if hasattr(self.board, "GetModules"):
            modules = self.board.GetModules()
        else:
            modules = self.board.GetFootprints()

        tracks = self.board.GetTracks()

        self.overlappings = []

        for item in tracks:
            if type(item) in [
                pcbnew.PCB_ARC,
                pcbnew.PCB_TRACK,
                pcbnew.PCB_VIA,
            ] and item.GetBoundingBox().Intersects(area_bbox):
                self.overlappings.append(item)

        for item in modules:
            if item.GetBoundingBox().Intersects(area_bbox):
                for pad in item.Pads():
                    self.overlappings.append(pad)

        # TODO: change algorithm to 'If one of the candidate area's edges overlaps with target area declare candidate as overlapping'
        for i in range(0, self.board.GetAreaCount()):
            item = self.board.GetArea(i)
            if item.GetBoundingBox().Intersects(area_bbox):
                if item.GetNetname() != self.net:
                    self.overlappings.append(item)

    def GetAreaConfig(self):
        """Check selected area (if any) and verify if it is a valid container for vias.

        Returns:
            bool: Returns True if an area/zone is selected and matches the insertion criteria, False otherwise.
        """

        for i in range(0, self.board.GetAreaCount()):
            area = self.board.GetArea(i)
            if area.IsSelected():
                if not area.IsOnCopperLayer():
                    return False
                elif area.GetDoNotAllowCopperPour():
                    return False
                self.area = area
                self.net = area.GetNetname()
                return True

        return False

    def PopulateNets(self):
        """Populate nets widget."""

        nets = self.board.GetNetsByName()

        # Tricky loop, the iterator should return two values, unluckly I'm not able to use the
        # first value of the couple so I'm recycling it as netname.
        for netname, net in nets.items():
            netname = net.GetNetname()
            if (netname != None) and (netname != ""):
                self.m_cbNet.Append(netname)

        # Select the net used by area (if any)
        if self.net != None:
            index = self.m_cbNet.FindString(self.net)
            self.m_cbNet.Select(index)

    def ClearArea(self):
        """Clear selected area."""

        remove_all = self.m_chkRemoveAll.IsChecked()
        drillsize = self.FromUserUnit(float(self.m_txtViaDrillSize.GetValue()))
        viasize = self.FromUserUnit(float(self.m_txtViaSize.GetValue()))
        netname = self.m_cbNet.GetStringSelection()
        # commit = pcbnew.COMMIT()
        viacount = 0

        for item in self.board.GetTracks():
            if type(item) is pcbnew.PCB_VIA:
                # If the user selected the Undo action only signed/grouped vias are removed,
                # otherwise are removed vias matching values set in the dialog.

                # if undo and (item.GetTimeStamp() == __timecode__):
                if (not remove_all) and (self.pcb_group is not None):
                    group = item.GetParentGroup()
                    if group is not None and group.GetName() == __viagroupname__:
                        self.board.Remove(item)
                        viacount += 1
                        # commit.Remove(item)
                elif (
                    remove_all
                    and self.area.HitTestFilledArea(
                        self.area.GetLayer(), item.GetPosition(), 0
                    )
                    and (item.GetDrillValue() == drillsize)
                    and (item.GetWidth() == viasize)
                    and (item.GetNetname() == netname)
                ):
                    self.board.Remove(item)
                    viacount += 1
                    # commit.Remove(item)

        if viacount > 0:
            wx.MessageBox(_("Removed %d vias!") % viacount)
            # commit.Push()
            pcbnew.Refresh()

    def CheckClearance(self, p1, area, clearance):
        """Check if position specified by p1 comply with given clearance in area.

        Parameters:
            p1 (wxPoint): Position to test
            area (pcbnew.ZONE_CONTAINER): Area
            clearance (int): Clearance value

        Returns:
            bool: True if p1 position comply with clearance value False otherwise.

        """

        corners = area.GetNumCorners()
        # Calculate minimum distance from corners
        # TODO: remove?
        for i in range(0, corners):
            p2 = area.GetCornerPosition(i)
            distance = sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

            if distance < clearance:
                return False

        # Calculate minimum distance from edges
        for i in range(0, corners):
            if i == corners - 1:
                corner1 = area.GetCornerPosition(corners - 1)
                corner2 = area.GetCornerPosition(0)
            else:
                corner1 = area.GetCornerPosition(i)
                corner2 = area.GetCornerPosition(i + 1)

            distance, _ = pnt2line(p1, corner1, corner2)

            if distance <= clearance:
                return False

        return True

    def CheckOverlap(self, via):
        """Check if via overlaps or interfere with other items on the board.

        Parameters:
            via (pcbnew.VIA): Via to be checked

        Returns:
            bool: True if via overlaps with an item, False otherwise.
        """

        for item in self.overlappings:
            if type(item) is pcbnew.PAD:
                if item.GetBoundingBox().Intersects(via.GetBoundingBox()):
                    return True
            elif type(item) is pcbnew.PCB_ARC or type(item) is pcbnew.PCB_TRACK:
                clearance = self.FromUserUnit(
                    float(self.m_txtTrackClearance.GetValue())
                )
                track_shape = item.GetEffectiveShape()
                via_shape = via.GetEffectiveShape()
                if track_shape.Collide(via_shape, clearance):
                    return True
            elif type(item) is pcbnew.PCB_VIA:
                # Overlapping with vias work best if checking is performed by intersection
                if item.GetBoundingBox().Intersects(via.GetBoundingBox()):
                    return True
            elif type(item) is pcbnew.ZONE:
                if item.HitTestFilledArea(self.area.GetLayer(), via.GetPosition(), 0):
                    return True

        return False

    def FillupArea(self):
        """Fills selected area with vias."""

        via_size = self.FromUserUnit(float(self.m_txtViaSize.GetValue()))
        drill_size = self.FromUserUnit(float(self.m_txtViaDrillSize.GetValue()))
        step_x = self.FromUserUnit(float(self.m_txtSpacingX.GetValue()))
        step_y = self.FromUserUnit(float(self.m_txtSpacingY.GetValue()))
        offset_x = self.FromUserUnit(float(self.m_txtOffsetX.GetValue()))
        offset_y = self.FromUserUnit(float(self.m_txtOffsetY.GetValue()))
        clearance = self.FromUserUnit(float(self.m_txtEdgeClearance.GetValue()))
        bbox = self.area.GetBoundingBox()
        top = bbox.GetTop()
        bottom = bbox.GetBottom()
        right = bbox.GetRight()
        left = bbox.GetLeft()
        netname = self.m_cbNet.GetStringSelection()
        netcode = self.board.GetNetcodeFromNetname(netname)
        pattern = self.m_cbPattern.GetStringSelection()
        offset_row = False
        layer_set = self.area.GetLayerSet()
        layers = list(layer_set.Seq())
        # commit = pcbnew.COMMIT()

        # Cycle through area bounding box checking and inserting vias
        viacount = 0
        y = top + offset_y
        while y <= bottom:
            x = left + offset_x
            if pattern == "Star":
                # Offset every second row to create star pattern
                x += int(step_x / 2) if offset_row else 0
                offset_row = not offset_row

            while x <= right:
                p = pcbnew.VECTOR2I(x, y)
                if all(self.area.HitTestFilledArea(layer, p, 0) for layer in layers):
                    via = pcbnew.PCB_VIA(self.board)
                    via.SetPosition(p)
                    via.SetLayerSet(layer_set)
                    via.SetNetCode(netcode)
                    via.SetDrill(drill_size)
                    via.SetWidth(via_size)
                    # via.SetTimeStamp(__timecode__)
                    if not self.CheckOverlap(via):
                        # Check clearance only if clearance value differs from 0 (disabled)
                        if (clearance == 0) or self.CheckClearance(
                            p, self.area, clearance
                        ):
                            self.board.Add(via)
                            # commit.Add(via)
                            self.pcb_group.AddItem(via)
                            viacount += 1
                x += step_x
            y += step_y

        if viacount > 0:
            wx.MessageBox(_("Inserted %d vias!") % viacount)
            # commit.Push()
            pcbnew.Refresh()
        else:
            wx.MessageBox(_("No vias were inserted..."))

    def onProcessAction(self, event):
        """Manage main button (Ok) click event."""

        if self.m_rFill.GetValue():
            self.FillupArea()
        else:
            self.ClearArea()

        self.Destroy()

    def onRadioButtonCheck(self, event):
        """Manage radio button state change event."""

        if self.m_rClear.GetValue():
            self.m_chkRemoveAll.Enable()
        else:
            self.m_chkRemoveAll.Disable()

    def onCloseWindow(self, event):
        """Manage Close button click event."""

        self.Destroy()


def InitViaStitchingDialog(board):
    """Initialize dialog."""

    dlg = ViaStitchingDialog(board)
    dlg.Show(True)
    return dlg


class aVector:
    def __init__(self, point: pcbnew.wxPoint | list):
        if isinstance(point, pcbnew.wxPoint):
            self.x = float(point.x)
            self.y = float(point.y)
        elif isinstance(point, list):
            self.x = point[0]
            self.y = point[1]

    def __sub__(self, other: pcbnew.wxPoint):
        return aVector([self.x - float(other.x), self.y - float(other.y)])

    def __mul__(self, other):
        return aVector([self.x * float(other), self.y * float(other)])

    def __add__(self, other):
        return aVector([self.x + float(other.x), self.y + float(other.y)])

    def __truediv__(self, other):
        return aVector([self.x / other, self.y / other])

    @staticmethod
    def norm(vector):
        return sqrt(pow(vector.x, 2) + pow(vector.y, 2))

    @staticmethod
    def dot(vector1, vector2):
        return vector1.x * vector2.x + vector1.y * vector2.y


# Given a line with coordinates 'start' and 'end' and the
# coordinates of a point 'point' the proc returns the shortest
# distance from pnt to the line and the coordinates of the
# nearest point on the line.
#
# 1  Convert the line segment to a vector ('line_vec').
# 2  Create a vector connecting start to pnt ('pnt_vec').
# 3  Find the length of the line vector ('line_len').
# 4  Convert line_vec to a unit vector ('line_unitvec').
# 5  Scale pnt_vec by line_len ('pnt_vec_scaled').
# 6  Get the dot product of line_unitvec and pnt_vec_scaled ('t').
# 7  Ensure t is in the range 0 to 1.
# 8  Use t to get the nearest location on the line to the end
#    of vector pnt_vec_scaled ('nearest').
# 9  Calculate the distance from nearest to pnt_vec_scaled.
# 10 Translate nearest back to the start/end line.
# Malcolm Kesson 16 Dec 2012
def pnt2line(point: pcbnew.wxPoint, start: pcbnew.wxPoint, end: pcbnew.wxPoint):
    pnt = vector([point.x, point.y])
    strt = vector([start.x, start.y])
    nd = vector([end.x, end.y])
    line_vec = nd - strt
    pnt_vec = pnt - strt
    line_len = norm(line_vec)
    line_unitvec = line_vec / line_len
    pnt_vec_scaled = pnt_vec / line_len
    t = dot(line_unitvec, pnt_vec_scaled)
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = line_vec * t
    dist = norm(pnt_vec - nearest)
    nearest = nearest + strt
    return dist, nearest


norm = aVector.norm
vector = aVector
dot = aVector.dot
