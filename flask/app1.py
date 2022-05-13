# Access Democracy 2020

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, send_file
app = Flask(__name__, static_url_path='/static')

import csv, sqlite3, datetime, io, math

#import pickle

import time
#import atexit
#from apscheduler.schedulers.background import BackgroundScheduler

import base64

#import statics
#import statics_webscraping
#import webscraping1
#import webscraping2

import os
import sys

#

_bRunningWebScraping = False
_topicKeywords = []

sys.path.insert(0, os.path.dirname(__file__))

#

@app.route("/")
def index():
	return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
	return app.send_static_file('img/favicon.ico')

@app.route('/aus.png')
def logoImg():
	return app.send_static_file('img/aus.png')

@app.route('/email.ico')
def emailIcon():
	return app.send_static_file('img/email.ico')

@app.route('/twitter.ico')
def twitterIcon():
	return app.send_static_file('img/twitter.ico')

@app.route('/facebook.ico')
def facebookIcon():
	return app.send_static_file('img/facebook.ico')

@app.route('/profile.ico')
def profileIcon():
	return app.send_static_file('img/profile.ico')

@app.route('/yes.ico')
def yesIcon():
	return app.send_static_file('img/yes.ico')

@app.route('/no.ico')
def noIcon():
	return app.send_static_file('img/no.ico')
	
@app.route('/arrow_rgt.png')
def rgtArrowIcon():
	return app.send_static_file('img/arrow_rgt.png')
	
@app.route('/arrow_lft.png')
def lftArrowIcon():
	return app.send_static_file('img/arrow_lft.png')

@app.route('/loadingIconC')
def loadingIcon1():
	#return app.send_static_file('img/ZZ5H.gif')
	return app.send_static_file('img/loading.gif')

#

@app.route("/api/getTopics", methods=["GET"])
def fetchTopics():
	return jsonify(getTopics())

@app.route("/api/getMPs", methods=["GET"])
def fetchMPs():
	return jsonify(getMPs())

@app.route("/api/getMPImages", methods=["GET"])
def fetchMPImages():
	return jsonify(getMPImages())

@app.route("/api/getMPByDetails/<string:details>")
def fetchMPByDetails(details):
	return jsonify(getMPByDetails(details))

@app.route("/api/getBillByID/<int:id>")
def fetchBillByID(id):
	return jsonify(getBillByID(id))

@app.route("/api/getBillBByID/<int:id>")
def fetchBillBByID(id):
	return jsonify(getBillBByID(id))

@app.route("/api/getPastBillsData/<int:id>")
def fetchPastBillsData(id):
	return jsonify(getPastBillsData(id))

@app.route("/api/getBills")
def fetchBills():
	return jsonify(getBills())

@app.route("/api/getBillsWithTopic/<string:topic>")
def fetchBillsWithTopic(topic):
	return jsonify(getBillsWithTopic(topic))

@app.route("/api/getBillsWithTopic_getAll/<string:topic>")
def fetchBillsWithTopic_getAll(topic):
	return jsonify(getBillsWithTopic_getAll(topic))
	
@app.route("/api/getBillsWithTopic_getAll_withAyesAndNoes/<string:topic>")
def fetchBillsWithTopic_getAll_withAyesAndNoes(topic):
	return jsonify(getBillsWithTopic_getAll_withAyesAndNoes(topic))

@app.route("/api/getBillsWithTopic_getAll_withoutAyesAndNoes/<string:topic>")
def fetchBillsWithTopic_getAll_withoutAyesAndNoes(topic):
	return jsonify(getBillsWithTopic_getAll_withoutAyesAndNoes(topic))

@app.route("/api/getBillsBWithTopic_getAll_withAyesAndNoes/<string:topic>")
def fetchBillsBWithTopic_getAll_withAyesAndNoes(topic):
	return jsonify(getBillsBWithTopic_getAll_withAyesAndNoes(topic))

@app.route("/api/getBillsBWithTopic_getAll_withoutAyesAndNoes/<string:topic>")
def fetchBillsBWithTopic_getAll_withoutAyesAndNoes(topic):
	return jsonify(getBillsBWithTopic_getAll_withAyesAndNoes(topic, True))
	
	
	
@app.route("/api/getBillsBWithTopic_statusBeforeRepsOrSen/<string:topic>")
def fetchBillsBWithTopic_statusBeforeRepsOrSen(topic):
	return jsonify(getBillsBWithTopic_statusBeforeRepsOrSen(topic))
	
	
	
@app.route("/api/getTopicKeywords", methods=["GET"])
def fetchTopicKeywords():
	return jsonify(getTopicKeywords())

#

@app.route("/api/submitToBillReportCount", methods=["POST"])
def r_submitToBillReportCount():
#
	if request.method != "POST":
		return abort(400)
	try:
		#return jsonify(submitToBillReportCount(request.json["item"], request.json["quantity"]))
		return jsonify(submitToBillReportCount(request.json["item"]))
	except Exception as e:
		raise e

def submitToBillReportCount(item):
#
	try:
		conn = sqlite3.connect("db1.db", timeout=10)
		c = conn.cursor()
		
		#c.execute("SELECT timesReported FROM bills WHERE billID = (?)", [item])
		c.execute("SELECT timesReported FROM billsB WHERE billB_ID = (?)", [item])
		
		ret = c.fetchall()
		
		print("ret[0]", ret[0][0])
		print("type(ret[0]): ", type(ret[0][0]))
		
		queryStr = """
		UPDATE billsB
		SET timesReported = (?)
		WHERE billB_ID = (?)
		"""
		
		values = [ret[0][0] + 1, item]
		
		c.execute(queryStr, values)
		
		conn.commit()
		conn.close()
		return True
	except Exception as e:
		raise e
	
	print("item: ", item)
#

def getTopics():
#
	#print("getTopics()")
	
	#return getSQLQueryResult("SELECT * from topics ORDER BY ROWID") # Until 2-9-20
	
	tkwDict = {} #Keys are main topics, values are a list of their sub-topics
	
	i = 0
	while i < len(_topicKeywords):
	#
		mainTopics = _topicKeywords[i][1].split("|")
		subTopics = _topicKeywords[i][2].split("|")
		
		#print(_topicKeywords[i][1])
				
		#if parentTopic not in tkwDict:
		#
			#tkwDict[parentTopic] = ""
		#
		
		if len(mainTopics) > 0: #There are main topics
		#
			j = 0
			while j < len(mainTopics):
			#
				#tkwDict[parentTopic] += mainTopics[j]
				#tkwDict[parentTopic] += "|"
				
				mainTopic = mainTopics[j].strip()
				
				if mainTopic != "":
				#
					if mainTopic not in tkwDict:
					#
						tkwDict[mainTopic] = []
					#
					else:
					#
						k = 0
						while k < len(subTopics):
						#
							subTopic = subTopics[k].strip()
							
							if subTopic != "":
							#
								if subTopic not in tkwDict[mainTopic]:
								#
									tkwDict[mainTopic] += [subTopic]
								#
							#
							
							k += 1
						#
					#
				#
				
				j += 1
			#
		#
		
		i += 1
	#
	
	#print("getTopics() B")
	
	# print(tkwDict.keys()) #Keys are the parent topics
	
	# print(tkwDict.items())
	
	#for item in tkwDict.items():
		#print(item)
	
	#return tkwDict.items()
	
	# We need to transform the contents of tkwDict into a facsimile of the old topics.csv
	# We need to create a list of 2 entry tuples - one for each row
	# If an item in tkwDict has an empty values list, the first entry in the row's tuple will contain the key and the second will be empty
	# If the item has items in the values list, we add a new row for each one of these - the first entry will contain the list value and the second entry will contain the key
	
	result = []
	for item in tkwDict.items():
	#
		result += [[item[0], ""]]
		
		if len(item[1]) > 0:
		#
			for listItem in item[1]:
			#
				result += [[listItem, item[0]]]
			#
		#
	#
	
	#for item in result:
		#print(item)
	
	return result # Needs to be a list of lists - each internal list is one row, NOT a column

#

def getMPs():
	return getSQLQueryResult("SELECT * from repsB ORDER BY mpID")
	
def getMPImages():
#
	query = """SELECT mpID, imageBase64 FROM repsB ORDER BY mpID"""
	return getSQLQueryResult(query)
#

def getMPByDetails(details):
#
	#Katrina Allen, Higgins, 3144, VIC
	
	details = details.replace("%20", " ")
	details = details.replace(",", "")
	spl = details.split()
		
	#resA = getSQLQueryResult("SELECT ROWID, reps.* from reps WHERE instr(reps.'First Name', '" + spl[0] + "') > 0 AND instr(reps.Surname, '" + spl[1] + "') > 0 AND instr(reps.Electorate, '" + spl[2] + "') > 0 ORDER BY ROWID")
	resA = getSQLQueryResult("SELECT * from repsB WHERE instr(repsB.first_name, '" + spl[0] + "') > 0 AND instr(repsB.surname, '" + spl[1] + "') > 0 AND instr(repsB.district, '" + spl[2] + "') > 0 ORDER BY mpID")
	
	#query = """SELECT * FROM repImages WHERE mpID = ? ORDER BY mpID"""
	#resB = getSQLQueryResult_values(query, [ int(resA[0][0])-1 ])
	
	#print(resB)
	
	#Image data, honorific, first name, surname, electorate, party, telephone, electorate address, electorate state, parliamentary title, ministerial title, mpID
	#res = [[resB[0][3], resA[0][1], resA[0][5], resA[0][4], resA[0][9], resA[0][11], resA[0][13], resA[0][15], resA[0][18], resA[0][31], resA[0][32], int(resA[0][0])-1]]
	
	res = resA
	
	return res
#

def getBillsWithTopic(topic):
#
	#return getSQLQueryResult("SELECT bills.billID FROM bills WHERE bills.billTopic = '" + topic + "'")
	return getSQLQueryResult("SELECT bills.billID FROM bills WHERE instr(bills.billTopic, '" + topic + "') > 0 ORDER BY billID") # Substring search
#

def getBillsWithTopic_getAll(topic):
#
	#return getSQLQueryResult("SELECT * FROM bills WHERE bills.billTopic = '" + topic + "'")
	return getSQLQueryResult("SELECT * FROM bills WHERE instr(bills.billTopic, '" + topic + "') > 0 ORDER BY billID") # Substring search
#

def getBillsWithTopic_getAll_withAyesAndNoes(topic):
#
	return getSQLQueryResult("SELECT * FROM bills WHERE instr(bills.billTopic, '" + topic + "') > 0 AND bills.ayeCount > 0 AND bills.noCount > 0 ORDER BY billID") # Substring search
#

def getBillsWithTopic_getAll_withoutAyesAndNoes(topic):
#
	return getSQLQueryResult("SELECT * FROM bills WHERE instr(bills.billTopic, '" + topic + "') > 0 AND bills.ayeCount == 0 AND bills.noCount == 0 ORDER BY billID") # Substring search
#

def getBills():
#
	return getSQLQueryResult("SELECT * FROM bills GROUP BY billTopic ORDER BY billID")
#

def getBillByID(id):
#
	query = """SELECT * FROM bills WHERE billID = ?"""
	ret = getSQLQueryResult_values(query, [id])
	
	return ret
#

def getBillBByID(id):
#
	query = """SELECT * FROM billsB WHERE billB_ID = ?"""
	ret = getSQLQueryResult_values(query, [id])
	
	return ret
#



def getBillsBWithTopic_getAll_withAyesAndNoes(topic, bInvert = False):
#
	origBillData = getSQLQueryResult("SELECT * FROM bills ORDER BY billID")
	
	resA = getSQLQueryResult("SELECT * FROM billsB WHERE instr(billsB.topics, '" + topic + "') > 0 ORDER BY billB_ID") # Substring search
	
	resB = []
	for row in resA:
	#
		row = list(row)
		if "|" in row[3]:
		#
			spl = row[3].split("|")
			#print("spl: ", spl)
			if len(spl) > 0:
			#
				spl.reverse() # So the last page is checked first
				
				for idx in spl:
				#
					idx = int(idx)
					#print("type(origBillData[idx][5]): ", type(origBillData[idx][5]))
					#print("type(origBillData[idx][6]): ", type(origBillData[idx][6]))
					
					# Note: There could be multiple origBillData[idx]es which have ayes and noes - this just takes the first one at the moment - 22-9-20
					# It may be a better idea to get the last one which should be the most recent
					# Update: Have now reversed the split list - hopefully this will mean that the last one is checked first instead
					
					if not bInvert:
					#
						if int(origBillData[idx][5]) > 0 and int(origBillData[idx][6]) > 0:
						#
							#print("idx: ", idx)
							
							row += [idx]
							row += [origBillData[idx][5]]
							row += [origBillData[idx][6]]
							resB += [row]
							break
						#
					#
					else:
					#
						if int(origBillData[idx][5]) == 0 and int(origBillData[idx][6]) == 0:
						#
							row += [idx]
							row += [origBillData[idx][5]]
							row += [origBillData[idx][6]]
							resB += [row]
							break
						#
					#
				#
			#
		#
	#
	
	return resB
#


def getBillsBWithTopic_statusBeforeRepsOrSen(topic):
#
	return getSQLQueryResult("SELECT * FROM billsB WHERE instr(billsB.topics, '" + topic + "') > 0 AND (billsB.status = 'Before Reps' OR billsB.status = 'Before Senate') ORDER BY billB_ID") # Substring search
#



def getTopicKeywords():
	return getSQLQueryResult("SELECT * from topicKeywords ORDER BY ROWID")

def getPastBillsData(id): # Get all of the ayes and noes for the bill with billID = id
#	
	startTime = time.time()
	
	query = """SELECT * FROM ayes WHERE billID = ? ORDER BY billID"""
	ayesForBill = getSQLQueryResult_values(query, [id])
	
	query = """SELECT * FROM noes WHERE billID = ? ORDER BY billID"""
	noesForBill = getSQLQueryResult_values(query, [id])
	
	# Then get the MP data for every MP referenced by their IDs in ayesForBill and noesForBill
	
	res = []
		
	if len(ayesForBill) > 0 and len(noesForBill) > 0:
	#		
		for aye in ayesForBill:
		#
			if aye[1] >= 0: # Some mpIDs in ayes and noes are in the negative, most likely indicating that the MP is no longer an MP
			#
				query = """SELECT * FROM repsB WHERE mpID = ? ORDER BY mpID"""
				repDatA = getSQLQueryResult_values(query, [int(aye[1])]) # Should return just one row
				res += [[int(id), "0", repDatA[0][4], repDatA[0][5], repDatA[0][10], repDatA[0][7], "aye", repDatA[0][11], repDatA[0][12], repDatA[0][13], int(aye[1])]]
			#
			else:
			#
				res += [[int(id), "0", "unknown", "unknown", "unknown", "unknown", "aye", "", "", "", -2]]
			#
		#
		
		for nay in noesForBill:
		#
			if nay[1] >= 0: # Some mpIDs in ayes and noes are in the negative, most likely indicating that the MP is no longer an MP
			#
				query = """SELECT * FROM repsB WHERE mpID = ?"""
				repDatA = getSQLQueryResult_values(query, [int(nay[1])]) # Should return just one row
				res += [[int(id), "0", repDatA[0][4], repDatA[0][5], repDatA[0][10], repDatA[0][7], "nay", repDatA[0][11], repDatA[0][12], repDatA[0][13], int(nay[1])]]
			#
			else:
			#
				res += [[int(id), "0", "unknown", "unknown", "unknown", "unknown", "nay", "", "", "", -2]]
			#
		#
	#
	else:
	#
		res += [[int(id), "0", "novotes", "novotes", "novotes", "novotes", "novotes", "novotes", "novotes", "novotes", -2]]
	#
	
	print("getPastBillsData -- len(res): ", len(res))
	print("getPastBillsData COMPLETE IN:", time.time() - startTime, " sec")
	
	return res
#

def getSQLQueryResult(queryStr):
#
	try:
		conn = sqlite3.connect("db1.db", timeout=10)
		c = conn.cursor()
		c.execute(queryStr)
		ret = c.fetchall()
		conn.close()
		return ret
	except Exception as e:
		raise e
	#
#

def getSQLQueryResult_values(queryStr, values):
#
	try:
		conn = sqlite3.connect("db1.db", timeout=10)
		c = conn.cursor()
		c.execute(queryStr, values)
		ret = c.fetchall()
		conn.close()
		return ret
	except Exception as e:
		raise e
	#
#

# JSON Serialisation
from flask.json import JSONEncoder
class SQLJSONEncoder(JSONEncoder):
	def default(self, obj):
		return obj.__dict__

app.json_encoder = SQLJSONEncoder

def convertSQL(array, object):
	for i in range(len(array)):
		array[i] = object(array[i])
	return array

#
#
#
#

# def tickA():
# #
	# print_date_time()
	# i = 0 # Do nothing
# #

# def tickB():
# #

	# #TODO: Add try/catch around this - 20-8-20
	# #manageWebScraping()
	# i = 0 # Do nothing
# #

# schedulerA = BackgroundScheduler()
# schedulerA.add_job(func=tickA, trigger="interval", seconds=1)
# schedulerA.start()

# schedulerB = BackgroundScheduler()
# schedulerB.add_job(func=tickB, trigger="interval", seconds=10)
# schedulerB.start()

# # Shut down the scheduler when exiting the app
# atexit.register(lambda: schedulerA.shutdown())
# atexit.register(lambda: schedulerB.shutdown())

# #

# def print_date_time():
# #
	# print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
# #

# def manageWebScraping(): #TODO: Run this ASync? Possible with Flask ??
# #
	# global _bRunningWebScraping
	
	# print("manageWebScraping() started")
	
	# wsResult = []
	# if not _bRunningWebScraping:
	# #
		# startTime = time.time()
		
		# #
		# _bRunningWebScraping = True
		
		# # MP images
		# wsResult2 = webscraping2.runWebScraping2()
		
		# # Bill data
		# wsResult = webscraping1.runWebScraping() # This will take a long time (20 mins +)
		
		# _bRunningWebScraping = False
		# #
		
		# print("############################## manageWebScraping COMPLETE IN:", time.time() - startTime, " sec #1")
		
		# statics_webscraping.printWebScrapingResultToFile(wsResult, "webscrapingAllBillsOutput1.txt")
		
		# print("############################## manageWebScraping COMPLETE IN:", time.time() - startTime, " sec #2")
		
		# statics_webscraping.writeWebScrapingResultToDB(wsResult)
		
		# #Serialize the object and store it -- for testing - so we don't have to keep running the web scraping in order to test its results
		# #with open('webscrapingTestOutput1_serialized.pkl', 'wb') as output:
			# #pickle.dump(wsResult, output, pickle.HIGHEST_PROTOCOL)
		
		# print("############################## manageWebScraping COMPLETE IN:", time.time() - startTime, " sec #3")
	# #
	
	# print("manageWebScraping() completed")
# #

# def importWSDataFromTextFile():
# #
	# wsResult = statics_webscraping.importWSResultFromFile(fileName = "webscrapingAllBillsOutput1.txt")
	# statics_webscraping.writeWebScrapingResultToDB(wsResult)
# #

def initialise():
#
	# Called on program start
	
	print("initialise()")
	
	global _topicKeywords
	_topicKeywords = getTopicKeywords()
#

#
#
#
#

#manageWebScraping() # TEST - when ready, run this from a scheduler instead

#importWSDataFromTextFile()

initialise()