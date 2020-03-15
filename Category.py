import sqlite3
class Category:
	def __init__(self, cat_id, name, url, parent_id):
		self.cat_id = cat_id
		self.name = name
		self.url = url
		self.parent_id = parent_id
		self.child_cats = []
	def get_cat_id(self):
		return self.cat_id
	def add_child_cats(self,child_cats):
		self.child_cats += child_cats
	def get_name(self):
		return self.name

	def get_url(self):
		return self.url

	def get_parent_id(self):
		return self.parent_id

	def save_into_db(self):
		query = """
            INSERT INTO categories (name, url, parent_id)
            VALUES (?, ?, ?);
        """
		conn = sqlite3.connect('tiki.db')
		cur = conn.cursor()
		self.name = self.name.strip()
		val = (self.name, self.url, self.parent_id)
		try:
			cur.execute(query, val)
			self.cat_id = cur.lastrowid
			conn.commit()
		except Exception as err:
			print('error by insert: ', err)

	def __repr__(self):
 		return "cat_id: "  + " , " + "name: " + str(self.name) + " , " + "url: " + str(self.url) + " , " + "parent_id: " 
