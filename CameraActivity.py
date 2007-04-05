#!/usr/bin/env python

import gtk
import gobject

from sugar.activity.Activity import Activity

from glive import LiveVideoSlot
from image_display import Image_Display
from controller import Controller
from thumbnails import Thumbnails


class CameraActivity(Activity):
	def __init__(self):
		Activity.__init__(self)
		self.set_title( "Camera Activity" )

		#wait a moment so that our debug console capture mistakes
		gobject.idle_add( self._initme, None )


	def _initme(self, userdata=None):
		self.connect("destroy", gtk.main_quit)

		w = gtk.gdk.screen_width()
		h = gtk.gdk.screen_height()
		self.c = Controller(w, h)
		self.c._frame = self
		self.set_default_size( self.c._w, self.c._h )

		#layout
		self.fix = gtk.Fixed()
		self.add( self.fix )

		#components
		self.thumbTrayHt = 150
		#photos
		Image_Display( self.c )
		self.c._id.set_size_request( self.c._w, self.c._h-self.thumbTrayHt )
		#thumbnails
		Thumbnails( self.c )
		self.c._thumbs.set_size_request( self.c._w, self.thumbTrayHt )
		#live video
		LiveVideoSlot( self.c )
		self.c._livevideo.set_size_request( 640, 480)

		#pack
		self.fix.put( self.c._id, 0, 0 )
		self.fix.put( self.c._thumbs, 0, self.c._h-self.thumbTrayHt )

		lv_x = ((self.c._w/2)-(self.c.polSvg.props.width/2)) + 15 + 1
		lv_y = (((self.c._h-self.thumbTrayHt)/2)-(self.c.polSvg.props.height/2)) + 15
		self.fix.put( self.c._livevideo, lv_x, lv_y )
		self.show_all()

		#turn on the camera
		self.c._livevideo.play()

		#wrapped up and heading off to play ball
		return False


	def execute(self, command, args):
		if (command == "camera"):
			#take a snap
			self.c.takeSnapshot()
			return True
		else:
			return False