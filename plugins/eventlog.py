# -*- coding: utf-8 -*-

import os
import re
import time
from PluginsManager import ConsolePlugin
from S2Wrapper import Savage2DaemonHandler
from operator import itemgetter
#This plugin was written by Old55 and he takes full responsibility for the junk below.
#He does not know python so the goal was to make something functional, not something
#efficient or pretty.


class eventlog(ConsolePlugin):
	VERSION = "0.0.1"
	ms = None
	PHASE = 0
	STARTSTAMP = 0
	playerlist = []
	eventlist = []
	eventbuffer = []
	objectlist = []
	typelist = []
	TIME = 0
	GAMETIME = 0
	EVENT = 0
	def onPluginLoad(self, config, **kwargs):
		
		#ini = ConfigParser.ConfigParser()
		#ini.read(config)
		#for (name, value) in config.items('balancer'):
		#	if (name == "level"):
		#		self._level = int(value)

		#	if (name == "sf"):
		#		self._sf = int(value)
		
		#f = open('objectlist.txt', 'r')
		#self.objectlist = f.readlines()
		#f.close()
		#print self.objectlist
		self.objectlist = [
('Building_Academy','Academy'),\
('Building_Armory','Armory'),\
('Building_ArrowTower','Arrow Tower'),\
('Building_CannonTower','Cannon Tower'),\
('Building_CharmShrine','Charm Shrine'),\
('Building_ChlorophilicSpire','Chlorophilic Spire'),\
('Building_EntangleSpire','Static Spire'),\
('Building_Garrison','Garrison'),\
('Building_GroveMine','Grove Mine'),\
('Building_HumanHellShrine','Hell Shrine'),\
('Building_Lair','Lair'),\
('Building_Monastery','Monastery'),\
('Building_Nexus','Nexus'),\
('Building_PredatorDen','Predator Den'),\
('Building_Sanctuary','Sanctuary'),\
('Building_ShieldTower','Shield Tower'),\
('Building_SiegeWorkshop','Siege Workshop'),\
('Building_SteamMine','Steam Mine'),\
('Building_StrataSpire','Strata Spire'),\
('Building_Stronghold','Stronghold'),\
('Building_SubLair','Sublair'),\
('Team1','Humans'),\
('Team2','Beasts'),\
('Gadget_AmmoDepot','Ammo Depot'),\
('Gadget_BeastSpawnPortal','Spawn Portal'),\
('Gadget_DemoCharge','Demo Charge'),\
('Gadget_ElectricEye','Electric Eye'),\
('Gadget_HumanOfficerSpawnFlag','Spawn Portal'),\
('Gadget_ManaFountain','Mana Fountain'),\
('Gadget_Sentry','Sentry Bat'),\
('Gadget_ShieldGenerator','Shield Generator'),\
('Gadget_SteamTurret','Steam Turret'),\
('Gadget_Venus','Poison Venus'),\
('Player_BatteringRam','Battering Ram'),\
('Player_Behemoth','Behemoth'),\
('Player_Chaplain','Chaplain'),\
('Player_Commander','Commander'),\
('Player_Conjurer','Conjurer'),\
('Player_Devourer','Devourer'),\
('Player_Engineer','Builder'),\
('Player_Hunter','Hunter'),\
('Player_Legionnaire','Legionnaire',),\
('Player_Maliken','Maliken'),\
('Player_Malphas','Malphas'),\
('Player_Marksman','Marksman'),\
('Player_Observer','Spectator'),\
('Player_Predator','Predator'),\
('Player_Revenant','Revenant'),\
('Player_Savage','Savage'),\
('Player_Shaman','Shaman',),\
('Player_ShapeShifter','Shape Shifter'),\
('Player_Steambuchet','Steambuchet'),\
('Player_Summoner','Summoner'),\
('Player_Tempest','Tempest'),\
('None','None')]		
		pass
	
	def onPhaseChange(self, *args, **kwargs):

		phase = int(args[0])
		self.PHASE = phase

		if phase == 6:
			#built
			kwargs['Broadcast'].broadcast(\
			"RegisterGlobalScript -1 \"RegisterEntityScript #GetScriptParam(index)# death \\\"Set _objdead #GetScriptParam(index)#;\
			 									          Set _killer #GetScriptParam(attackingindex)#;\
													  ExecScript ObjectDeath\\\";\
			echo EVENT built #GetScriptParam(type)# on None by None at #GetScriptParam(posx)# #GetScriptParam(posy)# 0.0; echo\" buildingplaced")
			
			#placed gadget
			kwargs['Broadcast'].broadcast(\
			"RegisterGlobalScript -1 \"RegisterEntityScript #GetScriptParam(gadgetindex)# death \\\"Set _objdead #GetScriptParam(index)#;\
			 									                Set _killer #GetScriptParam(attackingindex)#;\
													        ExecScript ObjectDeath\\\";\
			echo EVENT placed #GetScriptParam(type)# on -1 by #GetClientNumFromIndex(|#GetScriptParam(index)|#)# at #GetScriptParam(posx)# #GetScriptParam(posy)# 0.0; echo\" placegadget")

			#spawn
			kwargs['Broadcast'].broadcast(\
			"RegisterGlobalScript -1 \"RegisterEntityScript #GetScriptParam(index)# death \\\"Set _dead #GetScriptParam(index)#;\
			 									          Set _killer #GetScriptParam(attackingindex)#;\
													  ExecScript PlayerDeath\\\";\
			 set _spindex #GetScriptParam(index)#;\
			 set _spx #GetPosX(|#_spindex|#)#;\
			 set _spy #GetPosY(|#_spindex|#)#;\
			 set _spz #GetPosZ(|#_spindex|#)#;\
			 echo EVENT spawn #GetType(|#GetScriptParam(index)|#)# on -1 by #GetClientNumFromIndex(|#GetScriptParam(index)|#)# at #_spx# #_spy# 0.0; echo\" spawn")

			#changeteam, only for team 1 or 2
			kwargs['Broadcast'].broadcast(\
			"RegisterGlobalScript -1 \"set _team #GetScriptParam(newteam)#;\
						   if [_team > 0]\
						    echo EVENT join Team#_team# on -1 by #GetClientNumFromIndex(|#GetScriptParam(index)|#)# at 0.0 0.0 0.0; echo\" changeteam")
			
			#playerleave
			kwargs['Broadcast'].broadcast(\
			"RegisterGlobalScript -1 \"set _team #GetTeam(|#GetScriptParam(index)|#);\
						   if [_team > 0]\
						    echo EVENT leave Team#_team# on -1 by ##GetScriptParam(clientid)# at 0.0 0.0 0.0; echo\" playerleave")

				
			#ObjectDeath
			kwargs['Broadcast'].broadcast(\
			"RegisterGlobalScript -1 \"set _dx #GetPosX(|#_objdead|#)#;\
			 set _dy #GetPosY(|#_objdead|#)#;\
			 set _dz #GetPosZ(|#_objdead|#)#;\
			 echo EVENT killed #GetType(|#_objdead|#)# on -1 by #GetClientNumFromIndex(|#_killer|#)# at #_dx# #_dy# 0.0; echo\" ObjectDeath")
			
			#PlayerDeath
			kwargs['Broadcast'].broadcast(\
			"RegisterGlobalScript -1 \"set _dx #GetPosX(|#_dead|#)#;\
			 set _dy #GetPosY(|#_dead|#)#;\
			 set _dz #GetPosZ(|#_dead|#)#;\
			 echo EVENT killed #GetType(|#_dead|#)# on #GetClientNumFromIndex(|#_dead|#)# by #GetClientNumFromIndex(|#_killer|#)# at #_dx# #_dy# 0.0; echo\" PlayerDeath")

		if phase == 7:
			self.eventlist = sorted(self.eventlist, key=itemgetter('event','time'), reverse=False)
			self.endGame(**kwargs)
			self.STARTSTAMP = 0
		if phase == 5:
			self.GAMETIME = 0
			self.EVENT = 0
			self.STARTSTAMP = args[1]
	def getEvent(self, *args, **kwargs):

		

		if self.PHASE != 5:
			return

		self.EVENT += 1
		event = args[0]
		indextype = args[1]
		on = args[2]
		by = args[3]
		x = (args[4])
		y = (args[5])
		z = (args[6])
		tm = self.EVENT
		location = ('%s %s %s' % (x, y, z))
		objecttype = self.getObjectType(indextype)
		clienton = self.getPlayerByClientNum(on)
		clientby = self.getPlayerByClientNum(by)

		eventbuffer =  ({'action' : event,\
				 'type' : objecttype,\
				 'by' : clientby['name'],\
				 'on': clienton['name'],\
				 'time' : self.GAMETIME,\
				 'coord' : location,\
				 'event' : tm})	
		
		self.eventlist.append(eventbuffer)

		
	def getObjectType(self, indextype):
		
		for each in self.objectlist:
			if indextype == each[0]:
				return each[1]


	def getPlayerByClientNum(self, cli):
		
		for client in self.playerlist:
			if (client['clinum'] == cli):
				return client
		client = {'name' : 'None'}
		return client


	def getPlayerByName(self, name):
		
		for client in self.playerlist:
			if (client['name'].lower() == name.lower()):
				return client

		client = {'name' : 'None'}
		return client


	def onConnect(self, *args, **kwargs):
		
		id = args[0]
		ip = args[2]
		
		for client in self.playerlist:
			if (client['clinum'] == id):
				return
		
		self.playerlist.append ({'clinum' : id,\
					 'name' : 'X',\
					 'active' : True
					 })

		
	def onDisconnect(self, *args, **kwargs):
		
		cli = args[0]
		client = self.getPlayerByClientNum(cli)
		client ['active'] = False
	

	def onSetName(self, *args, **kwargs):

		cli = args[0]
		playername = args[1]
		client = self.getPlayerByClientNum(cli)
		client ['name'] = playername
		
	def onServerStatus(self, *args, **kwargs):
		CURRENTSTAMP = int(args[1])
		self.TIME = int(CURRENTSTAMP) - int(self.STARTSTAMP)
		self.GAMETIME += 1
		
	def endGame(self, **kwargs):
	
		f = open('event.txt', 'a')
		for each in self.eventlist:
			f.write("%s" % (each))
		f.close()
		
		self.eventlist = []