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


with open(file_name, 'rb') as fh:
   out = open(output_file_name, 'wb')
   reader = MARCReader(fh, to_unicode=True, force_utf8='true', utf8_handling='replace')
   for record in reader:
      print(record['001'])

      # add 950
      record.add_field(
         Field(
            tag = '950',
            indicators = ['0', '0'],
            subfields = [
               'a', 'Gale Virtual Reference Library',
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
