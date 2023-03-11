import flask
import hashlib
from flask import jsonify
from flask import request
from sql import create_connection, execute_query
from sql import execute_read_query
from flask import request, make_response
from datetime import datetime
import creds

#creating connection to mysql database
myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
cursor = conn.cursor(dictionary = True)

#setting up the name
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser

#########################################SECURITY########################################################################

#Code from Class06 Securityapi.py
# password 'password' hashed from 
masterPassword = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
masterUsername = 'username'

@app.route('/authenticatedroute', methods=['GET'])
def auth_example():
    if request.authorization:
        encoded=request.authorization.password.encode() #unicode encoding
        hashedResult = hashlib.sha256(encoded) #hashing
        if request.authorization.username == masterUsername and hashedResult.hexdigest() == masterPassword:
            return '<h1> WE ARE ALLOWED TO BE HERE </h1>'
    return make_response('COULD NOT VERIFY!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})




@app.route('/', methods=['GET']) # default url without any routing as GET request
def home():
    return "<h1> WELCOME TO MY Final Project API! </h1>"




#API FOR CAPTAIN
#GET specific Captain using captain badge http://127.0.0.1:5000/api/captains?id=
@app.route('/api/captains', methods=['GET']) # #
def api_captains_id():
    if 'id' in request.args: 
        id = int(request.args['id'])
    else:
        return 'ERROR: No valid ID provided!' 
    sql = "SELECT capt_badge, fname, lname, ranking, homeplanet FROM Captains WHERE capt_badge = %s" %(id)
    cursor=conn.cursor()
    cursor.execute(sql)
    records=cursor.fetchall()
    for records in records:
        capt_dict= {
            "Capt_badge ": records[0],
            "First_Name ":records[1],
            "Last_Name ":records[2],
            "Ranking ": records[3],
            "Home PLanet ": records[4]
        }
    return jsonify(capt_dict)

#GET  ALL Captains using  http://127.0.0.1:5000/api/captains/all
@app.route('/api/captains/all', methods=['GET'])
def api_getallcaptains():
    sql = "SELECT capt_badge, fname, lname, ranking, homeplanet FROM Captains"
    cursor=conn.cursor()
    cursor.execute(sql)
    records=cursor.fetchall()
    captains = []
    for record in records:
        captain = {
            'Captain Badge ': record[0],
            'First_Name': record[1],
            "Last_Name ":record[2],
            "Ranking ": record[3],
            "Home PLanet ": record[4]
        }
        captains.append(captain)
    response = {'captains': captains}
    return jsonify(response)
    
#Delete Captains using ID in http://127.0.0.1:5000/api/captains/delete/(capt_badge)
@app.route('/api/captains/delete/<int:capt_badge>', methods= ['DELETE'])
def delete_captain(capt_badge):
    delete = "DELETE FROM Captains WHERE capt_badge = '%s'" % (capt_badge)
    execute_query(conn, delete)
    return 'Captain ' +str(capt_badge)+' has been deleted.'

#PUT (udpate) Captain using JSON format http://127.0.0.1:5000/api/captains/update/(capt_badge) 
@app.route('/api/captains/update/<int:capt_badge>', methods=['PUT'])
def update_captains(capt_badge):
    request_data = request.json
    updfname = request_data['fname']
    updlname = request_data['lname']
    updrank = request_data['ranking']
    updhome = request_data['homeplanet']
    update_query = "UPDATE Captains SET  fname='%s', lname='%s', ranking='%s', homeplanet='%s' WHERE capt_badge=%s" % (updfname,updlname,updrank,updhome,capt_badge)
    execute_query(conn, update_query)
    return 'Captain '+ str(capt_badge)+' updated successfully'

#POST (add) captain  into table in JSON format in http://127.0.0.1:5000/api/captains
@app.route('/api/captains', methods=['POST'])
def api_addcaptain():
    request_data = request.get_json()
    capt_badge = request_data['capt_badge']
    newfname = request_data['fname']
    newlname = request_data['lname']
    newrank = request_data['ranking']
    newhome = request_data['homeplanet']
    
    add = "INSERT INTO Captains (capt_badge, fname, lname, ranking, homeplanet) values (%s,'%s', '%s',' %s', '%s')" % (capt_badge,newfname, newlname, newrank, newhome)
    execute_query(conn,add)
    return 'Captain added successfully'

####################### #API for spaceship #########
#GET spaaceships using ID http://127.0.0.1:5000/api/spaceship/all
@app.route('/api/spaceship/all', methods=['GET']) # #
def api_spaceship_id():

    sql = "SELECT maxweight, ship_tag FROM spaceship"
    cursor=conn.cursor()
    cursor.execute(sql)
    records=cursor.fetchall()
    spaceships = []
    for record in records:
        spaceship = {
            'Maxweight For Ship ': record[0],
            'Ship Tag': record[1]
        }
        spaceships.append(spaceship)
    response = {'Spaceships': spaceships}
    return jsonify(response)
    
#GET specific spaaceships using ID http://127.0.0.1:5000/api/spaceship
@app.route('/api/spaceship', methods=['GET']) # #
def api_onespaceship_id():
    if 'id' in request.args: 
        id = str(request.args['id'])
    else:
        return 'ERROR: No valid ID provided!'
    sql = "SELECT maxweight, ship_tag FROM spaceship where ship_tag= '%s'"%id
    cursor=conn.cursor()
    cursor.execute(sql)
    records=cursor.fetchall()
    spaceships = []
    for record in records:
        spaceship = {
            'Maxweight For Ship ': record[0],
            'Ship Tag': record[1]
        }
        spaceships.append(spaceship)
    response = {'Spaceship': spaceships}
    return jsonify(response)
    



#Delete Spaceship using ID in http://127.0.0.1:5000/api/spaceship/delete/(ship_tag)
@app.route('/api/spaceship/delete/<string:ship_tag>', methods= ['DELETE'])
def delete_spaceship(ship_tag):
    delete = "DELETE FROM spaceship WHERE ship_tag= '%s'" % (ship_tag)
    execute_query(conn, delete)
    return 'Spaceship with Tag ' +str(ship_tag)+' has been deleted.'

#POST(add) new spaceship  into table in JSON format in http://127.0.0.1:5000/api/spaceship
@app.route('/api/spaceship', methods=['POST'])
def api_addspaceship():
    #Get JSON info
    request_data = request.get_json()
    newmaxweight = request_data['maxweight'] 
    newshiptag = request_data['ship_tag']
    newcapt = request_data['capt_badge']
    #Check captain ID
    captain="SELECT id FROM Captains WHERE capt_badge=%s" % newcapt
    cursor=conn.cursor()
    cursor.execute(captain)
    results = cursor.fetchall()
    capid=results[0][0]
    add = "INSERT INTO spaceship (maxweight, ship_tag, capt_badge, captainid) values (%s, '%s', %s, %s)" %  (newmaxweight, newshiptag,newcapt,capid)
    execute_query(conn, add)
    return 'Spaceship added successfully'


#PUT (update) spaceship weight/capbadge in JSON format http://127.0.0.1:5000/api/spaceship/update/(ship_tag) 
@app.route('/api/spaceship/update/<string:ship_tag>', methods=['PUT'])
def update_spaceship(ship_tag):
    request_data = request.json
    updmaxweight = request_data['maxweight']
    updcapid = request_data['capt_badge']
    # Check captain ID
    captain = "SELECT id FROM Captains WHERE capt_badge=%s" % updcapid
    cursor = conn.cursor()
    cursor.execute(captain)
    results = cursor.fetchall()
    capid = results[0][0]
    update_query = "UPDATE spaceship SET maxweight=%s, capt_badge=%s, captainid=%s WHERE ship_tag= '%s'" % (updmaxweight,updcapid,capid,ship_tag)
    execute_query(conn, update_query)
    return 'Spaceship tag ' +(ship_tag)+ ' updated successfully'

################## #API for cargo #########

#GET  specific cargo using order ID http://127.0.0.1:5000/api/cargo/order?id=
@app.route('/api/cargo/order', methods=['GET']) # #
def api_cargo_id():
    if 'id' in request.args: 
        id = int(request.args['id'])
    else:
        return 'ERROR: No valid ID provided!'
    
    sql = "SELECT order_id,weight,cargotype,departure,arrival, ship_tag FROM cargo where order_id=%s" %id
    cursor=conn.cursor()
    cursor.execute(sql)
    records=cursor.fetchall()
    cargos = []
    for record in records:
        cargo = {
            'Order ID:  ': record[0],
            'Max Weight of Ship: ': record[1],
            'Cargo Type: ':record[2],
            'Departure Date': record[3],
            'Arrival Date': record[4],
            'Ship Tag': record[5]
        }
        cargos.append(cargo)
    response = {'cargo': cargos}
    return jsonify(response)

#Get all cargo using http://127.0.0.1:5000/api/cargo/all
@app.route('/api/cargo/all',methods=['GET'])
def api_cargo_all():
    sql = "SELECT order_id,weight, cargotype, departure, arrival, ship_tag FROM cargo"
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cargo_list = []
    for row in result:
        cargo = {
           
            'weight': row[1],
            'cargotype': row[2],
            'departure': str(row[3]) if row[3] else '',
            'arrival': str(row[4]) if row[4] else '',
            'ship_tag': row[5],
            'order_id':row[0]
        }
        cargo_list.append(cargo)
    return jsonify(cargo_list)

#PUT (update) order_id/cargotype cargo using JSON format http://127.0.0.1:5000/api/cargo/update/(order_ID) date format YYYY-MM-DD 
@app.route('/api/cargo/update/<int:order_id>', methods=['PUT'])
def update_cargo(order_id):
    request_data = request.json
    updorder = request_data['order_id']
    updcargotype = request_data['cargotype']
    update_query = "UPDATE cargo SET order_id=%s,cargotype='%s' WHERE order_id=%s" % (updorder,updcargotype,order_id)
    execute_query(conn, update_query)
    return 'Cargo ID ' +str(order_id)+ ' updated successfully'


#PUT (update) cargo arrival time using JSON format http://127.0.0.1:5000/api/cargo/arrival/order/(order_ID) UPDATING ARRIVAL TIME YYYY-MM-DD
@app.route('/api/cargo/arrival/order/<int:order_id>', methods=['PUT'])
def update_cargo_arrival(order_id):
    request_data = request.json 
    updarrival = request_data['arrival']
    checktime = "Select departure fROM cargo WHERE order_id=%s" %(order_id) #Retrieve cargo's departure time
    cursor = conn.cursor()
    cursor.execute(checktime)
    records = cursor.fetchall()
    if records:
        #compares time
        departure_str = records[0][0].strftime('%Y-%m-%d') #https://www.programiz.com/python-programming/examples/string-to-datetime
        departure = datetime.strptime(departure_str, '%Y-%m-%d')
        arrival = datetime.strptime(updarrival, '%Y-%m-%d')
        if arrival >= departure:
            update_query = "UPDATE cargo SET arrival='%s' WHERE order_id=%s" % (updarrival, order_id)
            execute_query(conn, update_query)
            return 'Cargo ID ' + str(order_id) + ' has been given an updated arrival time of ' + str(updarrival)
        else:
            return 'Arrival date cannot be before departure'
    else:
        return 'Cargo ID ' + str(id) + ' not found'    

#Put (update) cargo departure time using JSON format http://127.0.0.1:5000/api/cargo/departure/(order_ID) ADDING DEPARTURE TIME YYYY-MM-DD
@app.route('/api/cargo/departure/order/<int:order_id>', methods=['PUT'])
def update_cargo_departure(order_id):
    request_data = request.json
    upddeparture = request_data['departure']
    insert = "UPDATE cargo SET departure='%s' WHERE order_id =%s" %(upddeparture,order_id)
    execute_query(conn,insert)
    return 'Cargo Order ' +str(order_id) + ' has been updated with departure ' +str(upddeparture)


#POST (add)new cargo in JSON format in http://127.0.0.1:5000/api/cargo
@app.route('/api/cargo', methods=['POST'])
def api_cargo():
    request_data = request.get_json()
    newasset = request_data['order_id']
    newweight = request_data['weight']
    newcargotype = request_data['cargotype']
    newshiptag = request_data['ship_tag']
    checkweight = "SELECT  maxweight, id FROM spaceship WHERE ship_tag= '%s'" %(newshiptag)
    cursor = conn.cursor()
    cursor.execute(checkweight)
    record = cursor.fetchone()

    if record and record[0] >= newweight:
        add = "INSERT INTO cargo (order_id, weight, cargotype, ship_tag ,ship_id) values (%s, %s, '%s','%s',%s)" %  (newasset, newweight, newcargotype, newshiptag,record[1])
        execute_query(conn, add)
        return("Cargo has been added successfully")    
    else:
        return("Ship is unable to support weight")
        
#Delete cargo using ID in http://127.0.0.1:5000/api/cargo/delete/(order ID)
@app.route('/api/cargo/delete/<int:order_id>', methods= ['DELETE'])
def delete_cargp(order_id):
    delete = "DELETE FROM cargo WHERE order_id = %s" % (order_id)
    execute_query(conn, delete)
    return 'Cargo with ID ' +str(order_id)+' has been deleted.'


app.run()