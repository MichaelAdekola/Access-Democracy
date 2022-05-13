# Access Democracy 2020
# Get bill data from votes and proceedings pages

import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent

#import sqlite3
import time

import random

import statics_webscraping
import statics

#

def runWebScraping():
#	
	result = []
	
	startTime = time.time()
	
	topicKeywordsDict = statics_webscraping.importTopicKeywordsToDict()
	
	maxReconnectionTries = 20
	currReconnectionTries = 0
	
	ua = UserAgent()
	
	def getRandUAHeader(): # Local function
	#
		return {
		"User-Agent": ua.random
		}
	#
	
	# ua = UserAgent()
	# header = {
    # "User-Agent": ua.random
	# }
	
	header = getRandUAHeader()
	
	def remodulate():
	#
		nonlocal currReconnectionTries
		nonlocal maxReconnectionTries
		nonlocal header
		
		currReconnectionTries += 1
		if currReconnectionTries > maxReconnectionTries:
			print("Error: Max reconnection tries exceeded - quitting - BBB")
			quit()
		
		print("Connection failure - page: Remodulating for re-attempt")
		header = getRandUAHeader()
		
		time.sleep(random.randrange(60, 120)) # Wait for a bit before retrying - makes it seem more organic
		#time.sleep(1) # Wait for a bit before retrying - makes it seem more organic
		
		#Possible: We could use a VPN to switch our IP too ?
	#
	
	#
	
	#https://www.aph.gov.au/Parliamentary_Business/Chamber_documents/HoR/Votes_and_Proceedings/votes # List of these URLs located here
	
	#
	
	#url = "https://www.aph.gov.au/Parliamentary_Business/Chamber_documents/HoR/Votes_and_Proceedings/~/link.aspx?_id=F578A9450B854E8D8ADBA9609BF8C772&_z=z" # 45th parliament
	#url = "https://www.aph.gov.au/Parliamentary_Business/Chamber_documents/HoR/Votes_and_Proceedings" # 46th parliament
	
	urls = []
	#urls += ["https://www.aph.gov.au/Parliamentary_Business/Chamber_documents/HoR/Votes_and_Proceedings/~/link.aspx?_id=240969CC6D30422987EEEF86CACAA97C&_z=z"] # 42nd to 44th Parliaments - 2008-2016
	urls += ["https://www.aph.gov.au/Parliamentary_Business/Chamber_documents/HoR/Votes_and_Proceedings/~/link.aspx?_id=F578A9450B854E8D8ADBA9609BF8C772&_z=z"] # 45th parliament - 2016-2019
	urls += ["https://www.aph.gov.au/Parliamentary_Business/Chamber_documents/HoR/Votes_and_Proceedings"] # 46th parliament - 2019-?
	
	billPageCount = 0
	
	for url in urls:
	#
		#page = requests.get(url, headers=header, verify=False)
		
		page = None
		while True:
			try:
				page = requests.get(url, headers=header, verify=False)
				break
			except Exception:
				remodulate()
				continue
		
		soup = BeautifulSoup(page.content, 'html.parser')
		
		for a in soup.find_all('a', href=True): # Removed 'soup.tbody' as there is more than one tbody on the page and we weren't getting the links from all of them - 21-9-20
		#
			if not a.text.isdigit(): # 21-9-20 - avoid following irrelevant links - links on the given pages are drawn as digits representing dates
				continue
			
			#
			#
			
			print(a.text + ": ", a['href'])
			
			#continue
			
			#
			#
			
			#print("page2 = requests.get(a['href'])")
			#page2 = requests.get(a['href'])
			
			page2 = None
			while True:
				try:
					page2 = requests.get(a['href'])
					break
				except Exception:
					remodulate()
					continue
			
			print("BeautifulSoup(page2.content, 'html.parser')")
			soup2 = BeautifulSoup(page2.content, 'html.parser')
			
			for b in soup2.find_all('a', href=True, string=re.compile('BILL')): # Finds links which contain the word BILL -- generally found in a box on the left side of the page
			#
				#Found a 'BILL' page
				
				billPageCount += 1
				
				pageURL = b['href']
				print("Found the URL:", pageURL)
				print(soup2.title)
				
				#print("page3 = requests.get(pageURL)")
				#page3 = requests.get(pageURL)
				
				page3 = None
				while True:
					try:
						page3 = requests.get(pageURL)
						break
					except Exception:
						remodulate()
						continue
				
				print("soup3 = BeautifulSoup(page3.content,'html.parser')")
				soup3 = BeautifulSoup(page3.content,'html.parser')
				
				billName = "null"
				
				titleText = soup3.find('title').text
				print("titleText: ", titleText)
				print("")
				billName = titleText
				
				#
				
				billDate = "null"
				
				#
				# Now get all of the metadata stored on the page - including the date (only one we are storing at the moment)
				
				metaDataItems = soup3.findAll("dt", {"class": "mdLabel"})
				
				print("")
				print("")
				print("len(metaDataItems):", len(metaDataItems))
				for mdLab in metaDataItems:
				#					
					mdItem = mdLab.find_next('p', {"class": "mdItem"})
					
					print(mdLab.text, ":", mdItem.text)
					
					if mdLab.text.lower().strip() == "date":
					#
						billDate = mdItem.text
					#
				#
				print("")
				print("")
				
				#
				# Now we need to figure out the topic of the page/bill
				
				textToCheck = []
				textToCheck += titleText.split()
				
				dps = soup3.findAll("p", {"class": "DPSEntryDetail"})
				for x in dps:
					print(x.text)
					textToCheck += x.text.split()
				
				topicName = statics_webscraping.determineTopicName(textToCheck, topicKeywordsDict)
				
				print("")
				print("topicName (from statics_webscraping.determineTopicName): ", topicName)
				print("")
				
				#
				#
				#
				#
				
				names_ayes = []
				names_noes = []
				
				bFoundAyeAndNay = False
				bPassedStage2 = False
							
				ayes = soup3.findAll("p", {"class": "DIVAyes"})
				noes = soup3.findAll("p", {"class": "DIVNoes"})
				
				ayeToUse = None
				nayToUse = None
				
				#if len(ayes) == 1 and len(noes) == 1:
					#bFoundAyeAndNay = True
				
				if len(ayes) > 0 and len(noes) > 0 and len(ayes) == len(noes):
				#
					ayeToUse = ayes[len(ayes)-1] # Last one on the page
					nayToUse = noes[len(noes)-1]
					bFoundAyeAndNay = True
				#
				
				if bFoundAyeAndNay:
				#
					print("Found at least one Aye and Nay")
					
					currSib = ayeToUse # ayes[0]
					while currSib.name != 'table' and currSib is not None: #Find the next table
						currSib = currSib.nextSibling
					#print(currSib.text)
					table = currSib
					
					tableRows = table.find_all("p",{"class":"DIVName"})
					
					print("")
					print("len(tableRows)", len(tableRows))
					print("")
					
					print("")
					print("AYES:")
					for rw in tableRows:
						oneLine = rw.text.replace("\n", " ")
						oneLine = oneLine.replace("  ", " ")
						oneLine = oneLine.strip()
						print(oneLine)
						names_ayes += [oneLine]
					print("")
					
					currSib = nayToUse # noes[0]
					while currSib.name != 'table' and currSib is not None: #Find the next table
						currSib = currSib.nextSibling
					#print(currSib.text)
					table = currSib
					
					tableRows = table.find_all("p",{"class":"DIVName"})
					
					print("")
					print("len(tableRows)", len(tableRows))
					print("")
					
					print("")
					print("NOES:")
					for rw in tableRows:
						oneLine = rw.text.replace("\n", " ")
						oneLine = oneLine.replace("  ", " ")
						oneLine = oneLine.strip()
						print(oneLine)
						names_noes += [oneLine]
					print("")
				#
				
				#
				
				if len(names_ayes) > 0 and len(names_noes) > 0:
					bPassedStage2 = True
				
				if bPassedStage2:
				#
					print("Passed stage 2")
					
					
				#
				#
				
				textToCheck_oneLine = ""
				for word in textToCheck:
					textToCheck_oneLine += (word + " ")
				
				#
				
				#currResult = [(billName, billDate, topicName, names_ayes, names_noes, pageURL)]
				billData = statics_webscraping.BillData(billName, billDate, topicName, names_ayes, names_noes, pageURL, textToCheck_oneLine)
				
				
				
				#TESTING
				# # # Print one at a time to the file - for quick testing
				resultToTestPrint = []
				resultToTestPrint += [billData]
				statics_webscraping.printWebScrapingResultToFile(resultToTestPrint)
				
				# statics_webscraping.writeWebScrapingResultToDB(resultToTestPrint)
				# # #
				#
				
				print("")
				print("billPageCount so far: ", billPageCount)
				print("currReconnectionTries so far: ", currReconnectionTries)
				#print("time elapsed so far:", time.time() - startTime, "sec")
				print("time elapsed so far:", statics.display_time(time.time() - startTime))
				print("")
				
				result += [billData]
			#
		#
	#
	
	print("")
	
	#print("runWebScraping() COMPLETE IN:", time.time() - startTime, "sec")
	print("runWebScraping() COMPLETE IN:", statics.display_time(time.time() - startTime))
	
	print("billPageCount final: ", billPageCount)
	
	print("currReconnectionTries final: ", currReconnectionTries)
	
	return result
#

if __name__ == "__main__": # So it doesn't run when we import this script

	wsResult = runWebScraping()
	statics_webscraping.writeWebScrapingResultToDB(wsResult)
	statics_webscraping.printWebScrapingResultToFile(wsResult, "webscrapingAllBillsOutput1.txt")

	input('Press ENTER to exit')