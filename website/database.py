from pymongo import MongoClient
from scraper import scrape

def register_user(username, password, gpa, status, hours):
    """
    Description
    Creates an account in the database for the user from their inputs

    Parameters
    username:     TYPE: str
                  DESC: user's account username

    password:     TYPE: str
                  DESC: user's account password

    gpa:          TYPE: str
                  DESC: grade point average of user 

    status:       TYPE: str
                  DESC: enrollment status at UMBC

    hours:        TYPE: str
                  DESC: number of credit hours completed

    Returns       True if the account creation was successful
                  False otherwise
    """

    client = MongoClient(host=["mongodb://localhost:27017/"])
    db = client['FWA']
    users = db['users']
    
    #Ensures that all usernames are unique
    if users.count_documents({'username' : username}):
        return False
    
    users.insert_one({'username':username,'password':password,'GPA':gpa,'Enrollment Status':status,"Credit Hours":hours,"logs":[]})

    return True

def register_admin(username, password, admin_key):
    """
    Description
    Creates a new admin account in the database

    Parameters
    username:     TYPE: str
                  DESC: user's account username

    password:     TYPE: str
                  DESC: user's account password
    
    admin_key:    TYPE: str
                  DESC: A one time use admin key to permit 
                  the creation of a new admin account

    Returns       True is successful
                  False otherwise
    """
    client = MongoClient(host=["mongodb://localhost:27017/"])
    db = client['FWA']
    users = db['users']
    keys = db['keys']
    
    #Ensures that all usernames are unique
    if users.count_documents({'username' : username}):
        return False
    
    #Ensures that the user was given an admin key to register
    if keys.count_documents({'key': admin_key}) == 0:
        return False
    
    #Add the admin account to the database
    users.insert_one({'username':username,'password':password, 'scholarships':"Empty", 'admin':True})
    
    #Delete the key they used to register
    keys.delete_one({'key': admin_key})

    return True


def login_user(username, password):
    """
    Description
    Logs user into the requested account

    Parameters
    username:     TYPE: str
                  DESC: user's account username

    password:     TYPE: str
                  DESC: user's account password

    Returns:      A dictionary containing the user's profile
                  False if the account profile doesn't exist
    """
     
    client = MongoClient(host=["mongodb://localhost:27017/"])
    db = client['FWA']
    users = db['users']

    profile = users.find_one({'username' : username, 'password' : password})

    if profile == None:
        return False
    
    else:
        #Convert object id into string for session storing
        profile['_id'] = str(profile['_id'])
        if 'scholarships' in profile:
            for i in range(len(profile['scholarships'])):
                profile['scholarships'][i]['_id'] = str(profile['scholarships'][i]['_id'])
        
        return profile

def save_log(username, csv):
    """
    Description
    Saves milestone log as csv in database

    Parameters
    username:     TYPE: str
                  DESC: user's account username

    csv:          TYPE: csv
                  DESC: csv file of milestone logs

    Returns:      True if save was successful
                  False on failure
    """
    client = MongoClient(host=["mongodb://localhost:27017/"])
    db = client['FWA']
    users = db['users']

    #Checks if user is logged in
    profile = users.find_one({'username' : username})

    if profile == None:
        return False

    users.update_one({'username' : username},{'$set': {'logs':csv}})

    return True

def post_scholarship(sponsor, name, gpa, status, hours, desc, award):
    """
    Description  
    Uploads scholarship to the database

    Parameters
    sponsor:      TYPE: str
                  DESC: username of the sponsor

    name:         TYPE: str
                  DESC: name of the scholarship

    gpa:          TYPE: Float
                  DESC: grade point average on 4 point scale

    status:       TYPE: str
                  DESC: Required enrollment status for scholarship

    hours:        TYPE: Float
                  DESC: Required credit hours for scholarships

    desc:         TYPE: str
                  DESC: The scholarship's description and other requirements

    award:        TYPE: str
                  DESC: The award for the scholarship

    Returns:      The dictionary document that was inserted if posting was successful
                  False otherwise
    """
    client = MongoClient(host=["mongodb://localhost:27017/"])
    db = client['FWA']
    scholarships = db['scholarships']
    users = db['users']

    #If the scholarship already exists
    if scholarships.count_documents({'name' : name}):
        return False
    
    document = {'sponsor':sponsor, 'name':name, 'gpa':gpa, 'status':status, 'hours':hours, 'desc':desc, 'award':award}
    
    scholarships.insert_one(document)

    users.update_one({'username':sponsor},{'$push': {'scholarships': document}})

    if '_id' in document:
        document['_id'] = str(document['_id'])

    return document

def fetch_scholarships(profile):
    client = MongoClient(host=["mongodb://localhost:27017/"])
    db = client['FWA']
    scholarships = db['scholarships']

    #If the user isn't logged in give them all scholarships
    if profile == None:
        opportunities = list(scholarships.find())
        return opportunities
    
    else:
        gpa = profile['GPA']
        status = profile['Enrollment Status']
        hours = profile['Credit Hours']
        opportunities = list(scholarships.find({'gpa': {'$lte': gpa}, '$or':[{'status': {'$eq':status}}, {'status': {'$eq':'NP'}}], 'hours':{'$lte':hours}}))
        return opportunities

def edit_profile(gpa, status, hours, username):
    client = MongoClient(host=["mongodb://localhost:27017/"])
    db = client['FWA']
    users = db['users']
    users.update_one({'username':username},{'$set': {'GPA': gpa, 'Enrollment Status': status, 'Credit Hours': hours}})
    return

def load_scholarships():
    scholarships = scrape()
    client = MongoClient(host=["mongodb://localhost:27017/"])
    db = client['FWA']
    scholarships_col = db['scholarships']

    for opportunity in scholarships:
        if scholarships.count_documents({'name' : opportunity['name']}):
            scholarships.remove(opportunity)

    print(scholarships)
    scholarships_col.insert_many(scholarships)


if __name__ == '__main__':
    login_user('Admin', 'password123')