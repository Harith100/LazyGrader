import pymysql

# Establish the connection to the MySQL database
connection = pymysql.connect(
    host="localhost",    # MySQL server host
    user="root",         # MySQL username
    password="root",  # MySQL password
    database="university"  # The database you want to use
)

# Create a cursor object
cursor = connection.cursor()

# Execute the SHOW TABLES query to get the list of tables
cursor.execute("SHOW TABLES")

# Fetch all the tables
tables = cursor.fetchall()

# Display the tables
print("Tables in 'university' database:")
for table in tables:
    print(table[0])  # Each 'table' is a tuple, so we print the first element (the table name)

# Close the cursor and connection
cursor.close()
connection.close()
