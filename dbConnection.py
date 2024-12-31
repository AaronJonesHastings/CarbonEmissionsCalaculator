import mysql.connector
from mysql.connector import errorcode #to handle error messages when updating and performing queries

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "d4urVmrq1!",
    database = "carbonemissionscalculator"
)
