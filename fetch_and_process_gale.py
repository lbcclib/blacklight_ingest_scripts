#!/usr/bin/python
from pymarc import MARCReader, Field
import os, re, urllib
from indexing_functions import index_file
import windows_paths as paths #linux_paths or windows_paths

def remove_bad_subjects(record):
   for field650 in record.get_fields('650'):
      if (('4' == field650.indicators[1]) or ('6' == field650.indicators[1]) or ('7' == field650.indicators[1])):
         record.remove_field(field650)


def index_files(db_short_name, db_long_name):
   file_name = paths.new + db_short_name + '.mrc'
   urllib.urlretrieve('http://access.gale.com/api/dropoff/resources/' + db_short_name + '.mrc', file_name)
   output_file_name = file_name + '.tmp.mrc'

   with open(file_name, 'rb') as fh:
      out = open(output_file_name, 'wb')
      reader = MARCReader(fh, to_unicode=True, force_utf8='true', utf8_handling='replace')
      for record in reader:
         print(record['001'])

         remove_bad_subjects(record)

         # add 950
         record.add_field(
            Field(
               tag = '950',
               indicators = ['0', '0'],
               subfields = [
                  'a', db_long_name,
                  'b', 'Online'
            ]))


         #fix 856
         for field856 in record.get_fields('856'):
            field856['u'] = re.sub('ic.galegroup.com.ic.ovic.topic.actionWin.', 'infotrac.galegroup.com/itweb/oregongeo?', re.sub(r'userGroupName\=\[LOCATIONID\]', 'id=geo', field856['u']))

         out.write(record.as_marc())
      out.close()
      index_file(output_file_name)

index_files('ovic', 'Opposing Viewpoints in Context')
index_files('uhic', 'U.S. History In Context')
index_files('ngma', 'National Geographic Virtual Library')
