import requests
import time
import hmac
import hashlib
import json

class MagnusBillingAPI:
    def __init__(self, api_key, api_secret, public_url):
        self.api_key = api_key
        self.api_secret = api_secret
        self.public_url = public_url
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

        # Get module and action for URL construction
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


api = MagnusBillingAPI(api_key="your_key", api_secret="your_secret", public_url="https://yourapi.com")
response = api.query({"module": "some_module", "action": "some_action"})
print(response)
