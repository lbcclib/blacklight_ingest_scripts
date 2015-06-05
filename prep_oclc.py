#!/usr/bin/python
from cleanup_functions import add_fake_marc_formats, add_broadly_defined_corp_bodies, remove_all_fields_with_tag, remove_all_fields_with_tags, remove_bad_subjects, remove_empty_place_of_publication, remove_empty_publisher, remove_field_with_substring, remove_field_with_indicator
from indexing_functions import index_file
from bibtex_functions import BibEntry
from pymarc import MARCReader, Field
import sys, os

if sys.argv[1]:
   file_name = sys.argv[1]
else:
   file_name = '/home/lbccadmin/data/metacoll.OLX.new.D20150302.T240553.2.mrc'

output_file_name = file_name + '.tmp.mrc'

with open(file_name, 'rb') as fh:
   out = open(output_file_name, 'wb')
   reader = MARCReader(fh)
   for record in reader:
      print record['001']

      fields_to_delete = []

      # General cleanup
      #add_fake_marc_formats(record)
      add_broadly_defined_corp_bodies(record)
      remove_empty_place_of_publication(record)
      remove_empty_publisher(record)
      #replace_abbreviations(record)

      # Find source, add to record
      source = ''
      if record.get_fields('950'):
         for f in record.get_fields('950'):
            source = f['a']


      #Vendor-specific cleanup
      if 'American History in Video' == source:
         record.leader = record.leader[:6] + 'gz' + record.leader[8:]
         remove_bad_subjects(record)
         fields_to_delete.append('655')

      elif 'American Song' == source:
         record.leader = record.leader[:6] + 'jz' + record.leader[8:]
         remove_bad_subjects(record)
         fields_to_delete.extend(['007', '490', '655'])
         remove_field_with_substring('500', 'a', 'Compact dis', record)

      elif 'Credo Academic Core' == source:
         record.leader = record.leader[:6] + 'az' + record.leader[8:]
         remove_bad_subjects(record)
         fields_to_delete.append('655')

      elif 'Classical Music Library' == source:
         record.leader = record.leader[:6] + 'jz' + record.leader[8:]
         remove_bad_subjects(record)
         fields_to_delete.extend(['007', '655'])

      elif 'Directory of Open Access Books' == source:
         record.leader = record.leader[:6] + 'az' + record.leader[8:]
         remove_bad_subjects(record)
         fields_to_delete.append('655')

      elif 'ebrary Academic Complete' == source:
         remove_bad_subjects(record)
         if 'm' == record.leader[6]:
            record.leader = record.leader[:6] + 'a' + record.leader[7:]
         if 'a' == record.leader[6]:
            record.leader = record.leader[:7] + 'z' + record.leader[8:]
         remove_field_with_substring('650', 'a', 'Electronic book', record)
         remove_field_with_indicator('650', 1, '4', record)
         fields_to_delete.append('655')

      elif ('Films' in source) and ('Demand' in source):
         record.leader = record.leader[:6] + 'gz' + record.leader[8:]
         remove_bad_subjects(record)
         remove_field_with_substring('650', 'a', 'Streaming video', record)
         for field856 in record.get_fields('856'):
            field856['u'] = field856['u']+'&cid=1639'
         if 'TEDTalks' in record['245']['a'] or 'WPA Film Library' in record['245']['a']:
            if record['245']['b']:
               record['245']['a'] = record['245']['b']
         fields_to_delete.extend(['500', '710'])

      elif 'HathiTrust Public Domain only in US Access' == source:
         remove_bad_subjects(record)
         if 'a' == record.leader[6] and 'i' == record.leader[7]:
            record.leader = record.leader[:6] + 'sz' + record.leader[8:]
         else:
            record.leader = record.leader[:6] + 'az' + record.leader[8:]
         remove_field_with_substring('650', 'a', 'Theses', record)
         remove_field_with_indicator('650', 1, '4', record)
         fields_to_delete.append('655')
            
      elif 'NCBI Bookshelf' == source:
         record.leader = record.leader[:6] + 'az' + record.leader[8:]
         remove_bad_subjects(record)
         fields_to_delete.extend(['007', '655'])

      elif 'Smithsonian Global Sound For Libraries' == source:
         record.leader = record.leader[:6] + 'jz' + record.leader[8:]
         fields_to_delete.append('007')

      elif 'Wright American Fiction' == source:
         record.leader = record.leader[:6] + 'az' + record.leader[8:]
         remove_field_with_indicator('655', 1, '4', record)




      bibliography = BibEntry()
      bibliography.apply_marc_values(record)
      
      record.add_field(
         Field(
            tag = '951',
            indicators = [' ', ' '],
            subfields = [
               'a', bibliography.as_bibtex()
            ]))

      

      remove_all_fields_with_tags(fields_to_delete, record)
      out.write(record.as_marc())
   out.close()
   index_file(output_file_name)
