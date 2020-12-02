import firebase_admin
from firebase_admin import credentials, storage, firestore

# Import UUID4 to create token
from uuid import uuid4

#   Credentials for accessing admin sdk for the application
cred = credentials.Certificate('/root/PycharmProjects/sdk/notika-firebase-adminsdk.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'notika-e9b3a.appspot.com'
})

#   Creating a storage bucket
bucket = storage.bucket()

#   Creating a firestore object
db = firestore.client()

#   Upload a file to storage
local_file = input("Enter name of file to be uploaded to storage: ")
cloud_fileName = input("Enter name of the file in the bucket: ")
blob = bucket.blob('topics/' + cloud_fileName + '.jpg')
blob.upload_from_filename(local_file)

#   create new token
new_token  = uuid4()

#   create new dictionary with metadata
metadata = {"firebaseStorageDownloadTokens": new_token}

#   set metadata to blob
blob.metadata = metadata

#   upload file
blob.upload_from_filename(local_file, content_type='image/png')

#   get image url
url = blob.public_url

#   Data to be uploaded to firestore topic collection
subject = input("Enter name of subject: ")
topic_name = input("Enter name of topic: ")
level = input("A-level / O-level : ")
class_name = input("Enter name of class to take the subject: ")

#   uploading data to firestore
doc_ref = db.collection('Topic')
doc_ref.add({
    'subject': subject,
    'topic_name': topic_name,
    'level': level,
    'class_name': class_name,
    'image': url
})