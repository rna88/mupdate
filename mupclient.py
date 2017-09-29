import sys
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#import Tkinter
#from Tkinter import *

import ftplib
import ssl
ftps = ftplib.FTP_TLS()

fileType = ".pem"   # File extension to download.
localDir='.'    # Directory to place downloaded files.

#print (ftps.connect('192.168.1.66',47274))
#print (ftps.connect('151.25.42.11',47274))

#print (ftps.connect('0.0.0.0',47274))
#print (ftps.login('user','12345'))
ftps.connect('0.0.0.0',47274)
ftps.login('user','12345')

ftps.prot_p()
#print (ftps.retrlines('LIST'))
#print (ftps.retrlines('RETR ' +  'README.md'))
#ftps.retrlines('LIST')

#print (ftps.nlst())
# get remote file list
# get local file list
# Compare two lists and show files that are not on local.
localFiles= os.listdir(localDir)
print (localFiles)
remoteFiles=ftps.nlst()
print (remoteFiles)

newFiles = set(remoteFiles) - set(localFiles)
print (newFiles)
filteredFiles = []

for f in newFiles:
    if f.endswith(fileType):
    #    print (f)
        filteredFiles.append(f)
        #ftps.retrbinary('RETR %s' % f, open(f, 'wb').write)
print (filteredFiles)


for f in filteredFiles:
    ftps.retrbinary('RETR %s' % f, open(f, 'wb').write)

#filename='README.md'
##print (ftps.retrbinary('RETR %s' % filename, open(filename, 'wb').write))
#ftps.retrbinary('RETR %s' % filename, open(filename, 'wb').write)


