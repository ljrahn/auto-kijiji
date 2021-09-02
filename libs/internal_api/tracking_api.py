import requests
import json
import time

class TrackingAPI:
    """
    A class to make REST calls to the internal tracking API.
    :param base_url: The base url of the server
    """
    def __init__(self, base_url):
        self.base_url = f'{base_url}'
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    def get_tracking_objs(self, tracking_number=None):
        """
        :param tracking_number: optional tracking number. Specify for specific tracking obj
        :returns: list of tracking objs if tracking_number is None else return specific tracking obj
        """
        if tracking_number is None:
            response = requests.get(f'{self.base_url}/tracking', headers=self.headers)
        else:
            response = requests.get(f'{self.base_url}/tracking?tracking_number={tracking_number}', headers=self.headers)
        return response.json()

    def post_tracking_objs(self, body=None):
        """
        :param body: the payload as a dict consisting of tracking_number, address_from, address_to, tracking_status
        :returns: returns back the response from the rest api
        """
        response = requests.post(f'{self.base_url}/tracking', headers=self.headers, data=json.dumps(body))
         
        return response

    def put_tracking_objs(self, body=None):
        """
        :param body: the payload as a dict consisting of tracking_number, address_from, address_to, tracking_status
        :returns: returns back the response from the rest api
        """
        response = requests.put(f'{self.base_url}/tracking', headers=self.headers, data=json.dumps(body))
         
        return response

    def delete_tracking_objs(self, tracking_number=None):
        """
        :param tracking_number: tracking number to delete
        :returns: list of tracking objs if tracking_number is None else return specific tracking obj
        """
        response = requests.delete(f'{self.base_url}/tracking?tracking_number={tracking_number}', headers=self.headers)

        return response
