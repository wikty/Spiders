import abc

class BaseDb(metaclass=abc.ABCMeta):

	@abc.abstractmethod
	def close(self):
		pass

	@abc.abstractmethod
	def sql(self, q):
		pass

	@abc.abstractmethod
	def create_table(self, tbl_name, fields, extra=None):
		pass

	@abc.abstractmethod
	def select_table(self, tbl_name, fields=[], where_condition=None):
		pass

	@abc.abstractmethod
	def count_table(self, tbl_name, where_condition=None):
		pass

	@abc.abstractmethod
	def insert_table(self, tbl_name, fields={}):
		pass

	@abc.abstractmethod
	def insert_many_table(self, tbl_name, keys, values):
		pass

	@abc.abstractmethod
	def delete_table(self, tbl_name):
		pass

	@abc.abstractmethod
	def update_table(self, tbl_name, fields, where_condition):
		pass