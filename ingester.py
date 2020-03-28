# Ingester.py
# Takes in the xml file of stackexchange posts and populates a sqlite database with it


#!/bin/usr/python3

import xml.etree.ElementTree as ET
import sqlite3

def ingest():
  tree = ET.parse('bioinformatics_posts_se.xml')
  root = tree.getroot()

  conn = sqlite3.connect('posts.db')
  c = conn.cursor()

  # Create table
  c.execute('''CREATE TABLE posts(
    Id integer, 
    PostTypeId integer, 
    ParentId integer, 
    CreationDate text, 
    ViewCount integer, 
    Score integer, 
    Title text, 
    Tags text, 
    AnswerCount integer, 
    Body text,
    OwnerUserId integer, 
    LastEditorUserId integer, 
    LastEditDate text, 
    LastActivityDate text,
    CommentCount integer
  )''')

  for post in root.findall('row'):
    # Insert a row of data
    sqlite_insert_query = """INSERT INTO posts
          VALUES
          (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    c.execute(sqlite_insert_query, (
        post.get('Id'), 
        post.get('PostTypeId'), 
        post.get('ParentId'),
        post.get('CreationDate'),
        post.get('ViewCount'), 
        post.get('Score'), 
        post.get('Title'), 
        post.get('Tags'), 
        post.get('AnswerCount'), 
        post.get('Body'), 
        post.get('OwnerUserId'), 
        post.get('LastEditorUserId'), 
        post.get('LastEditDate'), 
        post.get('LastActivityDate'), 
        post.get('CommentCount')
    ))


  # Save (commit) the changes
  conn.commit()

  # We can also close the connection if we are done with it.
  # Just be sure any changes have been committed or they will be lost.
  conn.close()

