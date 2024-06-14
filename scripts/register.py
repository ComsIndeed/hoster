import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK with your service account credentials
cred = credentials.Certificate("../private_keys/project-academic-weapon-firebase-adminsdk-irvv8-de78853ef1.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project-id.firebaseio.com'
})

# Get a reference to the database
ref = db.reference()

# Write data using the service account's permissions
ref.child('heartbeat').set({'timestamp': 1623456789})

