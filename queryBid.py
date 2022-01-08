#!C:\Users\rabey\AppData\Local\Programs\Python\Python37\python.exe 

import cgi
import mysql.connector

print("Content-Type: text/html")
print()

mydb = mysql.connector.connect(
host="localhost",
user= "root",
passwd ="Estail123?",
database="SupplyDB")

cursor = mydb.cursor()

form = cgi.FieldStorage()
switcher = {
        "S.sid": "supplier's id",
        "S.sname": "supplier's name",
        "S.address": "supplier's address",
        "C.cost": "price that supplier charged"
    }
if 'query1' in form:
  if 'pname' not in form:
    print('<h2>please enter part name</h2>')  
  pname = form['pname'].value.strip().capitalize()
  print("<h2>Part name entered: "+pname+"</h2>")
  cursor.execute("Select P.pid From Parts P WHERE P.pname= "+"'"+pname+"'")
  if (len(cursor.fetchall()) == 0):
    print("<h2>This part doesn't exist</h2>")
    exit()
  cols = form.getlist('checkbox')
  if(len(cols)==0):
    print('<h2>please select at least one checkbox</h2>')
    exit()
  sql="SELECT "+",".join(cols)+" FROM Suppliers S, Parts P, Catalog C WHERE S.sid=C.sid AND P.pid=C.pid AND pname= "+"'"+pname+"'"
  cursor.execute(sql)
  results = cursor.fetchall()
  headings = ""
  numcol = 0
  title=[]
  for c in cols:
    numcol +=1
    headings += "<th>"+switcher.get(c)+"</th>"
    title.append(switcher.get(c))
  print("<h2>information of suppliers who supplied "+pname+"</h2>")
  print('<table align="center" border><tr>'+headings+'</tr>')
  for x in results:
    td = ""
    for i in range(numcol):
      td += '<td>'+str(x[i])+'</td>'
    print('<tr>'+td+'</tr>')
  print('</table>')

elif  'query2' in form:
  if 'cost' not in form:
    print('<h2>please enter a price</h2>')
  cost = int(form['cost'].value.strip())
  if (cost<=0):
    print('<h2>please enter a positive number as a cost</h2>')
    exit()
  print("<h2>Cost entered: "+str(cost))
  print('<h2>Names of suppliers who ever supplied a part for $'+str(cost)+' or higher</h2>')
  sql= "Select DISTINCT S.sname From  Suppliers S, Catalog C WHERE S.sid=C.sid AND C.cost >= "+str(cost)
  cursor.execute(sql)
  results = cursor.fetchall()
  if (len(results) == 0):
    print('<h2>no one supplied any part for this price or a higher price</h2>')
    exit()  
  print("<table align='center' border><tr><th>Supplier's name</th></tr>")
  for x in results:
    print('<tr><td>'+str(x[0])+'</td></tr>')
  print('</table>')  

elif  'query3' in form:
  if 'pid' not in form:
    print('<h2>please enter a part id</h2>')  
  pid = form['pid'].value.strip().capitalize() 
  print("<h2>Part Id entered: "+pid+"</h2>")
  sql = "SELECT P.pid FROM Parts P WHERE P.pid = "+"'"+pid+"'"
  cursor.execute(sql)
  results = cursor.fetchall()
  if (len(results) == 0):
    print("<h2>Invalid Part Id. This Part doesn't exists</h2>")
    exit()
  print('<h2>Names and addresses of suppliers who charged the most for  part '+str(pid)+'</h2>')
  sql= "SELECT S.sname, S.address FROM Suppliers S, Catalog C WHERE S.sid= C.sid AND C.pid= "+"'"+pid+"'"+" AND C.cost >= ALL (SELECT C.cost FROM Catalog C WHERE C.pid = "+"'"+pid+"'"+")"
  cursor.execute(sql)
  results = cursor.fetchall()
  if (len(results) == 0):
    print('<h2>no Supplier supplied this part</h2>')
    exit()  
  print("<table align='center' border><tr><th>Supplier's name</th><th>Address</th></tr>")
  for x in results:
    print('<tr><td>'+str(x[0])+'</td><td>'+str(x[1])+'</td></tr>')
  print('</table>')  

elif  'query4' in form:
  missingInputs = []
  errorMessagesforInvalidInput = []
  terminate = False
  if 'color' not in form: 
    missingInputs.append('color')
    terminate = True
  else:
    color = form['color'].value.strip()
    sql = "SELECT P.pid FROM Parts P WHERE P.color = "+"'"+color+"'"
    cursor.execute(sql)
    results = cursor.fetchall()
    if (len(results) == 0):
      terminate = True
      errorMessagesforInvalidInput.append("<h2>Invalid color. There is no part with this color. Please enter a valid color</h2>")
  
  if 'address' not in form:
    missingInputs.append('address')
  else:
    address = form['address'].value.strip().title()
    sql = "SELECT S.address FROM Suppliers S WHERE S.address = "+"'"+address+"'"
    cursor.execute(sql)
    results = cursor.fetchall()
    if (len(results) == 0):
      terminate = True
      errorMessagesforInvalidInput.append('<h2>Invalid address. There is no supplier with this address. Please enter a valid address</h2>')    
  
  if (missingInputs):
    print("<h2>please enter "+" and ".join(missingInputs)+"</h2>")
  if(errorMessagesforInvalidInput):
    for message in errorMessagesforInvalidInput:
      print(message)
  if(terminate):
    exit()
   
  #color = form['color'].value.strip()
  #sql = "SELECT P.pid FROM Parts P WHERE P.color = "+"'"+color+"'"
  #cursor.execute(sql)
  #results = cursor.fetchall()
  #invalidData = False
  #if (len(results) == 0):
    #print('<h2>Invalid color.There is no part with this color. Please enter a valid color</h2>')
    #invalidData = True    

  print("<h2> color: "+color+"</h2>")
  print("<h2> Address: "+address+"</h2>")
  print("<h2> Names of "+color+" parts supplied by suppliers who live at "+address+"</h2>")
  sql = "SELECT P.pname FROM Parts P WHERE P.color = " + "'" + color+ "'"+"AND NOT EXISTS "+\
  "(SELECT S.sid FROM Suppliers S WHERE S.address = "+ "'" + address + "'" + "AND S.sid NOT IN"+\
  "(SELECT C.sid FROM Catalog C WHERE C.pid = P.pid))"
  cursor.execute(sql)
  results = cursor.fetchall()
  if (len(results) == 0):
    print("<h3 align='center'>There is no "+color+" part which is supplied by all the suppliers living at "+address+"</h3>")
    exit()  
  print("<table align='center' border><tr><th>Part's name</th></tr>")
  for x in results:
    print('<tr><td>'+str(x[0])+'</td></tr>')
  print('</table>')  
  
elif  'query5' in form:
  if 'address' not in form:
    print("<h2>please enter a Supplier's address</h2>")  
  address = form['address'].value.strip().title() 
  sql = "SELECT S.address FROM Suppliers S WHERE S.address = "+"'"+address+"'"
  cursor.execute(sql)  
  results = cursor.fetchall()
  if (len(results) == 0):
    print("<h2>Invalid address. This address doesn't exists</h2>")
    exit()
  print("<h2>names and sids of suppliers who live at"+address+" and did not supply any part </h2>")
  sql= "SELECT S.sid, S.sname FROM Suppliers S WHERE S.address ="+"'"+address+"'"+" AND S.sid NOT IN(SELECT C.sid FROM Catalog C)"
  cursor.execute(sql)
  results = cursor.fetchall()
  if (len(results) == 0):
    print('<h2>Everyone living here supplied a part</h2>')
    exit()  
  print('<table align="center" border><tr><th>Supplier"s sid</th><th>supplier"s name</th></tr>')
  for x in results:
    print('<tr><td>'+str(x[0])+'</td><td>'+str(x[1])+'</td></tr>')
  print('</table>')    
else:
  print("<h1>submit NOT detected</h1>")