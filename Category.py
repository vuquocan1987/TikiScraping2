class Category:
	def __init__(self, cat_id, name, url, parent_id):
		self.cat_id = cat_id
		self.name = name
		self.url = url
		self.parent_id = parent_id
		
	def get_cat_id(self):
		return self.cat_id

	def get_name(self):
		return self.name

	def get_url(self):
		return self.url

	def get_parent_id(self):
		return self.parent_id


	def __str__(self):
 		return "cat_id: " + self.cat_id + " , " + "name: " + self.name + " , " + "url: " + self.url + " , " + "parent_id: " + self.parent_id
