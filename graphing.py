import dbConnection
import matplotlib.pyplot as pt
import numpy as np
from userClass import retrieveEmissions

"""

vehicle = input("Please provide your vehicle's registration number: ")
print(vehicle)
sqlValue = "SELECT value FROM car_emissions WHERE Vehicle = %s" #SQL query to pass
cursor = dbConnection.db.cursor()#buffered = True) #get cursor from dbConnection.py. use buffered to allow for multipe returns
cursor.execute(sqlValue, (vehicle,)) #execute the SQL
#dbConnection.db.commit()
valueResult = cursor.fetchall() #store restult in variable

sqlDate = "SELECT date FROM car_emissions WHERE Vehicle = %s"
cursor.execute(sqlDate, (vehicle,))
#dbConnection.db.commit
valueDate = cursor.fetchall()

#valueDate = str(valueDate).strip('[]')
#valueDate = valueDate.replace("'", "")

#valueResult = str(valueResult).strip('[]')
#valueResult = valueResult.replace("'", "")

values = []
dates = []

for i in valueResult:
    values.append(i[0])
 
for i in valueDate:
    dates.append([i[0]])

print(values)
print(dates)

"""


