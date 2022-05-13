# Access Democracy 2020

import statics
import statics_webscraping

# Note: Run this whenever editing topicKeywords to determine the bill topics again -- for the 'bill' table in the DB (results stored there)
# Far quicker to reimport WS data from file than to run the WS again

def importWS4DataFromTextFile():
#
	wsResult = statics_webscraping.importWS4ResultFromFile(fileName = "webscrapingAllBillsOutput2.txt")
	
	print("len(wsResult): ", len(wsResult))
	print("Writing to DB....")
	
	statics_webscraping.writeWS4ResultToDB(wsResult)
#

#
#
#
#

if __name__ == "__main__": # So it doesn't run when we import this script
#
	importWS4DataFromTextFile()
	
	input('Press ENTER to exit')
#