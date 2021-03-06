#!/usr/bin/python

from pymarc import MARCReader
from bibtex_functions import BibEntry
import sys

if sys.argv[1]:
   file_name = sys.argv[1]
else:
   file_name = '/home/lbccadmin/data/eg_to_index.mrc'

with open(sys.argv[0], 'rb') as fh:
   out = open(file_name, 'wb')
   reader = MARCReader(fh)
   for record in reader:
      record.add_field(
         Field(
            tag = '950',
            subfields = [
               'a', 'LBCC library catalog',
               'b', 'At the library'
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


