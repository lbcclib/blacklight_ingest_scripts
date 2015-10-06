from pymarc import MARCReader
import re

class BibEntry:
   def __init__(self, type='book'):
      #Required elements
      self.key = 'resource'
      self.type = type
      self.authors = []
      self.publisher = ''
      self.title = ''
      self.year = ''

      #Additional elements
      self.address = ''
      self.series = ''
      self.url = ''

   def apply_marc_values(self, record):
      if record['100']:
         self.authors.append(record['100']['a'])
         for field700 in record.get_fields('700'):
            if field700['a']:
               self.authors.append(field700['a'])
      elif record['110']:
         self.authors.append('{' + record['110']['a'] + '}')
      elif record['111']:
         self.authors.append('{' + record['111']['a'] + '}')

      self.title = record.title().replace(' : ', ':').replace(' /', '')

      for field260 in record.get_fields('260'):
         if field260['b']:
            self.publisher = field260['b'].replace(',', '')
            if field260['a']:
               self.address = field260['a'].replace(' :', '')
            if field260['c']:
               match = re.search(r'([12][0-9]{3})', field260['c'])
               if match:
                   self.year = match.group(0)
         else:
            for field264 in record.get_fields('264'):
               if field264['b']:
                  self.publisher = field264['b'].replace(',', '')
                  if field264['a']:
                     self.address = field264['a'].replace(' :', '')
                  if field264['c']:
                     match = re.search(r'([12][0-9]{3})', field264['c'])
                     if match:
                       self.year = match.group(0)
      for field950 in record.get_fields('950'):
         if field950['b']:
            if 'nline' in field950['b']:
               for field856 in record.get_fields('856'):
                  self.url = field856['u']
         

   def apply_sample_values(self):
      #self.authors.extend(['Mills, M. G. L.', 'Mills, Margie'])
      self.publisher = 'Jacana Media'
      self.title = 'Hyena nights & Kalahari days'
      self.year = '2010'
      self.address = 'Auckland Park, South Africa'
      self.series = ''

   def as_bibtex(self):
      bibtex_entry = []
      bibtex_entry.append('@')
      bibtex_entry.append(self.type)
      bibtex_entry.append('{' + self.key)
      bibtex_entry.append(self.line('author', (' and '.join(self.authors).replace('"', ''))))
      bibtex_entry.append(self.line('publisher', self.publisher.replace('"', '')))
      bibtex_entry.append(self.line('title', self.title.replace('"', '')))
      bibtex_entry.append(self.line('year', self.year.replace('"', '')))
      bibtex_entry.append(self.line('address', self.address.replace('"', '')))
      bibtex_entry.append(self.line('series', self.url.replace('"', '')))
      bibtex_entry.append(self.line('url', self.series.replace('"', '')))
      bibtex_entry.append('}')
      return ''.join(bibtex_entry)

   def line(self, label, value):
      if value is not None and 0 < len(value):
         if 'year' != label:
            value = '"' + value + '"'
         return ', ' + label + ' = ' + value
      else:
         return ''
