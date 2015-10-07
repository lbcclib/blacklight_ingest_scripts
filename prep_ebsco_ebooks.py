#!/usr/bin/python
from pymarc import MARCReader, Field
from bibtex_functions import BibEntry
import sys, os
from indexing_functions import index_file

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

with open(file_name, 'rb') as fh:
   out = open(output_file_name, 'wb')
   reader = MARCReader(fh, to_unicode=True, force_utf8='true', utf8_handling='replace')
   for record in reader:
      print(record['001'])

      # General cleanup
      remove_bad_subjects(record)
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
      
      bibliography = BibEntry()
      bibliography.apply_marc_values(record)
      
      record.add_field(
         Field(
            tag = '951',
            indicators = [' ', ' '],
            subfields = [
               'a', bibliography.as_bibtex()
            ]))

      out.write(record.as_marc())
   out.close()
   index_file(output_file_name)
