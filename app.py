from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import sqlite3
import Category
from collections import deque
from network import *
TIKI_URL = 'https://tiki.vn'
app = Flask(__name__)

conn = sqlite3.connect('tiki.db')
cur = conn.cursor()

def create_categories_table():
    query = """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            url TEXT,
            parent_id INT,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    try:
        cur.execute(query)
    except Exception as err:
        print('ERROR WHEN CREATE TABLE', err)
def select_all():
    return cur.execute("SELECT * FROM categories").fetchall()
def delete_all():
    return cur.execute("DELETE FROM categories")

def get_main_categories(save_db = False):
    soup = get_soup(TIKI_URL)
    result = []
    for a in soup.find_all("a",{'class':'MenuItem__MenuLink-tii3xq-1 efuIbv'})
        cat_id = None
        name = a.find('span', {'class':'text'})
        url = a['href']
        parent_id = None
        cat = Category(cat_id, name, url, parent_id)
        if save_db:
            cat.save_into_db()
        result.append(cat)
def get_sub_categories(category, save_db = False):
    name = category.name
    url = category.url
    result = []
    try:
        soup = get_soup(url)
        div_containers = soup.find_all('div',{"class":"list-group-item is-child"})
        for div in div_containers:
            sub_id = None
            sub_name = div.a.text
            sub_url = 'http://tiki.vn' + div.a['href']
            sub_parent_id = category.cat_id
            sub = Category(sub_id, sub_name, sub_url, sub_parent_id)
def get_all_categories(main_categories):
    de = deque(main_categories)
    count = 0
    while de:
        parent_cat = de.popleft()
        sub_cats = get_sub_categories(parent_cat, save_db=True)
        print(sub_cats)
        de.extend(sub_cats)
        count += 1
        if count % 100 = 0:
            print(count, 'times')
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 