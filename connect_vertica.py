# accepts three command line args
#
#   arg 1: file name
#
#   arg 2: development | production
#
#   arg 3: update| purge | append
#
#   -default behavior will clear each users permission rows
#     before running
#   -purge will truncate the permission table before running
#   -append will not delete any rows at all


import pyodbc
import io
import re
import time
import sys

 
class Db:   
            
    def connect(self,environment="development"):
         # set environment
        if (environment == "development"):
            self.host = 'dev.bigdata01.syncapse.com'
            self.user = 'dbadmin'
            self.pw = '********'
            self.dbname = 'syncapse'
            self.dsn = '********'
        elif (environment == "production"):
            self.host = 'bigdata01.syncapse.com'
            self.user = 'BigDataReadOnly'
            self.pw = 'EBub7ue12X1n'
            self.dbname = 'syncapse'
            self.dsn = 'verticaProdReadonly'
        constr = "DSN="+self.dsn+";UID="+self.user+";PWD="+self.pw+";"
        try:
            self.conn = pyodbc.connect(constr)
        except Exception as ex:
            message = ex.args[1]
            print 'Error in connecting - ' + message
	

    ## execute a query
     #
     # @param (string) sql to execute
     # @return a cursor object
    def exec_query(self,sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor

    def select_query(self,sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def commit(self):
        self.conn.commit()
    
# **********************************************************
#   Set up some globals

#determine environment
environment = "development"
if (len(sys.argv) > 1):
    file = sys.argv[1]
else:
    print "Must specify a file"
    exit()
    
if (len(sys.argv) > 2):
    if (sys.argv[2] == "development"):
        environment = "development"
        print "running in development"
    elif (sys.argv[2] == "production"):
        environment = "production"
        print "running in production"
    else:
        print "Argument 2 must be environment"
        exit()
else :
    print "No environment given, assuming development"
    environment = "development"
        
# determine mode. one of update | force
mode = "update"
if (len(sys.argv) > 3):
    mode = sys.argv[3]
    print "running in "+ mode + " mode"

db = Db()
db.connect(environment)
#db.exec_query('select * from tablex')


