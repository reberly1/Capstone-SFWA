from pymongo import MongoClient

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
    
    users.insert_one({'username':username,'password':password,'GPA':gpa,'Enrollment Status':status,"Credit Hours":hours,"logs":"Empty"})

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
        profile['_id'] = str(profile['_id'])
        return profile