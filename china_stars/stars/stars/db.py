import sqlite3, sys
import settings

sqlite_file = settings.SQLITE_FILE
sqlite_table = settings.SQLITE_TABLE
sqlite_table_desc = settings.SQLITE_TABLE_DESC

def create_table():
	client = sqlite3.connect(sqlite_file)
	cursor = client.cursor()

	sql = 'CREATE TABLE IF NOT EXISTS {table} ({fields})'
	fields = ['id INTEGER PRIMARY KEY AUTOINCREMENT']
	for field, dtype in sqlite_table_desc.items():
		if dtype == 'i':
			field = '%s INTEGER' % field
		elif dtype == 'S':
			field = '%s TEXT' % field
		else:
			field = '%s VARCHAR(255)' % field
		fields.append(field)
	sql = sql.format(table=sqlite_table, fields=', '.join(fields))
	print('SQL:', sql)
	cursor.execute(sql)
	client.commit()
	client.close()

def select_table():
	client = sqlite3.connect(sqlite_file)
	cursor = client.cursor()
	sql = 'SELECT * FROM {table}'.format(table=sqlite_table)
	results = cursor.execute(sql)
	print('SQL:', sql)
	for row in results:
		print(row)
	client.close()

def delete_table():
	client = sqlite3.connect(sqlite_file)
	cursor = client.cursor()
	sql = 'DROP TABLE IF EXISTS {table}'.format(table=sqlite_table)
	cursor.execute(sql)
	print('SQL:', sql)
	client.close()

if __name__ == '__main__':
	if len(sys.argv)<2:
		select_table()
	elif sys.argv[1] == 'create':
		create_table()
	elif sys.argv[1] == 'delete':
		delete_table()
	else:
		select_table()