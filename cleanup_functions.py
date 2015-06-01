#!/usr/bin/python
from pymarc import MARCReader, Field

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

def remove_all_fields_with_tag(tag, record):
   for field_to_delete in record.get_fields(tag):
      record.remove_field(field_to_delete)


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
