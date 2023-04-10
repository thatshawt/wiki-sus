from hashlib import sha256
from google.cloud import storage
from flask_login import current_user
from flaskr.user import User
import base64
import json
from datetime import datetime

# TODO(Project 1): Implement Backend according to the requirements.
class Backend:

    def __init__(self):
        # Starts class instance with a Storage Client
        self.storage_client = storage.Client(project="snappy-premise-377919")

    def _get_content_bucket(self):
        # Function returns content bucket
        return self.storage_client.bucket("sus-wiki-content-bucket")

    def _get_userpass_bucket(self):
        # Function returns user/pass bucket
        return self.storage_client.bucket("sus-user-pass-bucket")

    def _get_unique30_folder_blob(self, post_title):
        return self._get_content_bucket().blob("unique30/" + post_title)

    def get_wiki_page(self, name):

        # Get content bucket object
        content_bucket = self._get_content_bucket()

        # Retrieves page from bucket
        page_blob = content_bucket.blob("pages/" + name)

        # If it does not exist return nothing
        if not page_blob.exists():
            return None

        page_content = None
        # Reads blob object content and writes it to page_content variable
        with page_blob.open('r') as f:
            page_content = f.read()

        return page_content

    def get_author(self, name):
        # Function for getting an author

        # Content Bucket instance
        content_bucket = self._get_content_bucket()

        # Retrieves blob by author
        author_blob = content_bucket.blob("author/" + name)

        # Nothing returned if it does not exist
        if not author_blob.exists():
            return None

        author_content = None

        # Reads content of blob
        with author_blob.open('r') as f:
            author_content = f.read()
        return author_content

    def get_all_page_names(self):

        # Initialize an empty list for the pages names
        names = []

        # For loop iterates through content bucket blob objects/pages
        for blob in self.storage_client.list_blobs(self._get_content_bucket(),
                                                   prefix="pages/"):

            # Appends them to the list
            name = blob.name[len("pages/"):]
            names.append(name)

        # List is returned
        return names

    #post_image is already in base64
    def upload(self, post_title, post_content, post_image):

        # Object from content bucket
        content_bucket = self._get_content_bucket()

        # Creates blob with the name and specific path
        the_blob = content_bucket.blob("pages/" + post_title)

        # Writes content to blob
        with the_blob.open('w') as f:
            f.write(post_content)

        # Object from image bucket
        image_bucket = self.storage_client.bucket('sus-wiki-images')

        # Create blob for image with specified name
        image_blob = image_bucket.blob(post_title)

        # Write image to blob (B64 FORMAT)
        with image_blob.open('wb') as f:
            f.write(post_image)

        # Creates author blob based on post title
        author_blob = content_bucket.blob("author/" + post_title)

        # Writes author username to blob
        with author_blob.open('w') as f:
            f.write(current_user.username)

        return post_title

    #Grab image from blob (already in b64)
    #return decoded image
    def get_image(self, image_name):

        # Object from images bucket
        bucket = self.storage_client.bucket('sus-wiki-images')

        # Blob with the specified image name
        blob = bucket.blob(image_name)
        image = None

        # Opens blob and reads the content from the image (Already in B64).
        # Content is written to image variable.
        with blob.open('rb') as f:
            image = f.read()

        # Image content returned in decoded format
        return image.decode('utf-8')

    #SIGN_UP BUCKET | username is not case sensitive
    def sign_up(self, username, password, sha256=sha256):

        # Check if username and password are valid characters.
        # If not, it will return.
        if not self._check_valid(username, password):
            return 'INVALID'

        # Object from user/pass bucket.
        bucket = self._get_userpass_bucket()

        # Blob object with the specified username
        blob = bucket.blob(username.lower())

        # Checks if blob/username already exists.
        # In case it does, it will return.
        if blob.exists():
            return 'ALREADY EXISTS'

        # Password is hashed (SHA256) with 'sus' prefix + password | password = 123 -> sus123
        # This hashed password is then written into the blob.
        with blob.open('w') as f:
            prefixed_password = ''.join(['sus', password])
            f.write(sha256(prefixed_password.encode()).hexdigest())

    def sign_in(self, username, password, sha256=sha256):  # Draft for SIGN IN

        # Object from user/pass bucket
        bucket = self._get_userpass_bucket()

        # Blob object from the specified username
        blob = bucket.blob(username.lower())

        # If user does not exist it will return.
        if not blob.exists():
            return False

        # Prefix (sus) will be added to the password enter by the user.
        # Password will then be hashed (SHA256)
        prefixed_password = ''.join(['sus', password])
        hashed_password = sha256(prefixed_password.encode()).hexdigest()
        password_matches = False

        # Open blob object and read its content. ( Hashed password )
        # Comparison between the entered password and one in record is made
        with blob.open('r') as f:
            user_password = f.read()
            if hashed_password == user_password:
                password_matches = True
                f.close()

        return password_matches  # Will True if password correct -- False if not

    def _check_valid(self, username, password):

        # Function will verify if the username or password are a-z / A-Z , 0-9
        # or accepted special characters or has no spaces

        # Length of username 5 characters or more.
        # Password 8 characters or more.
        if len(username) < 5 or len(password) < 8:
            return False

        # username is not cAsE SeNsITiVe
        # Backend will always make it lowercase
        username = username.lower()

        valid_username = False
        valid_password = False

        for character in username:
            ascii_value = ord(character)

            if (int(ascii_value) >= 48 and int(ascii_value) <= 57) or (
                    int(ascii_value) >= 97 and
                    int(ascii_value) <= 122):  # a-z , 0-9
                valid_username = True

            elif int(ascii_value) == 45 or int(
                    ascii_value) == 95:  # Dash or underscore ( '_', '-' )
                valid_username = True

            else:
                valid_username = False
                break

        for character in password:

            valid_password = False
            ascii_value = ord(character)

            if (int(ascii_value) >= 48 and int(ascii_value) <= 57) or (
                    int(ascii_value) >= 97 and
                    int(ascii_value) <= 122):  # a-z, 0-9
                valid_password = True

            elif (int(ascii_value) >= 65 and int(ascii_value) <= 90):  # A-Z
                valid_password = True

            elif (int(ascii_value) >= 33 and
                  int(ascii_value) <= 42):  # Some special characters
                valid_password = True

            elif int(ascii_value) == 45 or int(
                    ascii_value) == 95:  # Dash or underscore ( '_', '-' )
                valid_username = True

            else:
                valid_password = False
                break

        return valid_username and valid_password


    def create_message(self, message : str, sender_user : User, receiver_user : User):
        receiver_user.append_message(message, sender_user.username)
        
    def get_user_message_list(self, user: User) -> list :
        return user.get_message_list()

    # Function just for TESTING purposes
    def test(self):

        bucket = self.storage_client.bucket("sus-user-pass-bucket")

        lst = []
        for blob in bucket.list_blobs():

            if blob.name != 'admin':

                lst.append(blob.name)

        return lst

    def _visited_postpage(self, post_title, ip):
        page_visit = PageVisit(post_title, ip, datetime.now())
        blob = page_visit.save_blob(self)

class PageVisit:
    def __init__(self, post_title, ip, date):
        self.ip = ip
        self.date = date
        self.post_title = post_title

    # def prune(self):


    def _encode_to_json(self):
        the_data = {
            'post_title': self.post_title,
            'ip': self.ip,
            'date': self.date.isoformat(),
        }
        the_json = json.dumps(the_data)
        return the_json

    @staticmethod
    def decode_from_json(the_json):
        def page_visit_decoder(dct):
            return PageVisit(dct['post_title'], dct['ip'], datetime.fromisoformat(dct['date']))

        return json.loads(the_json, object_hook=page_visit_decoder)

    def save_blob(self, backend):
        content_bucket = backend._get_content_bucket()
        the_blob = content_bucket.blob("unique30/" + self.post_title + "/" + self.ip)
        with the_blob.open('w') as f:
            the_json = self._encode_to_json()
            f.write(the_json)

        return the_blob

    