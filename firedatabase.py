import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyDjrfvE8FPIq1Zu8gFzJChdz_y7hwcTf3E",
  "authDomain": "spse-adventure.firebaseapp.com",
  "databaseURL": "https://spse-adventure-default-rtdb.firebaseio.com",
  "projectId": "spse-adventure",
  "storageBucket": "spse-adventure.appspot.com",
  "messagingSenderId": "880192570755",
  "appId": "1:880192570755:web:ef31a8d4f721549754a2b6",
  "measurementId": "G-EF9NM3SH3Q"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# DONE
def push_data(data: list, id_key: str): 
    '''
    Pushes the data to the server
    '''
    db.child(id_key).set(data[-1])
  

def update_data(data: list, id_key: str):
    '''
    Updates the data on the server
    '''
    db.child(id_key).update(data)