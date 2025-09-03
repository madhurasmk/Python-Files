fruits = ['apple', 'banana', 'pears']
book1 = {'title': 'Akashic Records', 'author': 'Ernesto Ortiz'}
book2 = {'title': 'Rework', 'author': 'Jason Fried'}
book3 = {'title': 'Akashic Records'}
book4 = {'title': 'The Secret The Power', 'author': 'Rhonda Byrne'}
books = [book1, book2, book3, book4]
for fruit in fruits:
    print(fruit)
capFruit = []
for fruit in fruits:
    capFruit.append(fruit.upper())
print(capFruit)
capFruit1 = [fruit.upper() for fruit in fruits]
print(capFruit1)
capFruit2 = [fruit.upper() for fruit in fruits if len(fruit) <=5]
print(capFruit2)
startFruitA = {fruit:fruit.upper() for fruit in fruits if not fruit.startswith('a')}
print(startFruitA)
allBooks = [book['title'] for book in books ]
print(allBooks)
# allAuthors = [book['author'] for book in books]
# print(allAuthors) # Fails with an error b/c one of the books doesn't have an author
# allAuthors = [book.get('author') for book in books if book.get('author') is not None]
allAuthors = [book.get('author') for book in books if book.get('author') ]
print(allAuthors)
bookSet = set([book.get('author') for book in books if book.get('author') ])
print(bookSet)
books_authors = {book.get('author') for book in books if book.get('author')}
print(books_authors)
import time
def genFruitName():
    for fruit in fruits:
        time.sleep(1)
        yield fruit
for fruit in genFruitName():
    print(fruit)

def genAuthors():
    for book in books:
        if book.get('author'):
            yield book.get('author')
for author in genAuthors():
    print(author)
print("With list comprehension -> ")
def genAuthorList():
    for author in  [book.get('author') for book in books if book.get('author')]:
        yield author
for author in genAuthorList():
    print(author)
# another variation using list comprehension
print("Variaion with list comprehension -> ")
def genAuthorsFrom():
    yield from  [book.get('author') for book in books if book.get('author')]
for author in genAuthorsFrom():
    print(author)

print("With set comprehension -> ")
def genAuthorsSet():
    yield from  {book.get('author') for book in books if book.get('author')}
for author in genAuthorsSet():
    print(author)

import random
import time

pronouns = ["I", "You", "We", "They"]
verbs = ["eat", "detest", "bathe in", "deny the existence of", "resent", "pontificate about", "juggle", "impersonate", "worship", "misplace", "conspire with", "philosophize about", "tap dance on", "dramatically renounce", "secretly collect"]
adjectives = ["turqoise", "smelly", "arrogant", "festering", "pleasing", "whimsical", "disheveled", "pretentious", "wobbly", "melodramatic", "pompous", "fluorescent", "bewildered", "suspicious", "overripe"]
nouns = ["turnips", "rodents", "eels", "walruses", "kumquats", "monocles", "spreadsheets", "bagpipes", "wombats", "accordions", "mustaches", "calculators", "jellyfish", "thermostats"]

def infinite_random_sentences():
    while True:
        yield from random.choice(pronouns)
        yield " "
        yield from random.choice(verbs)
        yield " "
        yield from random.choice(adjectives)
        yield " "
        yield from random.choice(nouns)
        yield ". "

for letter in infinite_random_sentences():
    print(letter, end="", flush=True)
    time.sleep(0.02)