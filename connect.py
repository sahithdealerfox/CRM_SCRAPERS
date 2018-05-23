import MySQLdb

db = MySQLdb.connect('dealerfox-mysql.czieat2fjonp.us-east-2.rds.amazonaws.com', 'Dealerfox', 'Temp1234', 'CRM')
cursor = db.cursor()
sql = "SHOW TABLES"
cursor.execute(sql)
result = cursor.fetchall()
for i in result:
    print(i)