import logging
import requests

from .datatypes import RenderArchive, RenderRequest, RenderLog

LOGGER = logging.getLogger(__name__)


class Client:
    def __init__(self, backend_host, backend_port, backend_auth_token=None):
        self.backend_host = backend_host
        self.backend_port = backend_port
        self.backend_auth_token = backend_auth_token
        self.SERVER_API_URL = f'http://{backend_host}:{backend_port}/api'

    def create(self, data, api_endpoint='', specialSuffix=''):
        try:
            response = requests.post(self.SERVER_API_URL + api_endpoint + '/post' + specialSuffix, json=data)
        except requests.exceptions.ConnectionError:
            LOGGER.error('failed to connect to server %s', self.SERVER_API_URL)
            return

        return response

    def delete(self, uuid, api_endpoint=''):
        try:
            response = requests.delete(self.SERVER_API_URL + api_endpoint + '/delete/{}'.format(uuid))
        except requests.exceptions.ConnectionError:
            LOGGER.error('failed to connect to server %s', self.SERVER_API_URL)
            return

        return response

    def delete_all(self, api_endpoint=''):
        try:
            response = requests.delete(self.SERVER_API_URL + api_endpoint + '/delete')
        except requests.exceptions.ConnectionError:
            LOGGER.error('failed to connect to server %s', self.SERVER_API_URL)
            return

        if (not response) or (not response.json()) or (not response.json()['results']):
            return []

        return response.json()['results']

    def get(self, uuid, api_endpoint=''):
        try:
            response = requests.get(self.SERVER_API_URL + api_endpoint + '/get/{}'.format(uuid))
        except requests.exceptions.ConnectionError:
            LOGGER.error('failed to connect to server %s', self.SERVER_API_URL)
            return

        return response

    def get_all(self, api_endpoint=''):
        try:
            response = requests.get(self.SERVER_API_URL + api_endpoint + '/get')
        except requests.exceptions.ConnectionError:
            LOGGER.error('failed to connect to server %s', self.SERVER_API_URL)
            return

        if (not response) or (not response.json()) or (not response.json()['results']):
            return []

        return response.json()['results']

    def update(self, params, uuid, api_endpoint=''):
        try:
            response = requests.put(self.SERVER_API_URL + api_endpoint + '/put/{}'.format(uuid), params)
        except requests.exceptions.ConnectionError:
            LOGGER.error('failed to connect to server %s', self.SERVER_API_URL)
            return

        return response

    # End of Abstract Methods Section
    # Start of the General Methods Section

    def add_worker(self, uuid, data=None):
        response = self.create(data, '/worker', '/{}'.format(uuid))
        return response.json() if (response and response.json()) else None

    def delete_worker(self, uuid):
        response = self.delete(uuid, '/worker')
        return RenderLog.from_dict(response.json()) if (response and response.json()) else None

    def get_workers(self):
        response = self.get_all('/worker')
        return [(res if res else '') for res in response] if response else []

    def ping_server(self, data=None):
        try:
            response = requests.post(self.SERVER_API_URL + '/ping', json=data)
        except requests.exceptions.ConnectionError:
            LOGGER.error('failed to connect to server %s', self.SERVER_API_URL)
            return

        return response

    # End of the General Methods Section
    # Start of Queue Methods Section

    def create_request(self, data):
        response = self.create(data)
        return RenderRequest.from_dict(response.json()) if (response and response.json()) else None

    def delete_all_requests(self):
        response = self.delete_all()
        return [(RenderRequest.from_dict(res.json()) if (res and res.json()) else None) for res in
                response] if response else []

    def delete_request(self, uuid):
        response = self.delete(uuid)
        return RenderRequest.from_dict(response.json()) if (response and response.json()) else None

    def get_all_requests(self):
        response = self.get_all()
        return [(RenderRequest.from_dict(res) if res else None) for res in
                response] if response else []

    def get_request(self, uuid):
        response = self.get(uuid)
        return RenderRequest.from_dict(response.json()) if (response and response.json()) else None

    def update_request(self, params, uuid):
        response = self.update(params, uuid)
        return RenderRequest.from_dict(response.json()) if (response and response.json()) else None

    # End of Queue Methods Section
    # Start of Archives Methods Section

    def create_archive(self, data):
        response = self.create(data, '/archive')
        return RenderArchive.from_dict(response.json()) if (response and response.json()) else None

    def delete_all_archives(self):
        response = self.delete_all('/archive')
        return [(RenderArchive.from_dict(res) if res else None) for res in
                response] if response else []

    def delete_archive(self, uuid):
        response = self.delete(uuid, '/archive')
        return RenderRequest.from_dict(response.json()) if (response and response.json()) else None

    def get_all_archives(self, ):
        response = self.get_all('/archive')
        return [(RenderArchive.from_dict(res) if res else None) for res in
                response] if response else []

    def get_archive(self, uuid):
        response = self.get(uuid, '/archive')
        return RenderArchive.from_dict(response.json()) if (response and response.json()) else None

    def update_archive(self, params, uuid):
        response = self.update(params, uuid, '/archive')
        return RenderArchive.from_dict(response.json()) if (response and response.json()) else None

    # End of Archives Methods Section
    # Start of Logs Methods Section

    def create_log(self, data):
        response = self.create(data, '/logs')
        return RenderLog.from_dict(response.json()) if (response and response.json()) else None

    def delete_all_logs(self):
        response = self.delete_all('/logs')
        return [(RenderLog.from_dict(res) if res else None) for res in
                response] if response else []

    def delete_log(self, uuid):
        response = self.delete(uuid, '/logs')
        return RenderLog.from_dict(response.json()) if (response and response.json()) else None

    def get_all_logs(self):
        response = self.get_all('/logs')
        return [(RenderLog.from_dict(res.json()) if (res and res.json()) else None) for res in
                response] if response else []

    def get_log(self, uuid):
        response = self.get(uuid, '/logs')
        return RenderLog.from_dict(response.json()) if (response and response.json()) else None

    def update_log(self, params, uuid):
        response = self.update(params, uuid, '/logs')
        return RenderLog.from_dict(response.json()) if (response and response.json()) else None
