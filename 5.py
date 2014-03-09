#!/usr/bin/python
# http://docs.python.org/2/library/index.html

# let the fun begin
import pyrax
import sys
import string
import re
import os

pyrax.set_credential_file("/root/creds.cfg")
cdb = pyrax.cloud_databases
dbName = raw_input("DB Name: ")

def updateData():

# create file and send out contents
	os.remove('out.txt')
	file = open('out.txt', 'w')
	print >> file, cdb.list()
	file.close()

updateData()

# search for existing database
with open ('out.txt','r') as myfile:
	data = myfile.read()
        contents = data.split()
        ## seems python separates array items by spaces
        # search for db name and find index
	dbCheck = "name=" + dbName + ","
	# dbIndex = contents.index("name=" + dbName + ",")
	# dbExists = data[dbIndex]
	dbCrnt = dbName
	# check the json file for an instance of the dbname
	if dbName in data:
		if dbName == dbCrnt:
			while dbName == dbCrnt:
                		print "Database name equal, how about " + dbName + "herpn?"
                		dbCrnt = raw_input("DB Name: ") 
	# need to find a way to get this in nested loop
	if dbName != dbCrnt:
        	print dbCrnt + "sounds good!"
	myfile.close()

cdb.create(dbCrnt, flavor=1, volume=2)
updateData()

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')

# return URL of created database
with open ('out.txt','r') as myfile:
        data = myfile.read()
	contents = data.split()
	## seems python separates array items by spaces
	# search for db name and find index
	dbIndex = contents.index("name=" + dbCrnt + ",")
	print dbIndex
	# URL is two items behind db name
	hostname=contents[dbIndex-3]
	print hostname

exit()


