#!/usr/bin/python

import socket
import json
from gi.repository import Gtk, Gdk, GObject


class MenuExampleWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Sys Monitor")

		self.set_default_size(500, 500)

		action_group = Gtk.ActionGroup("my_actions")

		table = Gtk.Table(3,3,True)
		self.add(table)

		title = Gtk.Label("Current Stats")
		cpu_title = Gtk.Label("CPU:")
		mem_title = Gtk.Label("Mem:")
		cpu_data = Gtk.Label()
		mem_data = Gtk.Label()
		
		table.attach(title,0,3,0,1)
		table.attach(cpu_title,0,1,1,2)
		table.attach(mem_title,0,1,2,3)
		table.attach(cpu_data,1,3,1,2)
		table.attach(mem_data,1,3,2,3)

		self.stats = dict()
		self.stats["Cpu"] = cpu_data
		self.stats["Memory"] = mem_data

		self.timeout_id = GObject.timeout_add(100, self.on_timeout, None)
		self.activity_mode = False


	def create_ui_manager(self):
		uimanager = Gtk.UIManager()

		# Throws exception if something went wrong
		uimanager.add_ui_from_string(UI_INFO)

		# Add the accelerator group to the toplevel window
		accelgroup = uimanager.get_accel_group()
		self.add_accel_group(accelgroup)
		return uimanager

	def on_timeout(self, data):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(('', 6000))
		data = sock.recv(10000)
		sock.close()
		#print data
		stats = json.loads(data)
		for stat in stats["Stats"]:
			self.stats[stat["type"]].set_label("%f"%stat["value"])
		return True



window = MenuExampleWindow()		
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
