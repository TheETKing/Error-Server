#CSV Exporter, by Bryton 2/10/16
#Last Updated: 8/26/17
import utils
from collections import OrderedDict
from TBACommunicator import TBACommunicator
import csv
from DataModel import *
import Math

#Puts scout z-scores in csv file
def CSVExportScoutZScores(zscores):
	with open('./scoutRankExport.csv', 'w') as f:
		writer = csv.DictWriter(f, fieldnames = ['name', 'spr', 'Z-Score'])
		writer.writeheader()
		for k, v in zscores.items():
			writer.writerow({'name' : k, 'spr' : zscores[k][1], 'Z-Score' : zscores[k][0]})

#Puts some scouted and calculated data in csv file
def CSVExport(comp, name, keys = []):
	calculator = Math.Calculator(comp)
	excluded = ['calculatedData', 'name', 'imageKeys', 'pitAllImageURLs', 'pitSelectedImageName']
	with open('./EXPORT-' + name + '.csv', 'w') as f:
		defaultKeys = [k for k in Team().__dict__.keys() if k not in excluded and k in keys]
		defaultKeys += [k for k in Team().calculatedData.__dict__.keys() if k in keys]
		defaultKeys = sorted(defaultKeys, key = lambda k: (k != 'number', k.lower()))
		writer = csv.DictWriter(f, fieldnames = defaultKeys)
		writer.writeheader()
		for team in comp.teams:
			team.numMatchesPlayed = len(calculator.su.getCompletedMatchesForTeam(team))
			tDict = team.__dict__
			tDict.update(team.calculatedData.__dict__)
			keys = sorted(defaultKeys, key = lambda k: (k != 'number', k.lower()))
			writer.writerow({k : tDict[k] for k in keys})

#Creates a dictionary of teams and their keys are the data associated with them
def readOPRData(dataFilePath):
	teamsDict = {}
	wantedKeys = ['team Number', 'auto Fuel High','auto Scored Gears', 'teleop Scored Gears', 'teleop Takeoff Points']
	with open(dataFilePath) as csvfile:
		reader = csv.DictReader(csvfile)
		first = True
		keys = []
		for r in reader:
			teamsDict[r['team Number']] = {k : r[k] for k in wantedKeys}
	return teamsDict

#Gets data from tba and firebase to make csv file
def CSVExportTeamOPRDataForComp(dataFilePath, dataOutputFilePath):
	wantedKeys = ['team Number', 'auto Fuel High','auto Scored Gears', 'teleop Scored Gears', 'teleop Takeoff Points']
	teams = TBACommunicator().makeEventTeamsRequest()
	teamNums = [team['team_number'] for team in teams]
	teamsDict = readOPRData(dataFilePath)
	teamsDict = {k : v for k, v in teamsDict.items() if int(k) in teamNums}
	print(teamsDict)
	# comp.updateTeamsAndMatchesFromFirebase()
	with open(dataOutputFilePath, 'w') as f:
		writer = csv.DictWriter(f, fieldnames = wantedKeys)
		writer.writeheader()
		for key, value in teamsDict.items():
			print(key)
			writer.writerow({k : teamsDict[key][k] for k in wantedKeys})

# CSVExportTeamOPRDataForComp('./ChampionshipHouston-Table 1.csv','./newton2017data.csv)

#General export function for all of your basic data export needs
def CSVExportGeneral(comp, name):
	CSVExport(comp, name, keys = Team().__dict__.keys() + Team().calculatedData.__dict__.keys())
