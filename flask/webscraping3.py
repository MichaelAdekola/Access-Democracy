# Access Democracy 2020
# Get MP data

import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent

import time

import statics_webscraping
import statics

#

def runWebScraping3():
#
	result = []
	
	startTime = time.time()
	
	#
	
	ua = UserAgent()
	header = {
	"User-Agent": ua.random
	}
	
	siteURL = "https://www.aph.gov.au"
	
	urls = []
	urls += [siteURL + "/Senators_and_Members/Parliamentarian_Search_Results?page=1&q=&mem=1&par=-1&gen=0&ps=96&st=1"]
	urls += [siteURL + "/Senators_and_Members/Parliamentarian_Search_Results?page=2&q=&mem=1&par=-1&gen=0&ps=96&st=1"]
	
	for url in urls:
	#
		page = requests.get(url, headers=header, verify=False)
		soup = BeautifulSoup(page.content, 'html.parser')
		
		#for a in soup.select('h4', {"class": "title"}):
		#
			#print(a.text)
		#
		
		sections = soup.findAll("div", {"class": "row border-bottom padding-top"})
		
		for section in sections:
		#
			title = section.find_next('h4', {"class": "title"})
			name = title.text.strip()
			#print(name)
			
			thumb = section.find_next("p", {"class": "result__thumbnail_parl"})
			src = siteURL + thumb.img['src']
			#print(src.strip())
			
			detailsSection = section.find_next("dl")
			
			#sibA = detailsSection.nextSibling
			#print(detailsSection.name)
			
			dts = []
			
			# dt = section.find_next("dt")
			# while dt != None:
			# #
				# print(dt.text)
				# dt = dt.find_next("dt")
			# #
			
			dat_district = ""
			dat_state = ""
			dat_positions = []
			dat_party = ""
			dat_connect_fb = ""
			dat_connect_tw = ""
			dat_connect_em = ""
			
			phase = "null"
			
			next = detailsSection
			while next is not None and next.name != 'div':
			#
				next = next.find_next()
				
				#print(next.name) # Tag type
				
				if next.name == "dt" and next.text == "For":
					phase = "for"
					continue
				
				if next.name == "dt" and next.text == "Positions":
					phase = "positions"
					continue
				
				if next.name == "dt" and next.text == "Party":
					phase = "party"
					continue
				
				if next.name == "dt" and next.text == "Connect":
					phase = "connect"
					continue
				
				if next.name == "dd":
				#
					if phase == "for":
					#
						spl = next.text.split(",")
						dat_district = spl[0].strip();
						dat_state = spl[1].strip();
					#
					
					if phase == "positions":
					#
						dat_positions += [next.text]
					#
					
					if phase == "party":
						dat_party = next.text
					
				#
				
				if phase == "connect":
				#
					if next.name == "a":
					#						
						if "twitter" in next.attrs['class']:
							dat_connect_tw = next.attrs['href'].strip()
						
						if "facebook" in next.attrs['class']:
							dat_connect_fb = next.attrs['href'].strip()
						
						if "mail" in next.attrs['class']:
							dat_connect_em = next.attrs['href'].strip()
							dat_connect_em = statics.remove_prefix(dat_connect_em, "mailto:")
						
					#
				#
			#
			
			# if dat_district != "":
				# print("dat_district: ", dat_district)
				
			# if dat_state != "":
				# print("dat_state: ", dat_state)
				
			# if len(dat_positions) > 0:
				# print("dat_positions: ", dat_positions)
				
			# if dat_party != "":
				# print("dat_party: ", dat_party)
			
			# if dat_connect_tw != "":
				# print("dat_connect_tw: ", dat_connect_tw)
			
			# if dat_connect_fb != "":
				# print("dat_connect_fb: ", dat_connect_fb)
			
			# if dat_connect_em != "":
				# print("dat_connect_em: ", dat_connect_em)
			
			# print("")
			
			#
			
			result += [[name, src, dat_district, dat_state, dat_positions, dat_party, dat_connect_tw, dat_connect_fb, dat_connect_em]]
			
			#if len(dat_positions) > 1:
			#	break; # TEST
			
			#
			
			#print(result)
			#print("")
			#print("")
		#
	#
	
	statics_webscraping.writeWS3ResultToDB(result)
	
	#
	
	print("runWebScraping3() COMPLETE IN:", statics.display_time(time.time() - startTime))
	
	return result
#

#
#
#
#

if __name__ == "__main__": # So it doesn't run when we import this script
#
	runWebScraping3()
	input('Press ENTER to exit')
#