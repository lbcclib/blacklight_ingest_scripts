#!/bin/python

from ftplib import FTP
import os, time
import oclc_credentials

def get_filename(data):
   file_dict = {}
   for line in data:
      col_list = line.split()
      date_str = ' '.join(line.split()[5:8])
      file_dict[time.strptime(date_str, '%b %d %H:%M')] = col_list[8]
      date_list = list([key for key, value in file_dict.items()])
   return file_dict[max(date_list)]

ftp = FTP(oclc_credentials.server)
ftp.login(oclc_credentials.username, oclc_credentials.password)

#New files
ftp.cwd('metacoll/out/ongoing/new')
data = []
ftp.dir(data.append)
filename = get_filename(data)
ftp.retrbinary('RETR %s' % filename, open('/home/lbccadmin/data/new/%s' % filename, 'a+').write)
os.system('python ~/scripts/prep_oclc.py ~/data/new/' + filename)


#Update files
ftp.cwd('../updates')
data = []
ftp.dir(data.append)
filename = get_filename(data)
ftp.retrbinary('RETR %s' % filename, open('/home/lbccadmin/data/update/%s' % filename, 'a+').write)
os.system('python ~/scripts/prep_oclc.py ~/data/update/' + filename)

#Delete files
ftp.cwd('../deletes')
data = []
ftp.dir(data.append)
filename = get_filename(data)
ftp.retrbinary('RETR %s' % filename, open('/home/lbccadmin/data/delete/%s' % filename, 'a+').write)
os.system('python ~/scripts/delete_oclc.py ~/data/delete/' + filename)

#but this doesn't quite work if multiple files in one session
