import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import ftplib
import ssl
ftps = ftplib.FTP_TLS()

#print (ftps.connect('192.168.1.66',47274))
#print (ftps.connect('151.25.42.11',47274))
print (ftps.connect('0.0.0.0',47274))
print (ftps.login('user','12345'))
ftps.prot_p()
print (ftps.retrlines('LIST'))


