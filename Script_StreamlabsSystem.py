import sys
import json
import os
import ctypes
import codecs
import time
import linecache
import os

ScriptName = "Kokushigotouebishe"
Website = "https://www.streamlabs.com"
Description = "Script to interact with auditory"
Creator = "Alexander"
Version = "1.0.0"

configFile = "config.json"
settings = {}

def Init():
	global settings

	path = os.path.dirname(__file__)
	
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"command": "!bank",
			"permission": "Everyone",
			"useCosts" : True,
			"costs" : 5000,
			"responseNotEnoughPoints" : "$user you have not $cost to use this command!",
			"useCooldown": True,
			"useCooldownMessages": True,
			"cooldown": 2,
			"onCooldown": "command on coldown $cd!",
			"userCooldown": 3,
			"onUserCooldown": "$user for you command on coldown $cd!",
			"Response": "$user you donate Zenusoid $cost mana!",
			"WrongFormat": "You need to write !bank [number]",
			"saveUserlist": True
		}

	return


def Execute(data):

	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, settings["permission"], ""):
		outputMessage = ""
		userId = data.User
		username = data.UserName
		msg = data.Message
		usercooldown = settings["userCooldown"]
		cd = settings["cooldown"]
		points = Parent.GetPoints(userId)

		if len(msg.split(" ")) > 1:
			if msg.split(" ")[1].isdigit() and int(msg.split(" ")[1].isdigit()) > 0:
				costs = int(msg.split(" ")[1])
				if (costs > Parent.GetPoints(userId)) and settings["useCosts"]:
					outputMessage = settings["responseNotEnoughPoints"]
				elif settings["useCooldown"] and (Parent.IsOnCooldown(ScriptName, settings["command"]) or Parent.IsOnUserCooldown(ScriptName, settings["command"], userId)):
					if settings["useCooldownMessages"]:
						if Parent.GetCooldownDuration(ScriptName, settings["command"]) > Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId):
							cdi = Parent.GetCooldownDuration(ScriptName, settings["command"])
							cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
							outputMessage = settings["onCooldown"]
						else:
							cdi = Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId)
							cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
							outputMessage = settings["onUserCooldown"]
						outputMessage = outputMessage.replace("$cd", cd)
					else:
						outputMessage = ""
				else:
					outputMessage = settings["Response"]

					if settings["useCosts"]:
						Parent.RemovePoints(userId, username, costs)

					if settings["useCooldown"]:
						Parent.AddUserCooldown(ScriptName, settings["command"], userId, settings["userCooldown"])
						Parent.AddCooldown(ScriptName, settings["command"], settings["cooldown"])

				outputMessage = outputMessage.replace("$user", username)
				outputMessage = outputMessage.replace("$cost", str(costs))
				outputMessage = outputMessage.replace("$points", str(points))
				outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())
				outputMessage = outputMessage.replace("$command", settings["command"])
				path = r"C:/Users/Zenusoid/AppData/Roaming/Streamlabs/BankScript/file.exe --mana_add={}".format(int(costs))
				os.system(os.path.normpath(path))
			else:
				outputMessage = settings['WrongFormat']
		else:
			outputMessage = settings['WrongFormat']

		Parent.SendStreamMessage(outputMessage)

	return()


def Parse(parseString, user, target, message):
    """Parse function"""
    if "!bank" in message:
        return parseString


def Tick():
	return


