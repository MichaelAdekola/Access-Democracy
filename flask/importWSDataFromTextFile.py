# Access Democracy 2020

import statics
import statics_webscraping

# Note: Run this whenever editing topicKeywords to determine the bill topics again -- for the 'bill' table in the DB (results stored there)
# Far quicker to reimport WS data from file than to run the WS again

def importWSDataFromTextFile():
#
	wsResult = statics_webscraping.importWSResultFromFile(fileName = "webscrapingAllBillsOutput1.txt")
	
	print("len(wsResult): ", len(wsResult))
	print("Writing to DB....")
	
	statics_webscraping.writeWebScrapingResultToDB(wsResult)
#

#
#
#
#

if __name__ == "__main__": # So it doesn't run when we import this script
#
	importWSDataFromTextFile()
	
	input('Press ENTER to exit')
#