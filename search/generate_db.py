from random_words import RandomWords
from faker import Factory
import random
import sqlite3

import search

NUM_GENERATE = 100

CATEGORIES = ['miscellaneous', 'appliance', 'bedding', 'books', 'clothing',
	'seasonal', 'electronics', 'household', 'kitchen', 'sports']

LOCATIONS = [76301 , 76302, 76305, 76306, 76308, 76309, 76310, 76311, 76367,94538,32456,94568,94356]

def generate_postings(count):
	postings = []
	for i in range(count):
		faker = Factory.create()
		rw = RandomWords()

		posting = {
			'name': faker.name(),
			'email': faker.email(),
			'phone': random.randint(1000000000, 9999999999),
			'title': " ".join(rw.random_words(count=random.randint(1, 3))),
			'description': " ".join(rw.random_words(count=random.randint(3, 9))),
			'category': random.choice(CATEGORIES),
			'address': random.choice(LOCATIONS),
		}
		postings.append(posting)
	return postings


def write_database(postings):
	conn=sqlite3.connect('FOCo_db');
	c=conn.cursor()
	for post in postings:
		# name email phone address category description title
		c.execute('''INSERT INTO posting_posting (
				id,
				name,
				email,
				phone,
				address,
				category,
				description,
				title
			) VALUES (null, '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (
				post['name'],
				post['email'],
				post['phone'],
				post['address'],
				post['category'],
				post['description'],
				post['title']
			)
		)
	conn.commit()
	conn.close()
	print str(len(postings)) + " postings written to database"


if __name__ == '__main__':

	postings = generate_postings(NUM_GENERATE)
	write_database(postings)
	search.create_index("indexdir", "FOCo_db")
