# Access Democracy 2020

import os
import csv
from math import cos, asin, sqrt, pi
import io
import sqlite3
import base64

from difflib import SequenceMatcher

stateAcronyms = {
	"Victoria": "VIC",
	"New South Wales": "NSW",
	"Queensland": "QLD",
	"Tasmania": "TAS",
	"South Australia": "SA",
	"Western Australia": "WA",
	"Northern Territory": "NT",
	"Australian Capital Territory": "ACT"
}

partyAcronyms = {
	"Liberal Party of Australia": "LP",
	"Liberal National Party of Queensland": "LNP",
	"The Nationals": "NATS",
	"Katter's Australian Party": "KAP",
	"Independent": "IND",
	"Centre Alliance": "CA",
	"Australian Labor Party": "ALP",
	"Australian Greens": "AG"
}

#
# 'Static' functions

def importCSV(filename):
#
	data = []
	
	if not os.path.isfile(filename):
		print("Error: CSV file is missing")
		return data

	with open(filename) as csv_file:
		data = [tuple(line) for line in csv.reader(csv_file, delimiter=',')]
		print("CSV lines read in: " + str(len(data)))
	
	return data
#

#https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
def realWorldDist(lat1, lon1, lat2, lon2): # Might not take earth curvature into consideration
#
	p = pi/180
	a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
	return 12742 * asin(sqrt(a))
#
	
def getLatLngFromStr(str):
#
	spl = str.split(',', 1)
	return [spl[0], spl[1]]
#

def getDistBetweenLatLngs(LL_a, LL_b):
#
	return realWorldDist(float(LL_a[1]), float(LL_a[0]), float(LL_b[1]), float(LL_b[0]))
#

def getDistBetweenLatLngsStrs(LLStr_a, LLStr_b):
#
	a = getLatLngFromStr(LLStr_a)
	b = getLatLngFromStr(LLStr_b)
	return getDistBetweenLatLngs(a, b)
#

def isTimeLaterThan(time, than):
#
	if time > than:
		return False
	
	return True
#
	
def roundToNearestMultiple(multOf, number):
#
	return multOf * round(number/multOf)
#

def getHighestNum(list):
#
	highest = 0
	
	for i in list:
		if i > highest:
			highest = i
		
	return highest
#
	
def getLowestNum(list):
#
	lowest = list[0]
	
	for i in list:
		if i < lowest:
			lowest = i
		
	return lowest
#

def getTimesInList(item, list):
#
	result = 0
	
	for element in list:
		if item == element:
			result += 1
	
	return result
#

def getIndicesMatchingItemInList(item, list):
#
	result = []
		
	i = 0
	for element in list:
		if item == element:
			result += [i]
		i += 1
	
	return result
#

def getItemIdxList(item, list):
#	
	i = 0
	for element in list:
		if item == element:
			return i
		i += 1
	
	return -1
#

def checkTwoItemsSameIdxInTwoLists(item1, item2, list1, list2):
#
	if len(list1) != len(list2):
		return (False, -2)
		
	i = 0
	while i < len(list1):
		if item1 == list1[i]:
			if item2 == list2[i]:
				return (True, i)
			
		i += 1
	#
	
	return (False, -1)
#

def blobToBase64(blob):
#
	return base64.b64encode(blob)
#

#https://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days
def display_time(seconds, granularity=2):
#
	result = []
	
	intervals = (('weeks', 604800), ('days', 86400), ('hours', 3600), ('minutes', 60), ('seconds', 1))

	for name, count in intervals:
		value = seconds // count
		if value:
			seconds -= value * count
			if value == 1:
				name = name.rstrip('s')
			result.append("{} {}".format(value, name))
	return ', '.join(result[:granularity])
#

#https://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string
def remove_prefix(text, prefix):
#
	if text.startswith(prefix):
		return text[len(prefix):]
	return text
#

def listOfStrsToOneStr(list):
#
	result = ""
	i = 0
	while i < len(list):
	#
		result += list[i]
		
		if i < len(list)-1:
			result += ", "
		i += 1
	#
	return result
#

def compareStrs1(str1, str2):
#
	str1 = str1.lower().strip()
	str2 = str2.lower().strip()
	
	spl1 = str1.split()
	spl2 = str2.split()
	
	if len(spl1) < 1 or len(spl2) < 1:
		return 0.0
	
	matchingWordCount = 0
	for a in spl1:
		for b in spl2:
			if a == b:
				matchingWordCount += 1
	
	if matchingWordCount == 0:
		return 0.0
	
	return float(matchingWordCount) / float(len(spl1))
#




def compareStrs2(str1, str2):
#
	str1 = str1.lower().strip()
	str2 = str2.lower().strip()

	return str1 == str2
#


def compareStrs3(str1, str2):
#
	return SequenceMatcher(None, str1, str2).ratio()
#



















