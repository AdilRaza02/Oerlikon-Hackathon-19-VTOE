import firebase_admin
from firebase_admin import credentials, firestore
# from firebase_admin import db

cred = credentials.Certificate("./serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Stream all document
docs = db.collection('Quotes').stream()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

# Get a single document
doc_3jWXivLkrOhXxG1ROylb = db.collection('Quotes').document('3jWXivLkrOhXxG1ROylb').get()
print(doc_3jWXivLkrOhXxG1ROylb.to_dict())

# Set a single document
doc_ref = db.collection('Quotes').document('q1')
doc_ref.set({
    'quote': 'Hello World',
    'author': 'Shubham'
})

# Update a document
doc_ref = db.collection('Quotes').document('q1')
doc_ref.update({
    'quote': "Hello World! 'sup?",
    'author': 'Shubham'
})