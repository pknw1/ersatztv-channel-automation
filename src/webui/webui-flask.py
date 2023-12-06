from flask import Flask
import pyodbc
conn = pyodbc.connect(connstr)
cursor = conn.cursor()


sql = "SELECT top 100 * FROM [dbo].[PATIENT_ELIGIBILITY]"
cursor.execute(sql)
data = cursor.fetchall()

#Query1
for row in data :
    print (row[1])

#Query2
print (data)

#Query3
data



app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'