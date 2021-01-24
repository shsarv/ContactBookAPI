'''
An Api for a ContactBook with features like adding, deleting and updating contacts.
that also suports searching of a contact using name or emailID.

'''
# importing flask and its modules
from flask import Flask,redirect,url_for,render_template,request,jsonify

# importing pymongo to work with MongoDB.
from flask_pymongo import PyMongo

# importing bson dumps to convert bson files.
from bson.json_util import dumps
from bson.objectid import ObjectId

#creating app
app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/ContactBook"
mongo = PyMongo(app)


@app.route('/')
def operation():
    Operations = {
    1: '/add (enter name, emailID and mobile number you want to add to your contact book)',
    2: '/delete (enter emailID of contact person you need to Delete)', 
    3: '/update (enter new name, emailID and mobile number, you need to update)', 
    4: '/searchByEmail (enter emailID of person you want to search)', 
    5: '/searchByName (enter Contact-person name you want to search)',
    0 :'enter details of every path in Json format only.'
    }
    return jsonify(data=Operations)

# route and function to add new Contact.

@app.route('/add', methods=['POST'])
def add_contact():
    my_json = request.json
    contact_name = my_json['name']
    contact_email = my_json['email']
    contact_mobile = my_json['mobile']
    condtion = dumps(mongo.db.contact.find({"_id": contact_email}))
    print(condition)
    if condition != "[]":
        return jsonify("Ooops !!!!, This emailID already exists,check EmailID or use a different EmailID !")

    elif contact_name and contact_email and contact_mobile and request.method == 'POST':
        mongo.db.contact.insert({'_id': contact_email, 'name': contact_name, 'mobile': contact_mobile})
        result = jsonify("User Added Successfully")
        result.status_code = 200
        return result
    else:
        return error_handle()

# Route & function to delete a Contact.

@app.route('/delete', methods=['DELETE'])
def delete_contact():
    my_json = request.json
    email_todelete = my_json["email"]
    mongo.db.contact.delete_one({"_id": email_todelete})
    result = jsonify("Contact with given emailID deated SuccessFully")
    result.status_code = 200
    return result

# Route & function to update a Contact.

@app.route('/update', methods=['PUT'])
def updateContact():
    my_json = request.json
    email_toupdate = my_json["email"]
    name_toupdate = my_json["name"]
    mobile_toupdate = my_json["mobile"]

    if name_toupdate and email_toupdate and mobile_toupdate and request.method == 'PUT':
        mongo.db.contact.update_one({"_id": email_toupdate}, {'$set': {'name': name_toupdate, 'mobile': name_toupdate}})
        result = jsonify("Contact updation Successful.")
        result.status_code = 200
        return result
    else:
        return error_handle()

# Route & function to searching a Contact using contact name.

@app.route('/searchByName', methods=['GET'])
def searchByName():
    my_json = request.json
    name_tosearch = my_json["name"]
    user_check = mongo.db.contact.find({"name": name_tosearch})
    result = dumps(user_check)
    if result == "[]":
        return jsonify("User with this Name is not found")
    return result


# Route & function to search a Contact using EmailID.

@app.route('/searchByEmail', methods=['GET'])
def searchByEmail():
    myn_json = request.json
    email_tosearch = myn_json["email"]
    user_check = mongo.db.contact.find({"_id": email_tosearch})
    result = dumps(user_check)
    if result == "[]":
        return jsonify("No Contact person found with given emailID")
    return result

# To Handle 404 ERROR

@app.errorhandler(404)
def error_handle(error=None):
    message = {'message': 'Oooops !!, Can not reach your proposed request. kindly check the details & fill correctly !!!'}
    result = jsonify(message)
    result.status_code = 404
    return result

# main Function

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)

