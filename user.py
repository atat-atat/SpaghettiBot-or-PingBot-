class User:

	"""
0 - > normal
1 - > vip
2 - > admin
3 - > master
"""


	ROLES = ["normal","vip","admin","master"]
	
	def __init__(self, userid, permission=0):
		self.__id = userid
		self.__permission = permission
		
		@property
		def id(self):
			return self.__id
			
		@property
		def permission(self):
			return self.__permission
			
		@property.setter
		def permission(self, val):
			if val >= 0 and val < 4:
				self.__permission = val
			
		def mention(self):
			return "<@{}>".format(self.__id)