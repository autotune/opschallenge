#!/usr/bin/python
# http://docs.python.org/2/library/index.html
# todo: cleanup vars
# let the fun begin
import pyrax
import sys
import string
import re
import os
import MySQLdb
import time
import contextlib 
import random

pyrax.set_credential_file("/root/creds.cfg")
cdb = pyrax.cloud_databases
dbName = raw_input("DB Name: ")
status = ""
dbNum = int(raw_input("Number of DBs: "))

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

# print dontPanic

# inst = cdb.create(dbName, flavor=1, volume=2)
        
# courtesy of marc-abramowitz.com
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
	dbCheck = "name=" + dbName + ","
	# dbIndex = contents.index("name=" + dbName + ",")
	# dbExists = data[dbIndex]
	dbCrnt = dbName
	
	name = (re.findall("\\b" +dbName+ "\\b,", data))
        # check if list is not empty
        
	while len(name):
                print "DB \'" + dbName +  "\' exists! Care to try another?\n"
                dbName = raw_input("DB Name: ")
                name = (re.findall("\\b" +dbName+ "\\b,", data))
	myfile.close()
	
inst = cdb.create(dbName, flavor=1, volume=2)
print inst
updateData()

with open ('out.txt','r') as myfile:
        data = myfile.read()
        contents = data.split()
        ## seems python separates array items by spaces
        # search for db name and find index
        dbCheck = "name=" + dbName + ","
        # dbIndex = contents.index("name=" + dbName + ",")
        # dbExists = data[dbIndex]
        dbCrnt = dbName

# check for status in out.txt array
if "status=BUILD," in contents:
	status = "status=BUILD,"
        while len(status):
                with open ('out.txt','r') as myfile:
                        data = myfile.read()
                        contents = data.split()

                        ## seems python separates array items by spaces
                        # search for db name and find index
                        # dbIndex = contents.index("name=" + dbName + ",")
                        # dbExists = data[dbIndex]
                        print "DB is building! Care to grab some tea?\n"
                        time.sleep(5)
                        # check if true, otherwise output sent regardless
                        if re.findall("\\b" +state+ "\\b,", data):
                                status = re.findall("\\b" +state+ "\\b,", data)
                        else:
                                print "Done!"
                                break
                        updateData()
else:
        print "Unknown build condition present!"
	print dontPanic

# os.system('cls' if os.name == 'nt' else 'clear')


updateData()

# return URL of created database
with open ('out.txt','r') as myfile:
        data = myfile.read()
	contents = data.split()
	## seems python separates array items by spaces
	# search for db name and find index
	dbIndex = contents.index("name=" + dbCrnt + ",")
	dbName = contents[dbIndex]
	print dbName
	# URL is two items behind db name
	hostname=contents[dbIndex-3]
	print hostname
	myfile.close

# create x number of databases and x number of users
for i in range(0, dbNum):
	i = str(i)
	db = inst.create_database("testdb" + i)
	password = ''
	password += chr(random.randint(33,126))
	
	print "user" + i + 'password: '

	user = inst.create_user(name="user" + i, password=password + i, database_names=[db], host="%")
	print "DB:", db

print "\nSomething went terribly right!\n"
print dontPanic
 
exit()


