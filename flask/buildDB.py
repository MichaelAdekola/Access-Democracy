# Access Democracy 2020
# Create the database

import sqlite3
import csv
import os
import time

import statics

#

tableAndCSVNames = ["reps", "topicKeywords" ]

#

def dropTable(c, tableName):
#
	c.execute("DROP TABLE IF EXISTS \"" + tableName + "\";")
#

def dropAllTables(c):
#
	c.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tableNames = c.fetchall()
	for tn in tableNames:
		print("Dropping existing table: " + tn[0])
		tableName = tn[0]
		dropTable(c, tableName)
	#
#

def createDBTable(c, tableName, columnNames, columnTypes):
#
	columnCount = len(columnNames)
	
	tableScript = ""
	tableScript += "CREATE TABLE IF NOT EXISTS \"" + tableName + "\" ("
	i = 0
	while i < columnCount:
		tableScript += ("\"" + columnNames[i] + "\"" + " " + columnTypes[i])
		if i < (columnCount-1):
			tableScript += ","
		i += 1
	tableScript += ");"
	
	c.executescript(tableScript)
#

def insertDataToDBTable(c, valuesList, tableName, columnNames): # valuesList is a list of lists - pass in exactly what was extracted from the CSV
#
	print("insertDataToDBTable() begun")
	
	columnCount = len(columnNames)
	rowCount = len(valuesList)
	
	print("columnCount: ", columnCount)
	print("rowCount: ", rowCount)
	
	start = "INSERT INTO [" + tableName + "] ("
	
	columnNamesFm = ""
	i = 0
	while i < columnCount:
		columnNamesFm += "[" + columnNames[i] + "]"
		if i < (columnCount-1):
			columnNamesFm += ", "
		i += 1
	
	mid = ") VALUES ("
	end = ");"
	
	#Insert the data
	
	#insertScript = ""
	insertScriptList = []
	i = 0
	while i < rowCount:
	#
		values = ""
		j = 0
		while j < columnCount:
		
			#values += ("'" + valuesList[i][j].replace("'", "") + "'") # Using the character ' in an SQL query (such as in O'Brien) causes trouble, so we remove it - 13-5-20
			values += ("'" + valuesList[i][j] + "'")
			
			if j < (columnCount-1):
				values += ", "
			j += 1
		
		#insertScript += (start + columnNamesFm + mid + values + end + "\n")
		insertScriptList += [(start + columnNamesFm + mid + values + end + "\n")]
		
		i += 1
	#
		
	#c.executescript(insertScript) # Is apparently MUCH slower than executing lines individually -- no idea why - 13-5-20
	for sl in insertScriptList:
		c.execute(sl)
	#
#

def insertDataToDBTable_tuples(c, tuplesList, tableName, columnNames):
#
	print("insertDataToDBTable_tuples() begun")
	
	columnCount = len(columnNames)
	rowCount = len(tuplesList)
	
	print("columnCount: ", columnCount)
	print("rowCount: ", rowCount)
	
	start = "INSERT INTO [" + tableName + "] ("
	
	columnNamesFm = ""
	i = 0
	while i < columnCount:
		columnNamesFm += "[" + columnNames[i] + "]"
		if i < (columnCount-1):
			columnNamesFm += ", "
		i += 1
	
	mid = ") VALUES ("
	
	qnMarks = ""
	i = 0
	while i < columnCount:
		qnMarks += "?"
		if i < columnCount-1:
			qnMarks += ","
		i += 1
	
	end = ");"
	
	#Insert the data
	
	sl = start + columnNamesFm + mid + qnMarks + end + "\n"
	
	for tuple in tuplesList:
	#
		c.execute(sl, tuple)
	#
#

def insertCSVData(c, csvFileName):
#
	startTime = time.time()
	
	data = []
	dataNoHeaders = []
	dataColNames = []
	dataColTypes = []
	
	if not csvFileName == "":
	
		if os.path.isfile(csvFileName):
		
			print("Found specified CSV file: ", csvFileName ," - importing...")
			
			data = statics.importCSV(csvFileName)
			
			dataColNames = data[0]
			dataColTypes = data[1]
			
			#dataNoHeaders = data[:] # Copy the list (via slicing) # Until 3-9-20
			
			for item in data:
			#
				# if all(item):
				
				for entry in item:
					if entry.rstrip() != "":
						dataNoHeaders += [item]
						break
				
			#
			
			del dataNoHeaders[0] # Delete column name line
			del dataNoHeaders[0] # Delete column type line
		#
		
		if len(data) == 0:
			print("Error: Specified CSV file data is empty")
			return 0
		#
	#
	
	columnCount = len(data[0])
	rowCount = len(data)
	rowCountNH = len(dataNoHeaders)
	
	if rowCountNH > 0:
	
		print("Column count: "+ str(columnCount))
		print("Row count: "+ str(rowCount))
		print("Row count NH: "+ str(rowCountNH))
		
		print("IMPORTED CSV DATA COMPLETE IN:", time.time() - startTime, "sec")
		
		#
		#
				
		print("CREATING DATABASE TABLE - Please wait....")
		
		spl = csvFileName.split(".", 1)
		tableName = spl[0]
		
		# Column names must be the first row of the CSV, and column types must be the second row
		# Alternatively, we could make it so these are automatically determined
		
		createDBTable(c, tableName, dataColNames, dataColTypes)
		
		insertDataToDBTable(c, dataNoHeaders, tableName, dataColNames)
		
	else:
	
		print("Error: CSV contains no data")
		return 0
		
	return 1
#

def runBuildDB(csvFileNames):

	startTime = time.time()

	conn = sqlite3.connect("db1.db") #Will create the db file if it doesn't already exist
	conn.text_factory = str
	c = conn.cursor()
	
	#
	#
	
	#dropAllTables(c) #Drop any pre-existing tables in the database
	
	c.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tableNames = c.fetchall()
	
	tableNames_new = []
	for entry in tableNames:
		tableNames_new += [entry[0]]
	tableNames = tableNames_new
	
	for entry in tableAndCSVNames: # Drop only the tables we would override here 
	#
		if entry in tableNames:
			print("Dropping existing table: " + entry)
			dropTable(c, entry)
	#
	#
	
	for entry in csvFileNames:
	#
		bSuccess = insertCSVData(c, entry)
		print("bSuccess: ", bSuccess)
	#
	
	conn.commit()
	conn.close()
	
	print("BUILD DATABASE COMPLETE IN:", time.time() - startTime, "sec")
#

#
#

if __name__ == "__main__": # So it doesn't run when we import this script

	csvNames = []
	for i in tableAndCSVNames:
		csvNames += [i + ".csv"]

	#runBuildDB(["topics.csv", "reps.csv", "topicKeywords.csv" ])
	runBuildDB(csvNames)
	
	input('Press ENTER to exit')