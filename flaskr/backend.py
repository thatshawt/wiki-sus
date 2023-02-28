from hashlib import sha256
from google.cloud import storage


# TODO(Project 1): Implement Backend according to the requirements.
class Backend:

    def __init__(self):
        self.storage_client = storage.Client(project="snappy-premise-377919")
        
    def _get_content_bucket(self):
        return self.storage_client.bucket("sus-wiki-content-bucket")

    def _get_userpass_bucket(self):
        return self.storage_client.bucket("sus-user-pass-bucket")

    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self, wikiname, file):
        content_bucket = self._get_content_bucket()
        the_blob = content_bucket.blob("pages/" + wikiname)
        the_blob.upload_from_file(file)

    def sign_up(self, username, password): # DRAFT FOR SIGN_UP BUCKET | username NOT cASe sEnSiTiVe

        if not self._check_valid(username, password): # Check if username and password are valid characters
            print('INVALID')
            return 'INVALID'
        
        bucket = self._get_userpass_bucket()
        blob = bucket.blob(username.lower())

        if blob.exists():
            print('ALREADY EXISTS')
            return 'ALREADY EXISTS'
        
        with blob.open('w') as f:
            f.write(sha256(password.encode()).hexdigest())


    def sign_in(self, username, password): # Draft for SIGN IN
        
        bucket = self._get_userpass_bucket()
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



    def _check_valid(self, username, password): # DRAFT - Verify if the username or password are a-z / A-Z , 0-9 or accepted special characters or has no spaces

        if len(username) < 5 or len(password) < 8: # Length of username 5 characters or more | Password 8 or more
            return False

        username = username.lower()

        valid_username = False
        valid_password = False

        for character in username:
            ascii_value = ord(character)

            if (int(ascii_value) >= 48 and int(ascii_value) <= 57) or (int(ascii_value) >= 97 and int(ascii_value) <= 122): # a-z , 0-9
                valid_username = True

            elif int(ascii_value) == 45 or int(ascii_value) == 95: # Dash or underscore ( '_', '-' )
                valid_username = True

            else:
                valid_username = False
                break

        for character in password:

            valid_password = False
            ascii_value = ord(character)

            if (int(ascii_value) >= 48 and int(ascii_value) <= 57) or (int(ascii_value) >= 97 and int(ascii_value) <= 122): # a-z, 0-9
                valid_password = True

            elif (int(ascii_value) >= 65 and int(ascii_value) <= 90): # A-Z
                valid_password = True

            elif (int(ascii_value) >= 33 and int(ascii_value) <= 42): # Some special characters
                valid_password = True

            elif int(ascii_value) == 45 or int(ascii_value) == 95: # Dash or underscore ( '_', '-' )
                valid_username = True

            else:
                valid_password = False
                break
        

        return valid_username and valid_password

