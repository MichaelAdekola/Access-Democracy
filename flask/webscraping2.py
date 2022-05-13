# Access Democracy 2020
# Get MP image data (deprecated)

import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent

import time

import statics_webscraping
import statics

#

def runWebScraping2():
	
	result = []
	
	startTime = time.time()
	
	#
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
		
		thumbs = soup.findAll("p", {"class": "result__thumbnail_parl"})
		
		print("len(thumbs): ", len(thumbs))
		
		for a in thumbs:
		#
			#print(a.img['alt'], ":", a.img['src'])
			
			alt = a.img['alt']
			#alt = alt.replace("Photo of ", "")
			
			#altOrig = alt
			altFinal = ""
			
			toIgnore_start = ["photo", "of", "hon", "mr", "mrs", "ms", "dr"]
			toIgnore_end = ["mp", "am", "oam", "qc"]
			
			altSpl = alt.split()
			i = 0
			while i < len(altSpl):
			#
				s = altSpl[i].lower().strip()
				#s = altSpl[i].lower().rstrip()
				
				regex = re.compile('[^a-zA-Z]') 
				s = regex.sub('', s)
				
				if s not in toIgnore_start and s not in toIgnore_end:
				#
					altFinal += s
					if i < len(altSpl)-1:
						altFinal += " "
					#
				#
				i += 1
			#
			
			src = siteURL + a.img['src']
			
			#result += [[altOrig + " : " + altFinal, src]]
			result += [[altFinal, src]]
		#
	#
	
	#
	
	#for r in result:
		#print(r)
	
	#
	
	statics_webscraping.writeMPImageWSResultToDB(result)
	
	#
		
	#print("runWebScraping2() COMPLETE IN:", time.time() - startTime, "sec")
	print("runWebScraping2() COMPLETE IN:", statics.display_time(time.time() - startTime))
	
	return result
#

#
#
#
#

if __name__ == "__main__": # So it doesn't run when we import this script
	runWebScraping2()
	input('Press ENTER to exit')