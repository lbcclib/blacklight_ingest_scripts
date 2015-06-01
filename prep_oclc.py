#!/usr/bin/python
from pymarc import MARCReader, Field
import sys, os

if sys.argv[1]:
   file_name = sys.argv[1]
else:
   file_name = '/home/lbccadmin/data/metacoll.OLX.new.D20150302.T240553.2.mrc'

output_file_name = file_name + '.tmp.mrc'

def add_fake_marc_formats(record):
   if 'b' == record.leader[7]: #Serial
      record.leader = record.leader[:6] + 'sz' + record.leader[8:]
   elif 'a' == record.leader[6] or 't' == record.leader[6]: #Ebook
      record.leader = record.leader[:6] + 'az' + record.leader[8:]
   elif 'g' == record.leader[6] or 'i' == record.leader[6] or 'j' == record.leader[6]: #Streaming content
      record.leader = record.leader[:7] + 'z' + record.leader[8:]

def add_broadly_defined_corp_bodies(record):
   group_names = [
      'Aboriginal Australians',
      'activist',
      'African American',
      'Americans',
      'Asian Americans',
      'Asians',
      'Blacks',
      'boys',
      'Canadians',
      'Celts',
      'Children',
      'children',
      'Civil rights workers',
      'Croats',
      'Dalits',
      'Disc jockeys',
      'Ecuadorians',
      'Extremists',
      'Freedmen',
      'girls',
      'Hispanic Americans',
      'Immigrants',
      'Indians',
      'Italians',
      'Jews',
      'Khazars',
      'Mestizos',
      'Minorities',
      'minorities',
      'Mothers',
      'Muslim',
      'offenders',
      'people',
      'Puerto Ricans',
      'Refugees',
      'Slavs',
      'Slaves',
      'Soldiers',
      'students',
      'Syrians',
      'Teenagers',
      'teenagers',
      'Women', 
      'women',
   ]
   for field650 in record.get_fields('650'):
      for group_name in group_names:
         if group_name in field650['a']:
            field650.tag = '610'
            break


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
      if (('6' == field650.indicators[1]) or ('7' == field650.indicators[1])):
         record.remove_field(field650)
   for field651 in record.get_fields('651'):
      if (('6' == field651.indicators[1]) or ('7' == field651.indicators[1])):
         record.remove_field(field651)

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
            for field655 in record.get_fields('655'):
               record.remove_field(field655)

         elif 'American Song' == source:
            record.leader = record.leader[:6] + 'jz' + record.leader[8:]
            remove_bad_subjects(record)
            for field490 in record.get_fields('490'):
               record.remove_field(field490)
            for field500 in record.get_fields('500'):
               if 'Compact dis' in field500:
                  record.remove_field(field500)
            for field655 in record.get_fields('655'):
               record.remove_field(field655)

         elif 'Credo Academic Core' == source:
            record.leader = record.leader[:6] + 'az' + record.leader[8:]
            remove_bad_subjects(record)
            for field655 in record.get_fields('655'):
               record.remove_field(field655)

         elif 'Classical Music Library' == source:
            record.leader = record.leader[:6] + 'jz' + record.leader[8:]
            remove_bad_subjects(record)
            for field655 in record.get_fields('655'):
               record.remove_field(field655)

         elif 'Directory of Open Access Books' == source:
            record.leader = record.leader[:6] + 'az' + record.leader[8:]
            remove_bad_subjects(record)
            for field655 in record.get_fields('655'):
               record.remove_field(field655)

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
            for field655 in record.get_fields('655'):
               record.remove_field(field655)

         elif ('Films' in source) and ('Demand' in source):
            record.leader = record.leader[:6] + 'gz' + record.leader[8:]
            remove_bad_subjects(record)
            for field500 in record.get_fields('500'):
               record.remove_field(field500)
            for field650 in record.get_fields('650'):
               if 'Streaming video' in field650['a']:
                  record.remove_field(field650)
            for field655 in record.get_fields('655'):
               record.remove_field(field655)
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
            for field655 in record.get_fields('655'):
               record.remove_field(field655)
            
         elif 'NCBI Bookshelf' == source:
            record.leader = record.leader[:6] + 'az' + record.leader[8:]
            remove_bad_subjects(record)
            for field655 in record.get_fields('655'):
               record.remove_field(field655)

         elif 'Smithsonian Global Sound For Libraries' == source:
            record.leader = record.leader[:6] + 'jz' + record.leader[8:]

         elif 'Wright American Fiction' == source:
            record.leader = record.leader[:6] + 'az' + record.leader[8:]
            for field655 in record.get_fields('655'):
               if '4' == field655.indicators[1]:
                  record.remove_field(field655)


         out.write(record.as_marc())
   out.close()
   os.system('java -Xmx512m  -Dsolr.hosturl=http://127.0.0.1:8983/solr  -jar /home/lbccadmin/.gem/ruby/gems/blacklight-marc-5.4.0/lib/SolrMarc.jar /home/lbccadmin/beta/config/SolrMarc/config.properties ' + output_file_name)

