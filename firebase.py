import firebase_admin
from firebase_admin import credentials, storage, firestore
from array import *

# Import UUID4 to create token
from uuid import uuid4

#   Credentials for accessing admin sdk for the application
cred = credentials.Certificate('/root/PycharmProjects/sdk/notika-firebase-adminsdk.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'notika-a2c99.appspot.com'
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
new_token = uuid4()

#   create new dictionary with metadata
metadata = {"firebaseStorageDownloadTokens": new_token}

#   set metadata to blob
blob.metadata = metadata

#   upload file
blob.upload_from_filename(local_file, content_type='image/png')

#   get image url
blob.make_public()
url = blob.public_url

#   Data to be uploaded to firestore topic collection
class_name = input("Enter name of class to take the subject: ")
level = input("A-level / O-level : ")
subject = input("Enter name of subject: ")
topic_name = input("Enter name of topic: ")

#   uploading data to firestore topic collection
doc_ref = db.collection('Topic').document()
doc_ref.set({
    'subject': subject,
    'topic_name': topic_name,
    'level': level,
    'class_name': class_name,
    'image': url
})

#   getting document ref ID
doc_id = doc_ref.get()
ref_id = doc_id.id


#   uploading data to firestore sub_topic collection
n = int(input('Enter number of sub_topics: '))
for i in range(0, n):
    sub_topic_ref = db.collection('Sub_Topic').document()
    sub_topic_name = input('Enter name of sub_topic: ')
    sub_topic_ref.set({
        'topic_id': ref_id,
        'sub_topic_name': sub_topic_name
    })

    #   Upload a pdf file to storage
    local_file = input("Enter name of pdf file to be uploaded to storage: ")
    cloud_fileName = input("Enter name of the pdf file in the bucket: ")
    blob = bucket.blob('pdf/' + cloud_fileName + '.pdf')
    blob.upload_from_filename(local_file)

    #   create new token
    new_token = uuid4()

    #   create new dictionary with metadata
    metadata = {"firebaseStorageDownloadTokens": new_token}

    #   set metadata to blob
    blob.metadata = metadata

    #   upload file
    blob.upload_from_filename(local_file, content_type='application/pdf')

    #   get pdf url
    blob.make_public()
    pdf_url = blob.public_url

    #   sub_topic_pdf collection
    sub_topic_id = sub_topic_ref.get()
    ref_sub_topic_id = sub_topic_id.id
    sub_topic_pdf_ref = db.collection("Sub_Topic_Pdf").document()
    sub_topic_pdf_ref.set({
        'sub_topic_id': ref_sub_topic_id,
        'file': pdf_url,
        'pdf_name': sub_topic_name
    })



