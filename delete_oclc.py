#!/usr/bin/python
from pymarc import MARCReader, Field
import sys, os, urllib, urllib2
import windows_paths as paths #linux_paths or windows_paths

DELETE_PREFIX = paths.solr_url + 'update?'
DELETE_SUFFIX = '&commit=true'

if sys.argv[1]:
   file_name = sys.argv[1]
else:
   file_name = '~/data/metacoll.OLX.deletes.W20150320.T105854.1.mrc'

def delete_record_by_id(control_number):
   delete_xml = urllib.urlencode({'stream.body': '<delete><id>' + control_number + '</id></delete>'})
   delete_url = DELETE_PREFIX + delete_xml + DELETE_SUFFIX
   if urllib2.urlopen(delete_url):
      print 'Deleted ' + control_number

with open(file_name, 'rb') as fh:
   reader = MARCReader(fh)
   for record in reader:
      delete_record_by_id(str(record['001'].data))
