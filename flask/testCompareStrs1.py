# Access Democracy 2020

import statics

def testCompareStrs1():
#
	#str1 = "Australian Capital Territory (Self-Government) Amendment (ACT Integrity Commission Powers) Bill 2020"
	#str2 = "AUSTRALIAN CAPITAL TERRITORY (SELF-GOVERNMENT) AMENDMENT (ACT INTEGRITY COMMISSION POWERS) BILL 2020"
	
	str1 = "Australian Broadcasting Corporation Amendment (Rural and Regional Measures) Bill 2019"
	str2 = "17 BROADCASTING SERVICES AMENDMENT (REGIONAL COMMERCIAL RADIO AND OTHER MEASURES) BILL 2020"
	
	str1 = str1.lower().strip()
	str2 = str2.lower().strip()
	
	#testFlt = statics.compareStrs1(str1, str2)
	#testFlt = statics.compareStrs2(str1, str2)
	testFlt = statics.compareStrs3(str1, str2)
	
	print("testFlt: ", testFlt)
#

#
#
#
#

if __name__ == "__main__": # So it doesn't run when we import this script
#
	testCompareStrs1()
	
	input('Press ENTER to exit')
#