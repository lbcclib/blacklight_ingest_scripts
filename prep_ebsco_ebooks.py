#!/usr/bin/python
from pymarc import MARCReader, Field
import sys, os

if sys.argv[1]:
   file_name = sys.argv[1]
else:
   file_name = '/home/lbccadmin/data/metacoll.OLX.new.D20150302.T240553.2.mrc'

output_file_name = file_name + '.tmp.mrc'

def remove_bad_subjects(record):
   for field600 in record.get_fields('600'):
      if (('6' == field600.indicators[1]) or ('7' == field600.indicators[1])):
         record.remove_field(field600)
   for field610 in record.get_fields('610'):
      if (('6' == field610.indicators[1]) or ('7' == field610.indicators[1])):
         record.remove_field(field610)
   for field611 in record.get_fields('611'):
      if (('6' == field611.indicators[1]) or ('7' == field611.indicators[1])):
         record.remove_field(field611)
   for field650 in record.get_fields('650'):
      if (('4' == field650.indicators[1]) or ('6' == field650.indicators[1]) or ('7' == field650.indicators[1])):
         record.remove_field(field650)
      elif 'Electronic books' in field650['a']:
         record.remove_field(field650)
   for field651 in record.get_fields('651'):
      if (('6' == field651.indicators[1]) or ('7' == field651.indicators[1])):
         record.remove_field(field651)
   for field655 in record.get_fields('655'):
      record.remove_field(field655)

def remove_empty_place_of_publication(record):
   for field260 in record.get_fields('260'):
      if field260['a']:
         if ('not identified' in field260['a']) or ('s.l.' in field260['a']):
            record.remove_field(field260)
   for field264 in record.get_fields('264'):
      if field264['a']:
         if ('not identified' in field264['a']) or ('s.l.' in field264['a']):
            record.remove_field(field264)

def remove_empty_publisher(record):
   for field260 in record.get_fields('260'):
      if field260['b']:
         if ('not identified' in field260['b']):
            record.remove_field(field260)
   for field264 in record.get_fields('264'):
      if field264['b']:
         if ('not identified' in field264['b']):
            record.remove_field(field264)

with open(file_name, 'rb') as fh:
   out = open(output_file_name, 'wb')
   reader = MARCReader(fh, to_unicode=True, force_utf8='true', utf8_handling='replace')
   for record in reader:
      print record['001']

      # General cleanup
      remove_bad_subjects(record)
#      remove_empty_place_of_publication(record)
#      remove_empty_publisher(record)
#      replace_abbreviations(record)

      # add 950
      record.add_field(
         Field(
            tag = '950',
            indicators = ['0', '0'],
            subfields = [
               'a', 'EBSCO ebooks',
               'b', 'Online'
         ]))

      out.write(record.as_marc())
   out.close()
   os.system('java -Xmx512m  -Dsolr.hosturl=http://127.0.0.1:8983/solr  -jar /home/lbccadmin/.gem/ruby/gems/blacklight-marc-5.4.0/lib/SolrMarc.jar /home/lbccadmin/beta/config/SolrMarc/config.properties ' + output_file_name)

