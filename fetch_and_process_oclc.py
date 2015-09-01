#!/bin/python

from ftplib import FTP
import os, time
import oclc_credentials
import windows_paths as paths #or linux_paths
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
      ftp.retrbinary('RETR %s' % filename, open(paths.new + filename, 'a+').write)
      os.system('python ' + paths.scripts_dir + 'prep_oclc.py ' + paths.new + filename)


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
      ftp.retrbinary('RETR %s' % filename, open(paths.update + filename, 'a+').write)
      os.system('python ' + paths.scripts_dir + 'prep_oclc.py ' + paths.update + filename)

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
      ftp.retrbinary('RETR %s' % filename, open(paths.delete + filename, 'a+').write)
      os.system('python ' + paths.scripts_dir + 'delete_oclc.py ' + paths.delete + filename)
