from hashlib import sha256
from google.cloud import storage


# TODO(Project 1): Implement Backend according to the requirements.
class Backend:

    def __init__(self):
        self.storage_client = storage.Client()
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self):
        pass

    def sign_up(self, username, password): # DRAFT FOR SIGN_UP BUCKET

        bucket = self.storage_client.bucket('sus-user-pass-bucket')
        blob = bucket.blob(username.lower())

        if blob.exists():
            print('ALREADY EXISTS')
            return 'ALREADY EXISTS'
        
        with blob.open('w') as f:
            f.write(sha256(password.encode()).hexdigest())


    def sign_in(self, username, password): # Draft for SIGN IN
        
        bucket = self.storage_client.bucket('sus-user-pass-bucket')
        blob = bucket.blob(username.lower())

        if not blob.exists():
            print('USER DOES NOT EXIST')
            return 'USER DOES NOT EXIST'

        hashed_password = sha256(password.encode()).hexdigest()
        password_matches = False
        with blob.open('r') as f:
            user_password = f.read()
            if hashed_password == user_password:
                password_matches = True
        
        if not password_matches:
            print('INCORRECT PASSWORD')
            return 'INCORRECT PASSWORD'
        
        print('LOGGED IN')
        return 'LOGGED IN'

    def get_image(self):
        pass

