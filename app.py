from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import sqlite3
from Category import *
from collections import deque
from network import *
TIKI_URL = 'https://tiki.vn'
app = Flask(__name__)

conn = sqlite3.connect('tiki.db')
cur = conn.cursor()

def create_categories_table():
    conn = sqlite3.connect('tiki.db')
    cur = conn.cursor()
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
    conn = sqlite3.connect('tiki.db')
    cur = conn.cursor()
    return cur.execute("SELECT * FROM categories;").fetchall()
def delete_all():
    conn = sqlite3.connect('tiki.db')
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM categories")
        conn.commit()
    except Exception as err:
        print('error while delete table categori:',err)

def get_main_categories(save_db = False,debug_run=False):
    soup = get_soup(TIKI_URL)
    result = []
    for a in soup.find_all("a",{'class' : 'MenuItem__MenuLink-tii3xq-1 efuIbv'}):
        cat_id = None
        name = a.find('span', {'class':'text'}).text
        url = a['href']
        parent_id = None
        cat = Category(cat_id, name, url, parent_id)
        if save_db:
            cat.save_into_db()
        result.append(cat)
    if debug_run:
        return result[0:3]
    return result
def get_sub_categories(category, save_db = False,debug_run=False):
    name = category.name
    url = category.url
    result = []
    try:
        soup = get_soup(url)
        div_containers = soup.find_all('div',{"class":"list-group-item is-child"})
        print(div_containers)
        for div in div_containers:
            sub_id = None
            sub_name = div.a.text
            sub_url = 'http://tiki.vn' + div.a['href']
            sub_parent_id = category.cat_id
            sub = Category(sub_id, sub_name, sub_url, sub_parent_id)
            if save_db:
                sub.save_into_db()
            result.append(sub)
    except Exception as err:
        print('ERROR BY GET SUB CATEGORIES:', err)
    if debug_run:
        return result[0:2]
    else:
        return result

def get_all_categories(main_categories,debug_run=False):
    de = deque(main_categories)
    count = 0

    while de:
        parent_cat = de.popleft()
        sub_cats = get_sub_categories(parent_cat, save_db=True, debug_run = debug_run)
        print(sub_cats)
        de.extend(sub_cats)
        print(sub_cats)
        count += 1
        if count :
            print(count, 'times')
    return de

def gen_cats_tree():
    cats_list = select_all()
    cats_list = [Category(cat[0],cat[1],cat[2],cat[3] )for cat in cats_list]
    main_cats = [cat for cat in cats_list if cat.parent_id == None]
    de = deque(main_cats)
    while de:
        parent_cat = de.popleft()
        sub_cats = [cat for cat in cats_list if cat.parent_id == parent_cat.cat_id]
        parent_cat.add_child_cats(sub_cats)
        de.extend(sub_cats)
    print(main_cats)
    return main_cats

def init_crawl(debug_run = True):
    create_categories_table()
    delete_all()
    main_cats = get_main_categories(save_db=True,debug_run=debug_run)
    de = get_all_categories(main_cats,debug_run=debug_run)

def parse_html(url):
    soup = get_soup(url)
    soup_item_list = soup.find_all('div', class_ = "content")
    item_list = []
    for soup_item in soup_item_list:
        dict_item = {"title":"","link":"","img_url":"","description":"","price":""}
        try:
            dict_item["title"] = soup_item.find("p", class_ = "title").text
            dict_item["img_url"] = soup_item.img["src"]
            dict_item["price"] = soup_item.find("span", class_="price-regular").text
            item_list.append(dict_item)
        except:
            pass
    return item_list

def convert_2d(items):
    item_lists = []
    while len(items)>2:
        item_lists.append(items[0:3])
        items = items[3:]
    return item_lists
def select_cat(index):
    conn = sqlite3.connect('tiki.db')
    cur = conn.cursor()
    query = "SELECT * FROM categories where id = ?;"
    cat = cur.execute(query,(index,)).fetchall()

    return cat

@app.route('/page/<int:id>')
def content(id):
    gen_cats_tree()
    main_cats = gen_cats_tree()
    cat = select_cat(id)
    url = cat[0][2]
    data = parse_html(url)
    data = convert_2d(data)
    return render_template('base.html',main_cats = main_cats, data=data)

@app.route('/')
def index():
#    init_crawl()
    gen_cats_tree()
    main_cats = gen_cats_tree()
    return render_template('base.html',main_cats = main_cats, data=[])


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 