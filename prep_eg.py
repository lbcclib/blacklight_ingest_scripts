#!/usr/bin/python

from pymarc import MARCReader
import sys

with open(sys.argv[0], 'rb') as fh:
   out = open('/home/lbccadmin/data/eg_to_index.mrc', 'wb')
   reader = MARCReader(fh)
   for record in reader:
      record.add_field(
         Field(
            tag = '950',
            subfields = [
               'a', 'LBCC library catalog',
               'b', 'At the library'
            ]))
      out.write(record.as_marc())
   out.close()


