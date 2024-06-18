# server/api_client.py
import requests

class PackageTrackingAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.fedex.com/track/v1/"

    def get_package_status(self, tracking_number):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "trackingInfo": [
                {
                    "trackingNumberInfo": {
                        "trackingNumber": tracking_number
                    }
                }
            ]
        }
        response = requests.post(f"{self.base_url}track", json=data, headers=headers)
        return response.json()
