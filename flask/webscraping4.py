# Access Democracy 2020
# Get bill data from bills-legislation pages

import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent

from urllib.parse import urljoin

#import sqlite3
import time

import statics_webscraping
import statics

#

def runWebScraping4():
	
	result = []
	
	print("Initialising runWebScraping4()")
	
	startTime = time.time()
	
	ua = UserAgent()
	header = {
	"User-Agent": ua.random
	}
	
	base_url = "https://www.aph.gov.au"
	
	#Bills before Parliament
	#https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_before_Parliament?page=1&drt=2&drv=7&drvH=7&pnu=46&pnuH=46&f=02%2f07%2f2019&to=17%2f09%2f2020&ps=100&ito=1&q=&bs=1&pbh=1&bhor=1&pmb=1&g=1&st=2
	#https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_before_Parliament?page=2&drt=2&drv=7&drvH=7&pnu=46&pnuH=46&f=02%2f07%2f2019&to=17%2f09%2f2020&ps=100&ito=1&q=&bs=1&pbh=1&bhor=1&pmb=1&g=1&st=2

	#Bills assented to
	#https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Assented_Bills_of_the_current_Parliament?page=1&drt=2&drv=7&drvH=7&pnu=46&pnuH=46&f=02%2f07%2f2019&to=17%2f09%2f2020&ps=100&ito=1&q=&bs=1&pbh=1&bhor=1&pmb=1&g=1&st=2
	#https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Assented_Bills_of_the_current_Parliament?page=2&drt=2&drv=7&drvH=7&pnu=46&pnuH=46&f=02%2f07%2f2019&to=17%2f09%2f2020&ps=100&ito=1&q=&bs=1&pbh=1&bhor=1&pmb=1&g=1&st=2

	#Bills not proceeding
	#https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_not_passed_current_Parliament?page=1&drt=2&drv=7&drvH=7&pnu=46&pnuH=46&f=02%2f07%2f2019&to=17%2f09%2f2020&ps=100&ito=1&q=&bs=1&pbh=1&bhor=1&pmb=1&g=1&st=2
	#https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_not_passed_current_Parliament?page=2&drt=2&drv=7&drvH=7&pnu=46&pnuH=46&f=02%2f07%2f2019&to=17%2f09%2f2020&ps=100&ito=1&q=&bs=1&pbh=1&bhor=1&pmb=1&g=1&st=2
	
	urls = []
	
	urls += ["https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_before_Parliament?page=1&drt=2&drv=7&drvH=7&pnu=46&pnuH=46&f=02%2f07%2f2019&to=17%2f09%2f2020&ps=100&ito=1&q=&bs=1&pbh=1&bhor=1&pmb=1&g=1&st=2"]
	urls += ["https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_before_Parliament?page=2&drt=2&drv=7&drvH=7&pnu=46&pnuH=46&f=02%2f07%2f2019&to=17%2f09%2f2020&ps=100&ito=1&q=&bs=1&pbh=1&bhor=1&pmb=1&g=1&st=2"]
	
	urls += ["https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Assented_Bills_of_the_current_Parliament?page=1&drt=2&drv=7&drvH=7&pnu=46&pnuH=46&f=02%2f07%2f2019&to=17%2f09%2f2020&ps=100&ito=1&q=&bs=1&pbh=1&bhor=1&pmb=1&g=1&st=2"]
	urls += ["https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Assented_Bills_of_the_current_Parliament?page=2&drt=2&drv=7&drvH=7&pnu=46&pnuH=46&f=02%2f07%2f2019&to=17%2f09%2f2020&ps=100&ito=1&q=&bs=1&pbh=1&bhor=1&pmb=1&g=1&st=2"]
	
	urls += ["https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_not_passed_current_Parliament?page=1&drt=2&drv=7&drvH=7&pnu=46&pnuH=46&f=02%2f07%2f2019&to=17%2f09%2f2020&ps=100&ito=1&q=&bs=1&pbh=1&bhor=1&pmb=1&g=1&st=2"]
	urls += ["https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_not_passed_current_Parliament?page=2&drt=2&drv=7&drvH=7&pnu=46&pnuH=46&f=02%2f07%2f2019&to=17%2f09%2f2020&ps=100&ito=1&q=&bs=1&pbh=1&bhor=1&pmb=1&g=1&st=2"]
	
	billPageCount = 0
	
	#
	#
	
	# Bill progress elements
	
	# House of Representatives
	# 
	# Introduced and read a first time
	# Second reading moved
	# Second reading debate *n...
	# Second reading agreed to
	# Third reading moved
	# Third reading debated
	# Third reading agreed to
	# Consideration in detail debate
	# Reported from Federation Chamber
	
	# Senate
	# 
	# Introduced and read a first time
	# Second reading moved
	# Second reading debate *n...
	# Lapsed at end of Parliament
	# Restored to Notice Paper
	# Committee of the Whole debate
	# Third reading agreed to
	
	# Unsure
	# 
	# Lapsed at dissolution
	# Lapsed at prorogation
	# Referred to Federation Chamber
	
	# When passed both houses
	# 
	# Finally passed both Houses
	# Assent
	# - Act no: xx
	# - Year: xxxx
	
	#
	#
	
	temp_notInBillProgressElements_all = []
	
	billProgressElements_all = [
	"Introduced and read a first time",
	"Second reading moved",
	"Second reading debate",
	"Second reading agreed to",
	"Third reading moved",
	"Third reading debated",
	"Third reading agreed to",
	"Consideration in detail debate",
	"Reported from Federation Chamber",
	"Lapsed at end of Parliament",
	"Restored to Notice Paper",
	"Committee of the Whole debate",
	"Referred to Federation Chamber", 
	"Lapsed at prorogation", 
	"Lapsed at dissolution",
	"Bill agreed to, subject to requests"
	"Consideration of Senate message",
	]
	
	billProgressElements_reps = [
	"Introduced and read a first time",
	"Second reading moved",
	"Second reading debate",
	"Second reading agreed to",
	"Consideration in detail debate",
	"Third reading moved",
	"Third reading debated",
	"Third reading agreed to"
	"Consideration of Senate message",
	]
	
	billProgressElements_sen = [
	"Introduced and read a first time",
	"Second reading moved",
	"Second reading debate",
	"Second reading agreed to",
	"Committee of the Whole debate",
	"Third reading moved",
	"Third reading debated",
	"Third reading agreed to",
	"Bill agreed to, subject to requests"
	]
	
	#
	#
	
	for url in urls:
	#
		print("")
		print("url: ", url)
		print("")
	
		page = requests.get(url, headers=header, verify=False)
		soup = BeautifulSoup(page.content, 'html.parser')
		
		#for a in soup.tbody.find_all('a', href=True, string=re.compile('Result')):
		#for a in soup.tbody.find_all('a', href=True):
		#for a in soup.find_all('a', href=re.compile("Result")):
		for a in soup.find_all('a', href=re.compile("bId=")):
		#
			print("")
			print("--------------------------------------------------------------------------------------------------------------------------------------------")
			print("")
			
			billPageCount += 1
			print("billPageCount: ", billPageCount)
			print("")
			
			if 'http' not in a['href']: # Likely a relative URL
				a['href'] = base_url + a['href']
			
			pageURL = a['href']
			
			print("")
			print("Found the URL:", pageURL)
			#print("soup.title: ", soup.title)
			print("")
			
			#
			
			page2 = requests.get(a['href'])
			soup2 = BeautifulSoup(page2.content, 'html.parser')
			
			#
			#
			
			heading = ""
			type = ""
			sponsors = ""
			portfolio = ""
			originatingHouse = ""
			status = ""
			parliamentNo = ""
			
			summary = ""
			
			#
			#
			
			headings1 = soup2.findAll("h1")
			lastHeading = headings1[len(headings1)-1]
			heading = lastHeading.text
			
			#
			
			dts = soup2.findAll("dt")
			
			for dt in dts:
			#
				if dt.text.lower() == "type":
					type = dt.find_next("dd").text.strip()
				elif dt.text.lower() == "sponsor(s)":
					sponsors = dt.find_next("dd").text.strip()
				elif dt.text.lower() == "portfolio":
					portfolio = dt.find_next("dd").text.strip()
				elif dt.text.lower() == "originating house":
					originatingHouse = dt.find_next("dd").text.strip()
				elif dt.text.lower() == "status":
					status = dt.find_next("dd").text.strip()
				elif dt.text.lower() == "parliament no":
					parliamentNo = dt.find_next("dd").text.strip()
			#
			
			summarySections = soup2.findAll("div", {"id": "main_0_summaryPanel"})
			if len(summarySections) > 0:
				summarySection_p = summarySections[0].find_next("p")
				summary = summarySection_p.text.strip()
			
			#
			
			print("")
			print("heading: ", heading)
			print("type: ", type)
			print("sponsors: ", sponsors)
			print("portfolio: ", portfolio)
			print("originatingHouse: ", originatingHouse)
			print("status: ", status)
			print("parliamentNo: ", parliamentNo)
			print("")
			print("summary: ", summary)
			print("")
			
			#
			#
			
			mainDivSections = soup2.findAll("div", {"id": "main_0_mainDiv"})
			if len(mainDivSections) > 0:
			#
				mainDivSection = mainDivSections[0]
				
				#
				
				reps_elements = []
				sen_elements = []
				
				bHasPassedHouseOfReps_orNoNeed = False # May have started in the senate?
				bHasPassedSenate = False
				
				bHasPassedBoth = False
				bHasAssent = False
				
				#
				
				#tables = mainDivSection.findAll("table", {"class": "fullwidth"})
				tables = mainDivSection.findAll("table")
				for table in tables:
				#
					tableHeaderName = ""
					
					theads = table.findAll("thead")
					if len(theads) > 0:
					#
						ths = theads[0].findAll("th")
						tableHeaderName = ths[0].text
					#
					
					print("tableHeaderName: ", tableHeaderName)
					
					tbodys = table.findAll("tbody")
					if len(tbodys) > 0:
					#
						trs = tbodys[0].findAll("tr")
						for tr in trs:
						#
							tds = tr.findAll("td")
							if len(tds) == 2:
							#
								span = tds[0].find_next("span")
								
								x_text = span.text.strip()
								x_date = tds[1].text.strip()
								
								#print(x_text)
								#print(x_date)
								
								
								
								
								
								if x_text not in billProgressElements_all:
									temp_notInBillProgressElements_all += [x_text]
								
								if len(temp_notInBillProgressElements_all) > 0:
									print("")
									print("temp_notInBillProgressElements_all: ", temp_notInBillProgressElements_all)
									print("")
								
								
								
								
								if tableHeaderName == "House of Representatives":
									reps_elements += [[x_text, x_date]]
								elif tableHeaderName == "Senate":
									sen_elements += [[x_text, x_date]]
								
								#
								
								if x_text == "Finally passed both Houses":
									bHasPassedBoth = True
									bHasPassedSenate = True
								
								if x_text == "Assent":
									bHasAssent = True
								
							#
						#
					#
					
				# end of: for table in tables:
				
				if len(sen_elements) > 0:
					bHasPassedHouseOfReps_orNoNeed = True
				
				#
				
				print("")
				
				print("len(reps_elements): ", len(reps_elements))
				for repElem in reps_elements:
					print(repElem)
				
				print("len(sen_elements): ", len(sen_elements))
				for senElem in sen_elements:
					print(senElem)
				
				print("bHasPassedHouseOfReps_orNoNeed: ", bHasPassedHouseOfReps_orNoNeed)
				print("bHasPassedSenate: ", bHasPassedSenate)
				
				print("bHasPassedBoth: ", bHasPassedBoth)
				print("bHasAssent: ", bHasAssent)
				
				print("pageURL: ", pageURL)
				
				#
				
				
				
				
				
				
				
			#
			#end of: if len(mainDivSections) > 0:
			
			result += [[heading, type, sponsors, portfolio, originatingHouse, status, parliamentNo, summary, reps_elements, sen_elements, bHasPassedHouseOfReps_orNoNeed, bHasPassedSenate, bHasPassedBoth, bHasAssent, pageURL]]
			
			#break
			
		# 
		# end of: for a in soup.find_all('a', href=re.compile("bId=")):
		
		#break
		
	# 
	# end of: for url in urls:
	
	#
	
	print("billPageCount final: ", billPageCount)
	print("runWebScraping4() COMPLETE IN:", statics.display_time(time.time() - startTime))
	
	#
	
	return result
#

if __name__ == "__main__": # So it doesn't run when we import this script

	wsResult = runWebScraping4()
	
	statics_webscraping.printWS4ResultToFile(wsResult, "webscrapingAllBillsOutput2.txt")
	statics_webscraping.writeWS4ResultToDB(wsResult)

	input('Press ENTER to exit')
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	