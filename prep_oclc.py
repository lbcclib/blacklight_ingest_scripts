#!/usr/bin/python
from cleanup_functions import add_fake_marc_formats, add_broadly_defined_corp_bodies, remove_all_fields_with_tag, remove_bad_subjects, remove_empty_place_of_publication, remove_empty_publisher
from indexing_functions import index_file
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
            remove_all_fields_with_tag('655', record)

         elif 'American Song' == source:
            record.leader = record.leader[:6] + 'jz' + record.leader[8:]
            remove_bad_subjects(record)
            remove_all_fields_with_tag('007', record)
            remove_all_fields_with_tag('490', record)
            for field500 in record.get_fields('500'):
               if 'Compact dis' in field500:
                  record.remove_field(field500)
            remove_all_fields_with_tag('655', record)

         elif 'Credo Academic Core' == source:
            record.leader = record.leader[:6] + 'az' + record.leader[8:]
            remove_bad_subjects(record)
            remove_all_fields_with_tag('655', record)

         elif 'Classical Music Library' == source:
            record.leader = record.leader[:6] + 'jz' + record.leader[8:]
            remove_bad_subjects(record)
            remove_all_fields_with_tag('007', record)
            remove_all_fields_with_tag('655', record)

         elif 'Directory of Open Access Books' == source:
            record.leader = record.leader[:6] + 'az' + record.leader[8:]
            remove_bad_subjects(record)
            remove_all_fields_with_tag('655', record)

         elif 'ebrary Academic Complete' == source:
            remove_bad_subjects(record)
            if 'm' == record.leader[6]:
               record.leader = record.leader[:6] + 'a' + record.leader[7:]
            if 'a' == record.leader[6]:
               record.leader = record.leader[:7] + 'z' + record.leader[8:]
            for field650 in record.get_fields('650'):
               if 'Electronic book' in field650['a']:
                  record.remove_field(field650)
               elif '4' == field650.indicators[1]:
                  record.remove_field(field650)
            remove_all_fields_with_tag('655', record)

         elif ('Films' in source) and ('Demand' in source):
            record.leader = record.leader[:6] + 'gz' + record.leader[8:]
            remove_bad_subjects(record)
            remove_all_fields_with_tag('500', record)
            for field650 in record.get_fields('650'):
               if 'Streaming video' in field650['a']:
                  record.remove_field(field650)
            remove_all_fields_with_tag('856', record)
            for field856 in record.get_fields('856'):
               field856['u'] = field856['u']+'&cid=1639'
            if 'TEDTalks' in record['245']['a'] or 'WPA Film Library' in record['245']['a']:
               record['245']['a'] = record['245']['b']

         elif 'HathiTrust Public Domain only in US Access' == source:
            remove_bad_subjects(record)
            if 'a' == record.leader[6] and 'i' == record.leader[7]:
               record.leader = record.leader[:6] + 'sz' + record.leader[8:]
            else:
               record.leader = record.leader[:6] + 'az' + record.leader[8:]
            for field650 in record.get_fields('650'):
               if ('4' == field650.indicators[1]):
                  record.remove_field(field650)
               elif 'Theses' in field650["a"]:
                  record.remove_field(field650)
            remove_all_fields_with_tag('655', record)
            
         elif 'NCBI Bookshelf' == source:
            record.leader = record.leader[:6] + 'az' + record.leader[8:]
            remove_bad_subjects(record)
            remove_all_fields_with_tag('655', record)

         elif 'Smithsonian Global Sound For Libraries' == source:
            record.leader = record.leader[:6] + 'jz' + record.leader[8:]
            remove_all_fields_with_tag('007', record)

         elif 'Wright American Fiction' == source:
            record.leader = record.leader[:6] + 'az' + record.leader[8:]
            for field655 in record.get_fields('655'):
               if '4' == field655.indicators[1]:
                  record.remove_field(field655)


         out.write(record.as_marc())
   out.close()
   index_file(output_file_name)
