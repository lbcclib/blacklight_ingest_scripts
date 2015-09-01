SOLR_CONFIG = '/home/lbccadmin/beta/config/SolrMarc/config.properties'
SOLR_HOST = 'http://127.0.0.1:8983/solr'
SOLR_JAR = '/home/lbccadmin/.gem/ruby/gems/blacklight-marc-5.4.0/lib/SolrMarc.jar'

from os import system

def index_file(file_name):
	system( 'C:/jetty/SolrMarc/bin/indexfile.bat ' + file_name)
