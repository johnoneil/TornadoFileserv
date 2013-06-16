#!/usr/bin/python
# vim: set ts=2 expandtab:

#MediaDatabaseUpdate.py
#John O'Neil
#Monday, February 18th, 2013
#
#Script (meant to be invoked by cron job) that recursively checks a single
#target directory for media files of various types.
#Upon finding a new file of interest, it checks if this media has already been
#logged. If not, it will log the following data on the new media:
#1. full filename (with extension)
#1.b file extension
#2. Current absolute path
#3. filesize in bytes
#4. (for video) Create video 3x3 snapshots
#5. (for video) Create a thumbnail of the above 3x3
#6. File creation timestamp
#7. Database entry creation timestamp
#8. (zero) number of times downloaded
#9. (list of all IPv4 addresses that have downloaded the file)
#10. timestamps for all downloads
#
# The above suggests it ought to be split into 3 or 4 tables
# 1. Video File information (filenames, paths, thumbnails etc.)
# 2. Audio file information
# 3. <TODO:>Image file information (to be done later?)
# 2. <TODO:>Download information (date and IP of downloads, and index of file downloaded)

import os
import sys
import MySQLdb as sql
import re #for escaping filename strings

if(len(sys.argv) < 2):
  print "USAGE: MediaDatabaseUpdate <root directory to search in for media>"
  sys.exit(1)
rootdir = sys.argv[1]

#Data driving the script
#MediaDatabase user only has local access to restricted tables.
databaseName = 'MediaDatabase'
databaseUser = 'MediaDatabase'
databasePW = ''

#A generic file structure
class File:
  def __init__(self, name, created, path, extension, size):
    self.name =  sql.escape_string(name)
    self.created = created
    self.absolutePath = sql.escape_string(path)
    self.extension = extension
    self.size = size

class VideoDatabase:
  def __init__(self,database):
    self._Extensions = [".mp4",".mkv",".mov",".avi"]
    self._TableName = 'VideoFiles'
    self.CreateTableIfNoneExists(database)

  def GetFileExtension(self,fienameWithExtension):
    fileName, fileExtension = os.path.splitext(fienameWithExtension)
    return fileName, fileExtension

  def IsFileOfInterest(self,filenameWithExtension):
    fileName, fileExtension = self.GetFileExtension(filenameWithExtension)
    print" filename: " + fileName + " ext: " + fileExtension
    if fileExtension.lower() in self._Extensions:
      print "This is a file of interest."
      return True
    else:
      print "This is not a file of interest."
      return False

  def IsFileLogged(self, database, file):
    #check the sql database to see if this file is already present in our database
    #we use a combination of filename and filesize in bytes to uniquely ID each file
    cursor = database.cursor()
    if(cursor is not None):
      query = 'SELECT * FROM VideoFiles WHERE filename = \'{0}\' and size = \'{1}\''.format(file.name,file.size)
      print query
      rows = cursor.execute(query)
      result = cursor.fetchall()
      cursor.close()
      return rows > 0
    return False
  def CreateTableIfNoneExists(self, database):
    cursor = database.cursor()
    if cursor is not None:
      cursor.execute( 'CREATE TABLE IF NOT EXISTS VideoFiles \
      (\
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        timestamp TIMESTAMP DEFAULT NOW(),\
        filename VARCHAR(255),\
        created TIMESTAMP,\
        absolutepath VARCHAR(4096),\
        extension VARCHAR(255),\
        size INT,\
        snapshot VARCHAR(4096),\
        thumbnail VARCHAR(4096)\
        );')
      result = cursor.fetchall()
      cursor.close() 
    
  def LogFile(self, database, file):
    cursor = database.cursor()
    if( cursor is not None and not self.IsFileLogged(database,file) ):
      sqlcommand = 'INSERT INTO VideoFiles(filename, created, absolutepath, extension, size)\
        VALUES (\'{0}\', \'{1}\',\'{2}\',\'{3}\',\'{4}\');'.format(file.name, file.created,\
        file.absolutePath, file.extension, file.size)
      print sqlcommand
      cursor.execute( sqlcommand )
      result = cursor.fetchall()
      cursor.close()
      

database = None

try:

  database = sql.connect('127.0.0.1', databaseUser, 
    databasePW, databaseName,use_unicode=1,charset="utf8")
    
  #database.query("SELECT VERSION()")
  #result = database.use_result()

  #print "MySQL version: %s" % result.fetch_row()[0]

  #recursively walk the directory tree to identify files of interest.
  videoDatabase = VideoDatabase(database)
  print "about to list directories at " + rootdir
  for (path, dirs, files) in os.walk(rootdir.encode('utf-8')):
      print path
      #for dir in dirs:
      #  print dir
      for file in files:
        try:
          size = os.path.getsize(path +'/'+ file)
          created = os.path.getmtime(path +'/'+ file)
          fileName, fileExtension = videoDatabase.GetFileExtension(file)
          newfile = File( name=file, created=created,path=path, extension=fileExtension ,size=size)
          if( videoDatabase.IsFileOfInterest(file) ):
            print file
            videoDatabase.LogFile(database,newfile)
        except os.error, e:
          print "Error %d: %s"  % (e.args[0], e.args[1])
      print "----"  
    
except sql.Error, e:
  print "Error %d: %s" % (e.args[0], e.args[1])
  sys.exit(1)

finally:
  if database:
    database.close()
  
