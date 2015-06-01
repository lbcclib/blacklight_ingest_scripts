SOLR_CONFIG = '/home/lbccadmin/beta/config/SolrMarc/config.properties'
SOLR_HOST = 'http://127.0.0.1:8983/solr'
SOLR_JAR = '/home/lbccadmin/.gem/ruby/gems/blacklight-marc-5.4.0/lib/SolrMarc.jar'

from os import system

def index_file(file_name):
   system( 'java -Xmx512m  -Dsolr.hosturl=' + SOLR_HOST +
   ' -jar ' + SOLR_JAR + 
   ' ' +  SOLR_CONFIG +
   ' ' +  file_name)
