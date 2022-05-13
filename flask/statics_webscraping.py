# Access Democracy 2020

import io
import sqlite3
import time

import re

#import urllib
#import os
import requests

import statics
import buildDB

#

class BillData:
	def __init__(self, billName, billDate, topicName, names_ayes, names_noes, pageURL, textToCheck):
		self.billName = billName
		self.billDate = billDate
		self.topicName = topicName
		self.names_ayes = names_ayes #list
		self.names_noes = names_noes #list
		self.pageURL = pageURL
		self.textToCheck = textToCheck
	#
#

#

def importTopicKeywordsToDict():
	
	# Open the DB and get the SQL table topicKeywords and transform it into a set of pairs
	
	topicKeywordsDict = {}
	
	queryStr = "SELECT * from topicKeywords"
	ret = []
	try:
	#
		conn = sqlite3.connect("db1.db", timeout=10)
		c = conn.cursor()
		c.execute(queryStr)
		ret = c.fetchall()
		
		for row in ret:
		#
			#print(row)
			
			word = row[0].lower().strip()
			
			if word not in topicKeywordsDict:
			#
				#topicKeywordsDict[word] = row[1].strip() # Until 3-9-20
				
				#
				
				toAdd = row[1].strip()
				
				if row[2].strip() != "":
					toAdd += "|" + row[2].strip()
				
				#toAdd = toAdd.replace("||", "|")
				#toAdd = toAdd.replace("| |", "|")
				
				topicKeywordsDict[word] = toAdd
			#
		#
		
		#for x in topicKeywordsDict:
			#print(x, topicKeywordsDict[x]) # Key, Value
		#
		
		conn.close()
	#
	except Exception as e:
	#
		raise e
	#

	
	return topicKeywordsDict
#

def printWebScrapingResultToFile(wsResult, fileName = "webscrapingTestOutput1.txt"): #wsResult should be a list of BillData objects
#	
	#f = open("webscrapingTestOutput1.txt", "a")
	with io.open(fileName, "w", encoding="utf-8") as f:
		
		for bill in wsResult:
		#
			f.write("<BILL>")
			f.write("\n")
			
			f.write("\n")
			
			#
			
			f.write("<BILLNAME>")
			f.write("\n")
			
			f.write(bill.billName)
			f.write("\n")
			
			f.write("</BILLNAME>")
			f.write("\n")
			
			f.write("\n")
			
			
			
			f.write("<BILLDATE>")
			f.write("\n")
			
			f.write(bill.billDate)
			f.write("\n")
			
			f.write("</BILLDATE>")
			f.write("\n")
			
			f.write("\n")
			
			
			
			f.write("<BILLTOPIC>")
			f.write("\n")
			
			f.write(bill.topicName)
			f.write("\n")
			
			f.write("</BILLTOPIC>")
			f.write("\n")
			
			f.write("\n")
						
			#
			
			f.write("<AYES>")
			f.write("\n")
			
			for aye in bill.names_ayes:
				f.write(aye)
				f.write("\n")
				
			f.write("</AYES>")
			f.write("\n")
			
			f.write("\n")
			
			#
			
			f.write("<NOES>")
			f.write("\n")
			
			for nay in bill.names_noes:
				f.write(nay)
				f.write("\n")
				
			f.write("</NOES>")
			f.write("\n")
			
			f.write("\n")
			
			#
			
			f.write("<PAGEURL>")
			f.write("\n")
			
			f.write(bill.pageURL)
			f.write("\n")
			
			f.write("</PAGEURL>")
			f.write("\n")
			
			f.write("\n")
			
			#
			
			f.write("<TEXTTOCHECK>")
			f.write("\n")
			
			f.write(bill.textToCheck)
			f.write("\n")
			
			f.write("</TEXTTOCHECK>")
			f.write("\n")
			
			f.write("\n")
			
			#
			
			f.write("</BILL>")
			f.write("\n")
			
			f.write("\n")
		#
		
		f.close()
	#
#

# Method for importing the above data from file into a list of BillData
def importWSResultFromFile(fileName = "webscrapingAllBillsOutput1.txt"):
#
	startTime = time.time()
	
	wsResult = []
	
	#
	
	billName = ""
	billDate = ""
	topicName = ""
	names_ayes = []
	names_noes = []
	pageURL = ""
	textToCheck = ""
	
	mode = 0
	
	#
	
	with io.open(fileName, "r", encoding="utf-8") as f:
	#	
		lines = f.readlines()
		
		i = 0
		for line in lines:
		#
			line = line.rstrip()
			
			#print(line)
			
			#print("Line {}: {}".format(cnt, line.strip()))
			
			if line == "": # Skip other checks on empty lines for efficiency
				continue
						
			if mode == 0 and line == "<BILL>":
			#
				mode = 1
				
				billName = ""
				billDate = ""
				topicName = ""
				names_ayes = []
				names_noes = []
				pageURL = ""
				textToCheck = ""
				
				continue
			#
			
			if mode > 0: # Creating a bill
			#
				if line == "</BILL>": # End of bill
				#
					mode = 0
					wsResult += [BillData(billName, billDate, topicName, names_ayes, names_noes, pageURL, textToCheck)]
					#print("ADDING BILL")
					continue
				#
				
				if line == "<BILLNAME>":
					mode = 2
					continue
				
				if line == "</BILLNAME>":
					mode = 1
					continue
				
				if line == "<BILLDATE>":
					mode = 3
					continue
				
				if line == "</BILLDATE>":
					mode = 1
					continue
				
				if line == "<BILLTOPIC>":
					mode = 4
					continue
				
				if line == "</BILLTOPIC>":
					mode = 1
					continue
				
				if line == "<AYES>":
					mode = 5
					continue
				
				if line == "</AYES>":
					mode = 1
					continue
				
				if line == "<NOES>":
					mode = 6
					continue
				
				if line == "</NOES>":
					mode = 1
					continue
				
				if line == "<PAGEURL>":
					mode = 7
					continue
				
				if line == "</PAGEURL>":
					mode = 1
					continue
				
				if line == "<TEXTTOCHECK>":
					mode = 8
					continue
				
				if line == "</TEXTTOCHECK>":
					mode = 1
					continue
				
				#
				
				if mode == 2:
					billName = line
					#print("billName: ", billName)
				
				if mode == 3:
					billDate = line
				
				if mode == 4:
					topicName = line
				
				if mode == 5:
					names_ayes += [line]
				
				if mode == 6:
					names_noes += [line]
				
				if mode == 7:
					pageURL = line
				
				if mode == 8:
					textToCheck = line
			#
			i += 1
		#
	#
	
	print("importWSResultFromFile() COMPLETE IN:", time.time() - startTime, "sec")
	
	return wsResult
#

def importRepData(c):
#	
	queryStr = "SELECT * from repsB"
	c.execute(queryStr)
	ret = c.fetchall()
	
	surnames = []
	firstNames = []
	preferredFirstNames = []
	middleNames = []
	titles = []
	
	for row in ret:
	#
		regex = re.compile('[^a-zA-Z ]') # Regex matches anything that isn't after the ^ hat, so here we only keep the things that ARE after the hat inside the square brackets
		
		sn = row[5].lower().strip()
		sn = regex.sub('', sn)
		
		fn = row[4].lower().strip()
		fn = regex.sub('', fn)
		
		#pn = row[4].lower().strip()
		#pn = regex.sub('', pn)
		
		#mn = row[5].lower().strip()
		#mn = regex.sub('', mn)
		
		tt = row[1].lower().strip()
		tt = regex.sub('', tt)
		
		surnames += [sn]
		firstNames += [fn]
		
		#preferredFirstNames += [pn]
		preferredFirstNames += [fn] # 21-9-20
		
		#middleNames += [mn]
		middleNames += [""] # 21-9-20
		
		titles += [tt]
	#
	
	#for surname in surnames:
		#print(surname)
	
	return (surnames, firstNames, preferredFirstNames, middleNames, titles)
#

def importRepData_full(c):
#	
	queryStr = "SELECT * from reps"
	c.execute(queryStr)
	return (c.fetchall())
#

def importBillData_full(c):
#	
	queryStr = "SELECT * from bills"
	c.execute(queryStr)
	return (c.fetchall())
#

def importBillBData_full(c):
#	
	queryStr = "SELECT * from billsB"
	c.execute(queryStr)
	return (c.fetchall())
#

def checkNameGetRepIdx(checkName): # Should be obsolete now that we are using repsB
#
	conn = sqlite3.connect("db1.db") #Will create the db file if it doesn't already exist
	conn.text_factory = str
	c = conn.cursor()
		
	# Import data from reps table into lists - their pos in the list will be their rowID(-1)
	# Can't use key pairs here as there are often multiple reps with the same surnames
	
	tpl = importRepData(c)
	
	surnames = tpl[0]
	firstNames = tpl[1]
	preferredFirstNames = tpl[2]
	middleNames = tpl[3]
	titles = tpl[4]
	
	conn.close()
	
	repIdx = -1
	
	regex = re.compile('[^a-zA-Z ]') # Regex matches anything that isn't after the ^ hat, so here we only keep the things that ARE after the hat inside the square brackets
	checkName = regex.sub('', checkName) # Remove any non a-z characters (including numbers)
	
	checkName = checkName.lower().strip()
	
	checkNameSpl = checkName.split() # Default split by whitespace
	
	#
	
	possibleTitles = ["mr", "mrs", "ms", "dr"]
	
	if len(checkNameSpl) == 2:
	#
		# Could be a first and last name, or a title and a surname (Mr, Mrs, Dr)
		
		if checkNameSpl[0] in possibleTitles: # Begins with a title
		#
			sameSnCount = statics.getTimesInList(checkNameSpl[1], surnames)
			if sameSnCount == 1:
			#
				return statics.getItemIdxList(checkNameSpl[1], surnames) # Can only be this entry
			#
			elif sameSnCount > 1:
			#
				# Begins with a title but there are multiple reps with the same surname, so we need to get creative -- check different titles
				
				repIdx = -2
				
				checkTwo = statics.checkTwoItemsSameIdxInTwoLists(checkNameSpl[0], checkNameSpl[1], titles, surnames)
				if checkTwo[0] == True:
				#			
					return checkTwo[1]
				#
			#
		#
		else: # Doesn't begin with a title - should be just a first name and a surname -- it is unlikely, but we now need to check for multiple reps with the same first and surnames
		#			
			repIdx = -3
			
			# This will currently pick the first rep with the given first and last names -- if there is more than one rep with these same names, we will need to perform further checks
			
			checkTwoA = statics.checkTwoItemsSameIdxInTwoLists(checkNameSpl[0], checkNameSpl[1], firstNames, surnames)
			checkTwoB = statics.checkTwoItemsSameIdxInTwoLists(checkNameSpl[0], checkNameSpl[1], preferredFirstNames, surnames)
			if checkTwoA[0] == True or checkTwoB[0] == True:
			#
				print("name: ", checkNameSpl[0], checkNameSpl[1], "*")
				
				if checkTwoA[0] == True:
					return checkTwoA[1]
				if checkTwoB[0] == True:
					return checkTwoB[1]
			#
			else:
				print("name: ", checkNameSpl[0], checkNameSpl[1])
		#
	#
	elif len(checkNameSpl) > 2:
	#
		# Probably means that there are initials being used, but it could also mean someone has more than 2 regular names (someone van someone etc..)
		repIdx = -4
		
		initials = []
		initialCount = 0
		for word in checkNameSpl:
		#
			if len(word) == 1:
				initialCount += 1
				initials += [word]
			#
		#
		
		if initialCount > 0: # There are initials
		#
			repIdx = -5
			
			# Before we check that the initials match, make sure that the surname matches
			
			lastWord = checkNameSpl[len(checkNameSpl)-1]
			idcs = statics.getIndicesMatchingItemInList(lastWord, surnames)
						
			if len(idcs) > 0: # Indices with matching surnames
			#
				# Get the initials for each first name and middle name
				repInitials = []
				i = 0
				for fn in firstNames:
					
					initial2 = ""
					initial3 = ""
					if middleNames[i] != "":
						mnSpl = middleNames[i].split()
						j = 0
						for mnB in mnSpl:
							if j == 0:
								initial2 = mnB[0].strip()
							elif j == 1:
								initial3 = mnB[0].strip()
							j += 1
										
					repInitials += [(fn[0], initial2, initial3)]
					i += 1
					#
				#
				
				i = 0
				for rin in repInitials:
				#
					if i in idcs: # Only continue if there is a matching surname
						if initials[0] == rin[0]:
							if initialCount == 1:
								return i
							if initials[1] == rin[1]:
								if initialCount == 2:
									return i
								if initials[2] == rin[2]:
									if initialCount == 3:
										return i
					
					i += 1
				#
			#
		#
		elif initialCount == 0:
		#
			# Probably means someone has multiple regular names (someone van someone etc..)
			repIdx = -6
			
			lastWord = checkNameSpl[len(checkNameSpl)-1]
			
			surnames_split_lastWord = []
			for surname in surnames:
				splt = surname.split()
				surnames_split_lastWord += [splt[len(splt)-1]]
			
			idcs = statics.getIndicesMatchingItemInList(lastWord, surnames_split_lastWord)
			
			if len(idcs) == 1:
				return idcs[0]
			
			#If we reach here, there is more than one matching split surname -- this would probably be a very rare event
			
			if checkNameSpl[0] in possibleTitles: # Begins with a title
			#
				repIdx = -7
				
				checkTwo = statics.checkTwoItemsSameIdxInTwoLists(checkNameSpl[0], lastWord, titles, surnames_split_lastWord)
				if checkTwo[0] == True:
				#			
					return checkTwo[1]
				#
			#
			else: # Does not begin with a title
			#
				repIdx = -8
				
				checkTwoA = statics.checkTwoItemsSameIdxInTwoLists(checkNameSpl[0], lastWord, firstNames, surnames_split_lastWord)
				checkTwoB = statics.checkTwoItemsSameIdxInTwoLists(checkNameSpl[0], lastWord, preferredFirstNames, surnames_split_lastWord)
				if checkTwoA[0] == True or checkTwoB[0] == True:
				#					
					if checkTwoA[0] == True:
						return checkTwoA[1]
					if checkTwoB[0] == True:
						return checkTwoB[1]
				#
			#
		#
	#
	
	return repIdx
#

def writeWebScrapingResultToDB(wsResult):
#
	if len(wsResult) == 0:
		print("Error: Tried to run writeWebScrapingResultToDB() on an empty wsResult")
		return -1
	
	startTime = time.time()
	
	conn = sqlite3.connect("db1.db") #Will create the db file if it doesn't already exist
	conn.text_factory = str
	c = conn.cursor()
	
	#
	
	# Create a new table named bills and fill each row with data about one bill
	
	#buildDB.createDBTable(c, tableName, columnNames, columnTypes)
	#buildDB.insertDataToDBTable(c, valuesList, tableName, columnNames)
	
	#billName, billDate, topicName, names_ayes, names_noes, pageURL
	#bill.billName
	
	buildDB.dropTable(c, "bills")
	buildDB.dropTable(c, "ayes")
	buildDB.dropTable(c, "noes")
	
	#Tables to create: bills, billAyes, billNoes
	# Bills contains billID, billName, billDate, billTopic and pageURL columns
	# BillAyes contains all of the ayes votes in the entire DB with their accompanying billID
	
	bill_columnNames = ["billID", "billName", "billDate", "billTopic", "pageURL", "ayeCount", "noCount", "textToCheck", "timesReported"]
	bill_columnTypes = ["INT", "TEXT", "TEXT", "TEXT", "TEXT", "INT", "INT", "TEXT", "INT"]
	buildDB.createDBTable(c, "bills", bill_columnNames, bill_columnTypes)
	
	#
	
	ayes_columnNames = ["billID", "mpID"]
	ayes_columnTypes = ["INT", "INT"]
	buildDB.createDBTable(c, "ayes", ayes_columnNames, ayes_columnTypes)
	
	noes_columnNames = ["billID", "mpID"]
	noes_columnTypes = ["INT", "INT"]
	buildDB.createDBTable(c, "noes", noes_columnNames, noes_columnTypes)
	
	#
	
	billTableRows = []
	ayesTableRows = []
	noesTableRows = []
	
	i = 0
	for bill in wsResult:
	#
		# rowA = ["1", "a", "f", "k", "p"]
		# rowB = ["2", "b", "g", "l", "q"]
		# rowC = ["3", "c", "h", "m", "r"]
		# rowD = ["4", "d", "i", "n", "s"]
		# rowE = ["5", "e", "j", "o", "t"]
		
		topicNameToUse = bill.topicName
		
		bUpdateTopicName = True # Optional: Redetermine bill.topicName with statics_webscraping.determineTopicName(textToCheck, topicKeywordsDict)
		if bUpdateTopicName:
			topicKeywordsDict = importTopicKeywordsToDict()
			topicNameToUse = determineTopicName(bill.textToCheck, topicKeywordsDict)
		
		billTableRows += [[str(i), bill.billName, bill.billDate, topicNameToUse, bill.pageURL, str(len(bill.names_ayes)), str(len(bill.names_noes)), bill.textToCheck, "0"]]
		
		for ayeName in bill.names_ayes:
		#
			repIdx = checkNameGetRepIdx(ayeName)
			ayesTableRows += [[str(i), str(repIdx)]]
		#
		
		for nayName in bill.names_noes:
		#
			repIdx = checkNameGetRepIdx(nayName)
			noesTableRows += [[str(i), str(repIdx)]]
		#
				
		i += 1
	#
	
	#billTableRows = [rowA, rowB, rowC, rowD, rowE] # Needs to be a list of lists (each inner list is a row)
	
	buildDB.insertDataToDBTable(c, billTableRows, "bills", bill_columnNames)
	buildDB.insertDataToDBTable(c, ayesTableRows, "ayes", ayes_columnNames)
	buildDB.insertDataToDBTable(c, noesTableRows, "noes", noes_columnNames)
	
	#
	
	conn.commit()
	conn.close()
	
	print("writeWebScrapingResultToDB() COMPLETE IN:", time.time() - startTime, "sec")
	
	return 0
#

#

def writeMPImageWSResultToDB(wsResult): # From webscraping2.py
#
	if len(wsResult) == 0:
		print("Error: Tried to run writeMPImageWSResultToDB() on an empty wsResult")
		return -1
	
	startTime = time.time()

	conn = sqlite3.connect("db1.db") #Will create the db file if it doesn't already exist
	conn.text_factory = str
	c = conn.cursor()
	
	#
	
	buildDB.dropTable(c, "repImages")
	
	columnNames = ["mpID", "imageURL", "imageBlob", "imageBase64"]
	columnTypes = ["INT", "TEXT", "BLOB", "TEXT"]
	buildDB.createDBTable(c, "repImages", columnNames, columnTypes)
	
	#
	
	# Insert data
	# Download each image and convert to BLOB format - https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/
	
	tableRows = [] # Needs to be a list of lists (each inner list is a row)
	
	i = 0
	for item in wsResult:
	#
		#item[0] #MP Name
		#item[1] #Image URL
		
		repIdx = checkNameGetRepIdx(item[0])
		
		#
		
		binImg = None
		if i < 5000:
			binImg = requests.get(item[1]).content # Automatically gets the image as a blob ?
			
		#
		
		blob = sqlite3.Binary(binImg)
		
		b64 = str(statics.blobToBase64(blob))
		b64 = "data:image/jpeg;base64," + b64[2:-1]
		
		#tableRows += [(str(repIdx), item[1], binImg)] # Until 24-8-20 @ 01:48
		tableRows += [(str(repIdx), item[1], blob, b64)]
		
		i += 1
	#
	
	#buildDB.insertDataToDBTable(c, tableRows, "repImages", columnNames)
	buildDB.insertDataToDBTable_tuples(c, tableRows, "repImages", columnNames)
	
	#
	
	conn.commit()
	conn.close()
	
	print("writeMPImageWSResultToDB() COMPLETE IN:", time.time() - startTime, "sec")
	
	return 0
#

def writeWS3ResultToDB(wsResult):
#
	if len(wsResult) == 0:
		print("Error: Tried to run writeWS3ResultToDB() on an empty wsResult")
		return -1
	
	print("writeWS3ResultToDB() running...")
	
	startTime = time.time()

	conn = sqlite3.connect("db1.db") #Will create the db file if it doesn't already exist
	conn.text_factory = str
	c = conn.cursor()
	
	#
	
	buildDB.dropTable(c, "repsB")
	
	columnNames = ["mpID", "imageURL", "imageBase64", "honorific", "first_name", "surname", "postNom", "district", "state", "positions", "party", "twitter", "facebook", "email"]
	columnTypes = ["INT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT",  "TEXT", "TEXT", "TEXT", "TEXT", "TEXT"]
	buildDB.createDBTable(c, "repsB", columnNames, columnTypes)
	
	possibleTitles = ["mr", "mrs", "ms", "dr"]
	possibleHonorifics = ["hon"] + possibleTitles
	possiblePostNoms = ["MP", "OAM", "AM", "QC"]
	
	tableRows = [] # Needs to be a list of lists (each inner list is a row)
	
	i = 0
	for item in wsResult:
	#
		#b64 = "test"
		binImg = requests.get(item[1]).content # Automatically gets the image as a blob
		blob = sqlite3.Binary(binImg)
		b64 = str(statics.blobToBase64(blob))
		b64 = "data:image/jpeg;base64," + b64[2:-1]
		
		positionsConcat = statics.listOfStrsToOneStr(item[4])
		
		state = item[3]
		if item[3] in statics.stateAcronyms:
			state = statics.stateAcronyms[item[3]]
		
		party = item[5]
		if item[5] in statics.partyAcronyms:
			party = statics.partyAcronyms[item[5]]
		
		#
		
		nameSpl = item[0].replace(",", "").strip().split() #split(' ', 3)
		
		nameIdx = 0
		
		honorific = nameSpl[nameIdx]
		nameIdx += 1
		
		first_name = nameSpl[nameIdx]
		nameIdx += 1
		
		if first_name.lower() in possibleTitles: # Occasionally there is an honorific followed by a title
			#Possible for future: Concat first_name in its current form to the honorific
			first_name = nameSpl[nameIdx]
			nameIdx += 1
		
		surname = nameSpl[nameIdx]
		nameIdx += 1
				
		postNom = ""
		while nameIdx < len(nameSpl):
		#
			if nameSpl[nameIdx] not in possiblePostNoms:
			#
				# We have probably found another segment of a two-part surname
				surname += " " + nameSpl[nameIdx]
				nameIdx += 1
				continue
			#
			
			postNom += nameSpl[nameIdx]
			if nameIdx < len(nameSpl)-1:
				postNom += ", "
			
			nameIdx += 1
		#
		
		#
		
		tableRows += [(str(i), item[1], b64,		honorific, first_name, surname, postNom	, item[2], state, positionsConcat, party, item[6], item[7], item[8])]
		
		i += 1
		
		print(i)
	#
	
	buildDB.insertDataToDBTable_tuples(c, tableRows, "repsB", columnNames)
	
	#
	
	conn.commit()
	conn.close()
	
	print("writeWS3ResultToDB() COMPLETE IN:", statics.display_time(time.time() - startTime), "sec")
#

#

def printWS4ResultToFile(wsResult, fileName = "webscrapingAllBillsOutput2.txt"): #wsResult should be a list of BillData objects
#	
	#f = open("webscrapingAllBillsOutput2.txt", "a")
	with io.open(fileName, "w", encoding="utf-8") as f:
		
		for bill in wsResult:
		#
			f.write("<BILLB>\n\n")
			
			f.write("<BILLHEADING>\n" + bill[0] + "\n</BILLHEADING>\n\n")
			f.write("<BILLTYPE>\n" + bill[1] + "\n</BILLTYPE>\n\n")
			f.write("<BILLSPONSORS>\n" + bill[2] + "\n</BILLSPONSORS>\n\n")
			f.write("<BILLPORTFOLIO>\n" + bill[3] + "\n</BILLPORTFOLIO>\n\n")
			f.write("<BILLORIGINATINGHOUSE>\n" + bill[4] + "\n</BILLORIGINATINGHOUSE>\n\n")
			f.write("<BILLSTATUS>\n" + bill[5] + "\n</BILLSTATUS>\n\n")
			f.write("<BILLPARLIAMENTNO>\n" + bill[6] + "\n</BILLPARLIAMENTNO>\n\n")
			f.write("<BILLSUMMARY>\n" + bill[7] + "\n</BILLSUMMARY>\n\n")
			
			f.write("<BILL_REPS_ELEMENTS>\n")
			for item in bill[8]:
				f.write(item[0] + "|" + item[1] + "\n")
			f.write("</BILL_REPS_ELEMENTS>\n\n")
			
			f.write("<BILL_SEN_ELEMENTS>\n")
			for item in bill[9]:
				f.write(item[0] + "|" + item[1] + "\n")
			f.write("</BILL_SEN_ELEMENTS>\n\n")
			
			f.write("<BILLPASSEDREPS>\n" + str(bill[10]) + "\n</BILLPASSEDREPS>\n\n")
			f.write("<BILLPASSEDSEN>\n" + str(bill[11]) + "\n</BILLPASSEDSEN>\n\n")
			f.write("<BILLPASSEDBOTH>\n" + str(bill[12]) + "\n</BILLPASSEDBOTH>\n\n")
			f.write("<BILLHASASSENT>\n" + str(bill[13]) + "\n</BILLHASASSENT>\n\n")
			f.write("<BILLURL>\n" + str(bill[14]) + "\n</BILLURL>\n\n")
			
			f.write("</BILLB>\n\n")
		#
		
		f.close()
	#
#

def importWS4ResultFromFile(fileName = "webscrapingAllBillsOutput2.txt"):
#
	startTime = time.time()
	
	wsResult = []
	
	heading = ""
	type = ""
	sponsors = ""
	portfolio = ""
	originatingHouse = ""
	status = ""
	parliamentNo = ""
	summary = ""
	reps_elements = []
	sen_elements = []
	bHasPassedHouseOfReps_orNoNeed = False
	bHasPassedSenate = False
	bHasPassedBoth = False
	bHasAssent = False
	URL = ""
	
	mode = 0
		
	with io.open(fileName, "r", encoding="utf-8") as f:
	#	
		lines = f.readlines()
		
		i = 0
		for line in lines:
		#
			line = line.rstrip()
			
			if line == "": # Skip other checks on empty lines for efficiency
				continue
						
			if mode == 0 and line == "<BILLB>":
			#
				mode = 1
				
				heading = ""
				type = ""
				sponsors = ""
				portfolio = ""
				originatingHouse = ""
				status = ""
				parliamentNo = ""
				summary = ""
				reps_elements = []
				sen_elements = []
				bHasPassedHouseOfReps_orNoNeed = False
				bHasPassedSenate = False
				bHasPassedBoth = False
				bHasAssent = False
				URL = ""
				
				continue
			#
			
			if mode > 0: # Creating a bill
			#
				if line == "</BILLB>": # End of bill
				#
					mode = 0
					wsResult += [(heading, type, sponsors, portfolio, originatingHouse, status, parliamentNo, summary, reps_elements, sen_elements, bHasPassedHouseOfReps_orNoNeed, bHasPassedSenate, bHasPassedBoth, bHasAssent, URL)]
					continue
				#
				
				if line == "<BILLHEADING>":
					mode = 2
					continue
				if line == "</BILLHEADING>":
					mode = 1
					continue
				
				if line == "<BILLTYPE>":
					mode = 3
					continue
				if line == "</BILLTYPE>":
					mode = 1
					continue
				
				if line == "<BILLSPONSORS>":
					mode = 4
					continue
				if line == "</BILLSPONSORS>":
					mode = 1
					continue
				
				if line == "<BILLPORTFOLIO>":
					mode = 5
					continue
				if line == "</BILLPORTFOLIO>":
					mode = 1
					continue
				
				if line == "<BILLORIGINATINGHOUSE>":
					mode = 6
					continue
				if line == "</BILLORIGINATINGHOUSE>":
					mode = 1
					continue
				
				if line == "<BILLSTATUS>":
					mode = 7
					continue
				if line == "</BILLSTATUS>":
					mode = 1
					continue
				
				if line == "<BILLPARLIAMENTNO>":
					mode = 8
					continue
				if line == "</BILLPARLIAMENTNO>":
					mode = 1
					continue
				
				if line == "<BILLSUMMARY>":
					mode = 9
					continue
				if line == "</BILLSUMMARY>":
					mode = 1
					continue
				
				if line == "<BILL_REPS_ELEMENTS>":
					mode = 10
					continue
				if line == "</BILL_REPS_ELEMENTS>":
					mode = 1
					continue
				
				if line == "<BILL_SEN_ELEMENTS>":
					mode = 11
					continue
				if line == "</BILL_SEN_ELEMENTS>":
					mode = 1
					continue
				
				if line == "<BILLPASSEDREPS>":
					mode = 12
					continue
				if line == "</BILLPASSEDREPS>":
					mode = 1
					continue
				
				if line == "<BILLPASSEDSEN>":
					mode = 13
					continue
				if line == "</BILLPASSEDSEN>":
					mode = 1
					continue
				
				if line == "<BILLPASSEDBOTH>":
					mode = 14
					continue
				if line == "</BILLPASSEDBOTH>":
					mode = 1
					continue
				
				if line == "<BILLHASASSENT>":
					mode = 15
					continue
				if line == "</BILLHASASSENT>":
					mode = 1
					continue
				
				if line == "<BILLURL>":
					mode = 16
					continue
				if line == "</BILLURL>":
					mode = 1
					continue
				
				#
				
				if mode == 2:
					heading = line
				
				if mode == 3:
					type = line
				
				if mode == 4:
					sponsors = line
				
				if mode == 5:
					portfolio = line
					
				if mode == 6:
					originatingHouse = line
				
				if mode == 7:
					status = line
				
				if mode == 8:
					parliamentNo = line
				
				if mode == 9:
					summary = line
				
				if mode == 10:
					spl = line.split("|")
					reps_elements += [[spl[0], spl[1]]]
				
				if mode == 11:
					spl = line.split("|")
					sen_elements += [[spl[0], spl[1]]]
				
				if mode == 12:
					bHasPassedHouseOfReps_orNoNeed = line == 'True'
				
				if mode == 13:
					bHasPassedSenate = line == 'True'
				
				if mode == 14:
					bHasPassedBoth = line == 'True'
				
				if mode == 15:
					bHasAssent = line == 'True'
				
				if mode == 16:
					URL = line
			#
			i += 1
		#
	#
	
	print("importWS4ResultFromFile() COMPLETE IN:", time.time() - startTime, "sec")
	
	return wsResult
#

#

def findWS1BillsThatMatchWS4Bill(billBNameToMatch, importedBillData):
#
	result = []
	
	i = 0
	for bd in importedBillData:
	#
		regex = re.compile('[^a-zA-Z1-9 ]')
		
		spl = bd[1].split(":")
		
		toCheck = spl[len(spl)-1][3:]
		
		billName = regex.sub('', toCheck)
		billName = billName.lower().strip()
		
		billNameB = regex.sub('', billBNameToMatch)
		billNameB = billNameB.lower().strip()
		
		#print("billName: ", billName)
		#print("billNameB: ", billNameB)
		
		#Possible: Create another system to match the name strings -- perhaps get a percentage of words which match and are in the same order?
		
		
		
		#if billName == billNameB:
		#if statics.compareStrs1(billName, billNameB) >= 0.75:# Check for percentage of identical words in each - ignores order
		if statics.compareStrs2(billName, billNameB) == True: # Directly compare strings
		#if statics.compareStrs3(billName, billNameB) >= 0.9: # Uses library function - seems to be quite slow
			result += [i]
		
		i += 1
	#
	
	return result
#

def writeWS4ResultToDB(wsResult):
#
	if len(wsResult) == 0:
		print("Error: Tried to run writeWS4ResultToDB() on an empty wsResult")
		return -1
	
	print("writeWS4ResultToDB() running...")
	
	startTime = time.time()
	
	topicKeywordsDict = importTopicKeywordsToDict()

	conn = sqlite3.connect("db1.db") #Will create the db file if it doesn't already exist
	conn.text_factory = str
	c = conn.cursor()
	
	#
	
	importedBillData = importBillData_full(c)
	
	#
	
	buildDB.dropTable(c, "billsB")
	
	columnNames = ["billB_ID", "heading", "topics", "matches", "type", "sponsors", "portfolio", "originatingHouse", "status", "parliamentNo", "summary", "reps_elements", "reps_elements_dates", "sen_elements", "sen_elements_dates", "bHasPassedHouseOfReps_orNoNeed", "bHasPassedSenate", "bHasPassedBoth", "bHasAssent", "URL", "timesReported"]
	columnTypes = ["INT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "INT"]
	buildDB.createDBTable(c, "billsB", columnNames, columnTypes)
	
	#
	
	tableRows = [] # Needs to be a list of lists (each inner list is a row)
	
	i = 0
	for item in wsResult:
	#
		reps_elements_str = ""
		reps_elements_dates_str = ""
		sen_elements_str = ""
		sen_elements_dates_str = ""
		
		j = 0
		for elem in item[8]:
			reps_elements_str += elem[0]
			reps_elements_dates_str += elem[1]
			if j < len(item[8]) - 1:
				reps_elements_str += "|"
				reps_elements_dates_str += "|"
			j += 1
		
		j = 0
		for elem in item[9]:
			sen_elements_str += elem[0]
			sen_elements_dates_str += elem[1]
			if j < len(item[9]) - 1:
				sen_elements_str += "|"
				sen_elements_dates_str += "|"
			j += 1
		
		topicNames = determineTopicName(item[0] + " " + item[7], topicKeywordsDict)
		
		matches = findWS1BillsThatMatchWS4Bill(item[0], importedBillData)
		matches_str = ""
		j = 0
		for match in matches:
			matches_str += str(match)
			if j < len(matches) - 1:
				matches_str += "|"
			j += 1
		
		tableRows += [(str(i), item[0], topicNames, matches_str, item[1], item[2], item[3], item[4], item[5], item[6], item[7], reps_elements_str, reps_elements_dates_str, sen_elements_str, sen_elements_dates_str, item[10], item[11], item[12], item[13], item[14], 0)]
		
		i += 1
	#
	
	#
	
	buildDB.insertDataToDBTable_tuples(c, tableRows, "billsB", columnNames)
	
	#
	
	conn.commit()
	conn.close()
	
	print("writeWS4ResultToDB() COMPLETE IN:", statics.display_time(time.time() - startTime), "sec")
#

#
#
#
#

# Check every word on the page against each entry in the topicKeywords table in the DB. 
# Keep count of the times a match is found and against what. 
# Once the doc has finished iterating, find the keyword which appeared the most often and set its paired topic in topicKeywords to be the bill's topic.
def determineTopicName(textToCheck, topicKeywordsDict):
#
	# print("len(topicKeywordsDict): " + str(len(topicKeywordsDict)))
	
	topicName = "Unknown Topic"
	topicDict = {}
	
	textToCheckSpl = []
	if isinstance(textToCheck, list):
		textToCheckSpl = textToCheck
	elif isinstance(textToCheck, str):
		textToCheckSpl = textToCheck.split(" ")

	for word in textToCheckSpl:
	#
		regex = re.compile('[^a-zA-Z ]')
		word = regex.sub('', word) # Remove any non a-z characters (including numbers)
		
		word = word.lower().strip() # To lowercase and remove any whitespace
		#print(word)
		
		if word in topicKeywordsDict:
		#
			# Added multiple topics to one keyword --  rather than 'word = topicKeywordsDict[word]', we can retrieve x number of matching words in this fashion - they would each individually be operated on below (topicDict[word] += 1 etc...)
			
			keyword_s = topicKeywordsDict[word] # Convert to the overall topic name(s) for better results below
			
			#print("word: ", word)
			#print("keyword_s: ", keyword_s)
			
			if "|" in keyword_s: # Multi-keywords
			#
				keywordSpl = keyword_s.split("|")
				
				#print("keywordSpl: ", keywordSpl)
				
				for kw in keywordSpl:
					if kw in topicDict:
						topicDict[kw] += 1
					else:
						topicDict[kw] = 1
			#
			else: # Solo keyword
			#
				if keyword_s in topicDict:
					topicDict[keyword_s] += 1
				else:
					topicDict[keyword_s] = 1
			#
		#
	#
	
	type = 2
	
	#Possible: Before we check for the highest, we could check for topics which appear more often -- we could then place bills in multiple categories
	#This would require the ability for each bill to have multiple topics stored and retrieved (already done - 30-8-20)

	if type == 1: # Find most common category - just one category
	#
		if len(topicDict) > 0:
		#
			highestVal = 0
			highestValWord = ""
			for x in topicDict:
			#
				#print(x, topicDict[x]) # Key, Value
				
				if topicDict[x] > highestVal:
					highestVal = topicDict[x]
					highestValWord = x
				#
			#
			
			topicName = highestValWord
		#
	#
	elif type == 2: # Multiple categories
	#
		if len(topicDict) > 0:
		#
			topicName = ""
			i = 0
			for x in topicDict:
			#
				topicName += x
				if i < len(topicDict)-1:
					topicName += "|"
				i += 1
			#
		#
	#
	
	return topicName
#














































