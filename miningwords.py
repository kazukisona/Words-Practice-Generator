# Author: Kazuki Sona
# Program: gre_words.py
# This program contains rutines to extract GRE words from the website
# and put them into SQLite3 database for word list generator project

from bs4 import BeautifulSoup
import requests
import sqlite3, re

# take in a request object and return a list of words
def makeWordList(res):
    soup = BeautifulSoup(res.content.decode('utf-8', 'ignore'), 'html5lib')
    
    return [word.text for word in soup.find_all('th')]


# @res: Request object
# definitions of words
def makeDefList(res):
    soup = BeautifulSoup(res.content.decode('utf-8', 'ignore'), 'html5lib')    
    
    return [mean.text for mean in soup.find_all('td')]


# @word_list: a list of word
# @mean_list: a list of meaning for corresponding word
# return a list of pair of word and defin
def makePair(word_list, mean_list):
    
    return [p for p in zip(word_list, mean_list)]


def makeFinalList():
    base_url = "http://www.majortests.com/gre/wordlist.php"

    # create a Session to persist a connection in a process
    s = requests.Session()
    r = s.get(base_url)

    # let BeautifulSoup analyze and scrape the content of the website
    soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), 'html5lib')

    # select only needed links which end with "wordlist_" and decimal number
    href_list = [h for h in [a['href'] for a in soup.find_all('a')] if re.search("wordlist_\d", h)]

    # list for storing a final output
    results = []

    # iterate over links of words list
    # and make a list of (word, def.)
    for i in range(len(href_list)):
        res = s.get(href_list[i])
        results += makePair(makeWordList(res), makeDefList(res))

    return results

# @db: sqlite3 database object
def loadData(db):

    # get a cursor object
    cursor = db.cursor()

    # get data which is a sorted list of a pair of word and meaning
    data = makeFinalList()

    # insert data into database
    # i = id, wm[0] = word, wm[1] = meaning
    cursor.executemany("""INSERT INTO words (id, word, meaning) VALUES (?, ?, ?)""", [(i, wm[0], wm[1]) for i, wm in enumerate(data)])
    db.commit()

