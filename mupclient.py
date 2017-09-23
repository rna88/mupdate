import sys
import PyQt4.QtCore import *
import PyQt4.QtGUI import *

import ftplib
import ssl
ftps = ftplib.FTP_TLS()

print (ftps.connect('192.168.1.66',47274))
print (ftps.login('user','12345'))
ftps.prot_p()
print (ftps.retrlines('LIST'))


