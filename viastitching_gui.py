# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import sys

import gettext
_ = gettext.gettext

###########################################################################
## Class viastitching_gui
###########################################################################

class viastitching_gui ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Via Stitching"), pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )

		if sys.version_info[0] == 2:
			self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		else:
			self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bMainSizer = wx.BoxSizer( wx.VERTICAL )

		fgOptionsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgOptionsSizer.SetFlexibleDirection( wx.BOTH )
		fgOptionsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_lblNetName = wx.StaticText( self, wx.ID_ANY, _(u"Net Name"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblNetName.Wrap( -1 )

		fgOptionsSizer.Add( self.m_lblNetName, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.ALIGN_RIGHT, 5 )

		m_cbNetChoices = []
		self.m_cbNet = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_cbNetChoices, wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT )
		fgOptionsSizer.Add( self.m_cbNet, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_lblVia = wx.StaticText( self, wx.ID_ANY, _(u"Via (Size/Drill)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblVia.Wrap( -1 )

		fgOptionsSizer.Add( self.m_lblVia, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.ALIGN_RIGHT, 5 )

		bHSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_txtViaSize = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bHSizer1.Add( self.m_txtViaSize, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_txtViaDrillSize = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bHSizer1.Add( self.m_txtViaDrillSize, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_lblUnit1 = wx.StaticText( self, wx.ID_ANY, _(u"mm"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblUnit1.Wrap( -1 )

		bHSizer1.Add( self.m_lblUnit1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		fgOptionsSizer.Add( bHSizer1, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_lblSpacing = wx.StaticText( self, wx.ID_ANY, _(u"Spacing (V/H)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblSpacing.Wrap( -1 )

		fgOptionsSizer.Add( self.m_lblSpacing, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.ALIGN_RIGHT, 5 )

		bHSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_txtVSpacing = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bHSizer2.Add( self.m_txtVSpacing, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_txtHSpacing = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bHSizer2.Add( self.m_txtHSpacing, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_lblUnit2 = wx.StaticText( self, wx.ID_ANY, _(u"mm"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblUnit2.Wrap( -1 )

		bHSizer2.Add( self.m_lblUnit2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		fgOptionsSizer.Add( bHSizer2, 1, wx.EXPAND, 5 )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, _(u"Clearance"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		fgOptionsSizer.Add( self.m_staticText6, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.ALIGN_RIGHT, 5 )

		bHSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_txtClearance = wx.TextCtrl( self, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bHSizer3.Add( self.m_txtClearance, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

		self.m_lblUnit3 = wx.StaticText( self, wx.ID_ANY, _(u"mm"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblUnit3.Wrap( -1 )

		bHSizer3.Add( self.m_lblUnit3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		fgOptionsSizer.Add( bHSizer3, 1, wx.EXPAND, 5 )

		self.m_lblPattern = wx.StaticText( self, wx.ID_ANY, _(u"Pattern"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblPattern.Wrap( -1 )

		fgOptionsSizer.Add( self.m_lblPattern, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		m_cbPatternChoices = [ _(u"Grid"), _(u"Star") ]
		self.m_cbPattern = wx.ComboBox( self, wx.ID_ANY, _(u"Grid"), wx.DefaultPosition, wx.DefaultSize, m_cbPatternChoices, wx.CB_DROPDOWN|wx.CB_READONLY )
		self.m_cbPattern.SetSelection( 0 )
		fgOptionsSizer.Add( self.m_cbPattern, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


		bMainSizer.Add( fgOptionsSizer, 0, wx.EXPAND, 5 )

		self.staticHLine1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bMainSizer.Add( self.staticHLine1, 0, wx.EXPAND |wx.ALL, 5 )

		bHSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_rFill = wx.RadioButton( self, wx.ID_ANY, _(u"Fill"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_rFill.SetValue( True )
		bHSizer4.Add( self.m_rFill, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_rClear = wx.RadioButton( self, wx.ID_ANY, _(u"Clear"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bHSizer4.Add( self.m_rClear, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

		self.m_chkClearOwn = wx.CheckBox( self, wx.ID_ANY, _(u"Only clear plugin placed vias"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_chkClearOwn.SetValue(True)
		self.m_chkClearOwn.Enable( False )

		bHSizer4.Add( self.m_chkClearOwn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bMainSizer.Add( bHSizer4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.staticHLine2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bMainSizer.Add( self.staticHLine2, 0, wx.EXPAND |wx.ALL, 5 )

		bHSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_btnOk = wx.Button( self, wx.ID_ANY, _(u"&Ok"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_btnOk.SetDefault()
		bHSizer5.Add( self.m_btnOk, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_btnCancel = wx.Button( self, wx.ID_ANY, _(u"&Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bHSizer5.Add( self.m_btnCancel, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bMainSizer.Add( bHSizer5, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )


		self.SetSizer( bMainSizer )
		self.Layout()
		bMainSizer.Fit( self )

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


