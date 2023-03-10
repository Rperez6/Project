import flask
from flask import jsonify
from flask import request
from sql import create_connection, execute_query
from sql import execute_read_query
from datetime import datetime
import creds

#creating connection to mysql database
myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
cursor = conn.cursor(dictionary = True)

#setting up the name
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser

@app.route('/', methods=['GET']) # default url without any routing as GET request
def home():
    return "<h1> WELCOME TO MY Final Project API! </h1>"


#API FOR CAPTAIN
#GET specific Captains captain ID http://127.0.0.1:5000/api/captains?id=
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

#GET  ALL Captains using ID http://127.0.0.1:5000/api/captains
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
#GET spaaceships using ID http://127.0.0.1:5000/api/spaceship
@app.route('/api/spaceship', methods=['GET']) # #
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
    response = {'spaceships': spaceships}
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
    
    if len(results) == 0:
        return 'ERROR: Captain badge not found!'
    
    capid=results[0][0]
    add = "INSERT INTO spaceship (maxweight, ship_tag, capt_badge, captainid) values (%s, '%s', %s, %s)" %  (newmaxweight, newshiptag,newcapt,capid)
    execute_query(conn, add)
    return 'Spaceship added successfully'


#PUT (update) spaceship using JSON format http://127.0.0.1:5000/api/spaceship/update/(ship_tag) 
@app.route('/api/spaceship/update/<string:ship_tag>', methods=['PUT'])
def update_spaceship(ship_tag):
    request_data = request.json
    updmaxweight = request_data['maxweight']
    updcapid = request_data['capt_badge']
    #Check captain ID
    captain="SELECT id FROM Captains WHERE capt_badge=%s" % updcapid
    cursor=conn.cursor()
    ship_tag1=str(ship_tag)
    cursor.execute(captain)
    results = cursor.fetchall()
    capid=results[0]
    update_query = "UPDATE spaceship SET maxweight=%s, capt_badge=%s, captainid=%s WHERE ship_tag='%s'" % (updmaxweight,updcapid,capid,ship_tag1)
    execute_query(conn, update_query)
    return 'Spaceship tag ' +(ship_tag)+ ' updated successfully'


# #API for cargo #########

# #GET  cargo using ID http://127.0.0.1:5000/api/cargo?id=
# @app.route('/api/cargo', methods=['GET']) # #
# def api_cargo_id():
#     if 'id' in request.args: 
#         id = int(request.args['id'])
#     else:
#         return 'ERROR: No valid ID provided!'
    
#     sql = "SELECT * FROM cargo WHERE id = %s" %(id)
#     cargo = execute_read_query(conn, sql)
#     if cargo:
#         return jsonify(cargo[0])
    

# #PUT new cargo using JSON format http://127.0.0.1:5000/api/cargo/(cargo ID) date format YYYY-MM-DD 
# @app.route('/api/cargo/<int:id>', methods=['PUT'])
# def update_cargo(id):
#     request_data = request.json
#     updname = request_data['name']
#     updweight = request_data['weight']
#     updcargotype = request_data['cargotype']
#     updshipid = request_data['shipid']
#     update_query = "UPDATE cargo SET name='%s', weight=%s, cargotype='%s',shipid=%s WHERE id=%s" % (updname,updweight,updcargotype,updshipid,id)
#     execute_query(conn, update_query)
#     return 'Cargo ID ' +str(id)+ ' updated successfully'


# #PUT cargo arrival time using JSON format http://127.0.0.1:5000/api/cargo/arrival/(cargo ID) UPDATING ARRIVAL TIME
# @app.route('/api/cargo/arrival/order/<int:id>', methods=['PUT'])
# def update_cargo_arrival(id):
#     request_data = request.json 
#     updarrival = request_data['arrival']
#     checktime = "Select departure fROM cargo WHERE id=%s" %(id) #Retrieve cargo's departure time
#     cursor = conn.cursor()
#     cursor.execute(checktime)
#     records = cursor.fetchall()
#     if records:
#         departure_str = records[0][0].strftime('%Y-%m-%d') #https://www.programiz.com/python-programming/examples/string-to-datetime
#         departure = datetime.strptime(departure_str, '%Y-%m-%d')
#         arrival = datetime.strptime(updarrival, '%Y-%m-%d')
#         if arrival >= departure:
#             update_query = "UPDATE cargo SET arrival='%s' WHERE id=%s" % (updarrival, id)
#             execute_query(conn, update_query)
#             return 'Cargo ID ' + str(id) + ' has been given an updated arrival time of ' + str(updarrival)
#         else:
#             return 'Arrival date cannot be before departure'
#     else:
#         return 'Cargo ID ' + str(id) + ' not found'    

# #Put cargo departure time using JSON format http://127.0.0.1:5000/api/cargo/departure/(cargo ID) ADDING DEPARTURE TIME
# @app.route('/api/cargo/departure/order/<int:id>', methods=['PUT'])
# def update_cargo_departure(id):
#     request_data = request.json
#     upddeparture = request_data['departure']
#     insert = "UPDATE cargo SET departure='%s' WHERE =%s" %(upddeparture,id)
#     execute_query(conn,insert)
#     return 'Cargo ID ' +str(id) + ' has been updated with departure' +str(upddeparture)


# #POST new cargo in JSON format in http://127.0.0.1:5000/api/cargo
# @app.route('/api/cargo', methods=['POST'])
# def api_cargo():
#     request_data = request.get_json()
#     newname = request_data['name']
#     newweight = request_data['weight']
#     newcargotype = request_data['cargotype']
#     newshipname = request_data['shipname']
#     checkweight = "SELECT maxweight FROM spaceship WHERE id=%s" %(newweight)
#     cursor = conn.cursor()
#     cursor.execute(checkweight)
#     record = cursor.fetchone()
#     if record and record[0] >= newweight:    
#         add = "INSERT INTO cargo (name, weight, cargotype, shipname ) values ('%s', %s, '%s',%s)" %  (newname, newweight, newcargotype, newshipname)
#         execute_query(conn, add)
#         return("Cargo has been added successfully")    
#     else:
#         return("Ship is unable to support weight")
    
# #Delete cargo using ID in http://127.0.0.1:5000/api/cargo/(cargo ID)
# @app.route('/api/cargo/<int:id>', methods= ['DELETE'])
# def delete_cargp(id):
#     delete = "DELETE FROM cargo WHERE id = %s" % (id)
#     execute_query(conn, delete)
#     return 'Cargo with ID ' +str(id)+' has been deleted.'




    



app.run()