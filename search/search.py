import sqlite3
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import sorting
import os.path
import shutil
from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import MultifieldParser
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from geopy.distance import great_circle
from stemming.porter2 import stem
from nltk import PorterStemmer

# CREATING A DATABASE
def populate_database():
	conn=sqlite3.connect('FOCo_db');
	c=conn.cursor();
	# name email phone address category description title
	c.execute('''INSERT INTO posting_posting VALUES (null, 'a', 'a@my.msutexas.edu', '76301',"",'electronics', 'in very good condition','mobiles')''');
	c.execute('''INSERT INTO posting_posting VALUES (null, 'b', 'b@my.msutexas.edu', '76302',"",'electronics','10 years old','tv')''');
	c.execute('''INSERT INTO posting_posting VALUES (null, 'c', 'c@my.msutexas.edu', '76305',"",'electronics','latest latest 1987 classic collection','radio')''');
	c.execute('''INSERT INTO posting_posting VALUES (null, 'd', 'd@my.msutexas.edu', '76306',"",'bottle','plastic bottles 12','recyclable')''');
	c.execute('''INSERT INTO posting_posting VALUES (null, 'e', 'e@my.msutexas.edu', '76308',"",'clothes','blue denim latest style','jeans')''');
	conn.commit()
	conn.close()
	print "Database created"


# CREATING AN INDEX OF DATABASE
def create_index(indexdir,database_name):
	if not os.path.exists(indexdir):
		os.mkdir(indexdir)	
	conn=sqlite3.connect(database_name);
	c=conn.cursor();
	schema = Schema(id=NUMERIC(stored=True),title=TEXT(stored=True),description=TEXT(stored=True),category=TEXT(stored=True),name=STORED, address=STORED,phone=STORED,email=STORED)
	ix = create_in(indexdir, schema)
	writer = ix.writer()
	for row in c.execute('SELECT id,title,description,category,name,address,phone,email FROM posting_posting'):
		d1=" "
		d2=" "
		d3=" "
		x1=row[1].split(" ")
		for words in x1:
			d1=d1 + PorterStemmer().stem(words.lower()) + " "
		x2=row[2].split(" ")
		for words in x2:
			d2=d2 + PorterStemmer().stem(words.lower()) + " "
		x3=row[3].split(" ")
		for words in x3:
			d3=d3 + PorterStemmer().stem(words.lower()) + " "
		writer.add_document(id=row[0],title=d1, description=d2, category=d3, name=(row[4].lower()), address=(row[5].lower()), phone=(row[6].lower()), email=(row[7].lower()))
		# print row
	writer.commit()
	print "index created"


# PARSE A QUERY STRING AND SEARCH RESULTS IN SORTED ORDER
def query_result(getter_address, search_query, max_distance):

	database_name="FOCo_db"
	conn=sqlite3.connect(database_name);

	address_list=[]
	all_fields_list=[]
	hits=[]
	d={}
	ix=open_dir("indexdir")
	f=open("search_results.txt","a")

	query=""
	search_list= search_query.split(" ")
	for words in search_list:
		words=PorterStemmer().stem(words.lower())
		query= str(query) + str(words) + " OR "
	query=query+" "
	search_query=query
	# print search_query		
	with ix.searcher() as searcher:
		query = MultifieldParser(["title","category","description"], schema=ix.schema).parse(search_query)
    	# query = QueryParser("description" AND "title", ix.schema).parse(u'latest')
		results = searcher.search(query)
		# print results
		for words in results:
			f.write(str(words)+"\n")
			hits.append(str(words))
			# print words.score, words['address']
			address_list.append(words['address'])

			c=conn.cursor();
			x=int(words['id'])
			x=(x,)
			# print x
			for row in c.execute('SELECT id FROM posting_posting where id= ? ',x ):
				all_fields_list.append(row);
	getter_address= (getter_address.lower())
	conn.commit()
	conn.close()
	return add_filter(getter_address, address_list, all_fields_list, max_distance)


# FILTER THE RESULTS ACOORDING TO THE ADDRESS
def add_filter(getter_address, address_list, all_fields_list, max_distance):
	distances=[]
	final_list=[]
	final_all_fields_list=[]
	geolocator = Nominatim()		
	location1 = str(getter_address)
	if location1 is None:
		return
	# print len(address_list)
	for i in range(0,len(address_list)):
		# print words
		try:
			words=address_list[i]
			# print (words)
			location2 = (str(words))
                        if location1[:-1]==location2[:-1]:
				final_list.append(words)
				final_all_fields_list.append(all_fields_list[i][0])
		except Exception as e :
			print e
			continue
	return final_all_fields_list
			

# MAIN FUNCTION
if __name__=="__main__":

	populate_database()

	# assign database_name as desired
	indexdir="indexdir"
	database_name="FOCo_db"
	create_index(indexdir,database_name)

	# assign search_query as entered by the user 
	# hits contains the top search results sorted by relevance and filtered by zipcode
	# hit is the tuple.. use this to display results on web page
	search_query='latest'
	getter_address="76308"
	max_distance=25
	hits=query_result(getter_address, search_query, max_distance)
	print type(hits)
	for hit in hits:
		print (hit)
