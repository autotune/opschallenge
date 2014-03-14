#!/usr/bin/python
# http://docs.python.org/2/library/index.html
# todo: cleanup vars
# let the fun begin
import pyrax
import sys
import string
import re
import os
import MySQLdb as mdb
import time
import contextlib 
import random
from creds import * 

pyrax.set_credential_file("/root/creds.cfg")
cdb = pyrax.cloud_databases
status = ""

# better than the MGC fail whale
dontPanic = '''
		DON'T PANIC!
                  nnnmmm                    
   \||\       ;;;;%%%@@@@@@       \ //,     
    V|/     %;;%%%%%@@@@@@@@@@  ===Y//      
    68=== ;;;;%%%%%%@@@@@@@@@@@@    @Y      
    ;Y   ;;%;%%%%%%@@@@@@@@@@@@@@    Y      
    ;Y  ;;;+;%%%%%%@@@@@@@@@@@@@@@    Y     
    ;Y__;;;+;%%%%%%@@@@@@@@@@@@@@i;;__Y     
   iiY"";;   "55%@@@@@@@@@@55"   @"";;;>    
          Y     "555555555"     @@          
          `;       555555_    @@            
            `;.  ,====\\=.  .;'             
              ``""""`==\\=='                
                     `;=====              
                        ===                 
'''

        
@contextlib.contextmanager
def suppress_output(stdchannel, dest_filename):
    try:
        oldstdchannel = os.dup(stdchannel.fileno())
        dest_file = open(dest_filename, 'w')
        os.dup2(dest_file.fileno(), stdchannel.fileno())
 
        yield
    finally:
        if oldstdchannel is not None:
            os.dup2(oldstdchannel, stdchannel.fileno())
        if dest_file is not None:
            dest_file.close()

def updateData():
	print "updating..."
	with suppress_output(sys.stderr, os.devnull):
	# create file and send out contents
		os.remove('out.txt')
		file = open('out.txt', 'w')
		print >> file, cdb.list()
		file.close()
	print "done \n"

updateData()

with open ('out.txt','r') as myfile:
        data = myfile.read()
        contents = data.split()

        ## seems python separates array items by spaces
        # search for db name and find index
        state = "status=BUILD"
        # dbIndex = contents.index("name=" + dbName + ",")
        # dbExists = data[dbIndex]
        dbCrnt = dbName

        if re.findall("\\b" +state+ "\\b,", data):
                status = re.findall("\\b" +state+ "\\b,", data)
        myfile.close()

with open ('out.txt','r') as myfile:
        data = myfile.read()
        contents = data.split()
        ## seems python separates array items by spaces
        # search for db name and find index
        dbCheck = "hostname=" + dbHost 
        # dbIndex = contents.index("name=" + dbName + ",")
        # dbExists = data[dbIndex]
        dbCrnt = dbName

        name = (re.findall("\\b" +dbCheck+ "\\b,", data))
        # check if name not in list
        while not len(name):
                print "DB \'" + dbName +  "\' must exist! Care to try another?\n"
                dbName = raw_input("DB Name: ")
                name = (re.findall("\\b" +dbName+ "\\b,", data))
        myfile.close()
# todo: implement more error handeling in previous and future scripts	
con = mdb.connect(dbHost, user, passwd, dbName);
try:
	cur = con.cursor()
	cur.execute("SHOW TABLES")
	ver = cur.fetchone()
	if str(ver) == "None":
		choice = raw_input("DB doesn't have data! Continue backup?: [y/n]")
		while choice != "y" or "n":
			print "Choice must be \"y\" or \"n\""
			choice = raw_input("DB doesn't have data! Continue backup?: [y/n]")
			if choice == "y" :
				break
			elif choice == "n":
				exit()
		
	else:
		print "Tables are as follows: \n\n%s " %ver
except mdb.Error, e:
	
	print "error %d: %s" % (e.args[0],e.args[1])
	print dontPanic
finally:
	if con:
		con.close()

# create backup
backup = cdb.create_backup(dbHost, name="backup1")
print backup
print dontPanic
