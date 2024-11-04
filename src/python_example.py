import requests
import time
import hmac
import hashlib
import json

class MagnusBilling:
    def __init__(self, api_key, api_secret, public_url):
        self.api_key = api_key
        self.api_secret = api_secret
        self.public_url = public_url
        self.filter = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/4.0 (compatible; MagnusBilling Python bot; Python)'
        })

    def query(self, req=None):
        if req is None:
            req = {}

        # Generate nonce
        mt = time.time()
        req['nonce'] = f"{int(mt)}{str(mt).split('.')[1][:6]}"

        # Generate POST data string
        post_data = "&".join(f"{key}={value}" for key, value in req.items())
        sign = hmac.new(
            self.api_secret.encode('utf-8'), 
            post_data.encode('utf-8'), 
            hashlib.sha512
        ).hexdigest()

        # Generate headers
        headers = {
            'Key': self.api_key,
            'Sign': sign
        }

        # Construct URL
        module = req.get('module')
        action = req.get('action')
        url = f"{self.public_url}/index.php/{module}/{action}"

        # Send POST request
        response = self.session.post(url, data=req, headers=headers, verify=False)

        # Check for response errors
        if response.status_code != 200:
            raise Exception(f"HTTP error: {response.status_code}")
        
        # Decode JSON response
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Response:", response.text)
            raise ValueError("Failed to parse JSON response")

    def create(self, module, data=None, action='save'):
        if data is None:
            data = {}
        data.update({
            'module': module,
            'action': action,
            'id': 0
        })
        return self.query(data)

    def update(self, module, id, data):
        data.update({
            'module': module,
            'action': 'save',
            'id': id
        })
        return self.query(data)

    def destroy(self, module, id):
        return self.query({
            'module': module,
            'action': 'destroy',
            'id': id
        })

    def read(self, module, page=1, action='read'):
        return self.query({
            'module': module,
            'action': action,
            'page': page,
            'start': 0 if page == 1 else (page - 1) * 25,
            'limit': 25,
            'filter': json.dumps(self.filter)
        })

    def buy_did(self, id_did, id_user):
        return self.query({
            'module': 'did',
            'action': 'buy',
            'id': id_did,
            'id_user': id_user
        })

    def spy_call(self, channel, sip_account, type):
        return self.query({
            'module': 'callOnLine',
            'action': 'spyCall',
            'channel': channel,
            'sipuser': sip_account,
            'type': type
        })

    def release_did(self, did):
        self.set_filter('did', did, 'eq', 'string')
        result = self.read('did')

        if 'rows' not in result or not result['rows']:
            return json.dumps({'error': f'DID {did} not exist'})

        self.clear_filter()
        return self.query({
            'module': 'did',
            'action': 'liberar',
            'ids': json.dumps([result['rows'][0]['id']])
        })

    def get_fields(self, module):
        return self.query({
            'module': module,
            'getFields': 1
        })

    def create_user(self, data):
        data.update({
            'module': 'user',
            'action': 'save',
            'createUser': 1,
            'id': 0
        })
        return self.query(data)

    def get_modules(self):
        return self.query({
            'getModules': 1
        })

    def get_menu(self, username):
        return self.query({
            'username': username,
            'getMenu': 1
        })

    def get_id(self, module, field, value):
        self.set_filter(field, value, 'eq')
        query = self.query({
            'module': module,
            'action': 'read',
            'page': 1,
            'start': 0,
            'limit': 1,
            'filter': json.dumps(self.filter)
        })

        self.clear_filter()

        if 'rows' in query and query['rows']:
            return query['rows'][0]['id']
        return None

    def clear_filter(self):
        self.filter = []

    def set_filter(self, field, value, comparison='st', type='string'):
        self.filter.append({
            'type': type,
            'field': field,
            'value': value,
            'comparison': comparison
        })



#EXAMPLES
# Initialize the API client with your credentials and public URL
api_key = "your_api_key"
api_secret = "your_api_secret"
public_url = "http://your_magnusBillingIP/mbilling/"  # Replace with your actual API URL

# Create an instance of the MagnusBilling class
api = MagnusBilling(api_key, api_secret, public_url)


############ READ ##############

# Define the module and other parameters
module_name = "user"  # Replace with the name of the module you want to read from, e.g., "user"
page = 1  # Page number for paginated results

# Read data from the specified module
try:
    response = api.read(module_name, page=page)
    print("Data retrieved successfully:", response)
except Exception as e:
    print("An error occurred:", e)


############ CREATE USER ##############
# Data for the new user
user_data = {
    'username' : 'the new username',
    'password': 'password',
    'active': '1',
    'firstname': 'my name', 
    'password' : 'new_password', 
    'email' : 'email',
    'id_group' : 3, #DEFAULT: GROUP IS USER
    'id_plan' : 1, #DEFAULT: GET THE FIRST PLAN THAT YOU SET TO USE IN SIGNUP      
    'credit' : 0, #DEFAULT: GET THE CREDIT FROM THE PLAN
    # Add other fields as required by the API
}

# Create a new user
try:
    response = api.create_user(user_data)
    print("User created successfully:", response)
except Exception as e:
    print("An error occurred:", e)



############ UPDATE USER ##############

# Define the module, user ID, and data to update
module_name = "user"  # The module where the user data is stored
user_id = 123  # Replace with the ID of the user you want to update

# Data with the new values to update
update_data = {
    "name": "Updated User Name",
    "email": "updateduser@example.com",
    # Add any other fields you want to update
}

# Call the update function to update the user
try:
    response = api.update(module_name, user_id, update_data)
    print("User updated successfully:", response)
except Exception as e:
    print("An error occurred:", e)



############ DELETE USER ##############
# Define the module and ID of the entry to delete
module_name = "user"  # The module from which you want to delete, e.g., "user"
entry_id = 123  # Replace with the ID of the entry you want to delete

# Call the destroy function to delete the entry
try:
    response = api.destroy(module_name, entry_id)
    print("Entry deleted successfully:", response)
except Exception as e:
    print("An error occurred:", e)



############ USE FILTERS  ##############
# Set a filter to find entries where 'credit' is greater than 10
field = "credit"
value = "10"
comparison = "gt"  # Comparison can be 'eq' (equal), 'lt' (less than), 'gt' (greater than), etc.
type = "numeric"  # Field type, e.g., 'string' or 'numeric'

# Use setFilter to apply the filter
api.set_filter(field, value, comparison, type)
# Now call the read function on the desired module, e.g., "user"
module_name = "user"  # Specify the module you want to read from
page = 1  # Define the page if pagination is required

# Read data from the specified module using the filter
try:
    response = api.read(module_name, page=page)
    print("Filtered data:", response)
except Exception as e:
    print("An error occurred:", e)

# Clear the filter if you want to remove it for future queries
api.clear_filter()

