#!/bin/python

from ftplib import FTP
import os, time
import oclc_credentials
from datetime import strptime, date, timedelta

ftp = FTP(oclc_credentials.server)
ftp.login(oclc_credentials.username, oclc_credentials.password)

#New files
ftp.cwd('metacoll/out/ongoing/new')
files = []
ftp.dir(files.append)
for line in files:
   col_list = line.split()
   date_str = ' '.join(line.split()[5:8])
   file_date = datetime.strptime(date_str, '%b %d %H:%M').date().replace(date.today().year)
   if ((date.today() - from_ftp.date()) < timedelta(weeks=1)):
      filename = col_list[8]
      ftp.retrbinary('RETR %s' % filename, open('/home/lbccadmin/data/new/%s' % filename, 'a+').write)
      os.system('python ~/scripts/prep_oclc.py ~/data/new/' + filename)


#Update files
ftp.cwd('../updates')
files = []
ftp.dir(data.append)
for line in files:
   col_list = line.split()
   date_str = ' '.join(line.split()[5:8])
   file_date = datetime.strptime(date_str, '%b %d %H:%M').date().replace(date.today().year)
   if ((date.today() - from_ftp.date()) < timedelta(weeks=1)):
      filename = col_list[8]
      ftp.retrbinary('RETR %s' % filename, open('/home/lbccadmin/update/%s' % filename, 'a+').write)
      os.system('python ~/scripts/prep_oclc.py ~/data/update/' + filename)

#Delete files
ftp.cwd('../deletes')
files = []
ftp.dir(data.append)
for line in files:
   col_list = line.split()
   date_str = ' '.join(line.split()[5:8])
   file_date = datetime.strptime(date_str, '%b %d %H:%M').date().replace(date.today().year)
   if ((date.today() - from_ftp.date()) < timedelta(weeks=1)):
      filename = col_list[8]
      ftp.retrbinary('RETR %s' % filename, open('/home/lbccadmin/delete/%s' % filename, 'a+').write)
      os.system('python ~/scripts/delete_oclc.py ~/data/delete/' + filename)
