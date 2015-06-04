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

def remove_all_fields_with_tags(tags, record):
   for tag in tags:
      for field_to_delete in record.get_fields(tag):
         record.remove_field(field_to_delete)

def remove_field_with_substring(tag, subfield, value, record):
   substring_values = []
   if type(value) is not list:
      substring_values.append(value)
   else:
      substring_values = value
   for field in record.get_fields(tag):
      if field[subfield]:
         for string in substring_values:
            if string in field[subfield]:
               record.remove_field(field)

def remove_field_with_indicator(tag, pos, value, record):
   indicator_values = []
   if type(value) is not list:
      indicator_values.append(value)
   else:
      indicator_values = value
   for field in record.get_fields(tag):
      if field.indicators[pos] in indicator_values:
         record.remove_field(field)

def remove_bad_subjects(record):
   subject_fields = ['600', '610', '611', '650', '651']
   bad_indicators = ['6', '7']
   for field in subject_fields:
      remove_field_with_indicator(field, 1, bad_indicators, record)

def remove_empty_place_of_publication(record):
   remove_field_with_substring('260', 'a', ['not identified', 's.l.'], record)
   remove_field_with_substring('264', 'a', ['not identified', 's.l.'], record)

def remove_empty_publisher(record):
   remove_field_with_substring('260', 'b', 'not identified', record)
   remove_field_with_substring('264', 'b', 'not identified', record)
