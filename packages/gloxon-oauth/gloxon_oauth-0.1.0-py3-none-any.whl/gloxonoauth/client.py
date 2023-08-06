import json
import urllib3


http = urllib3.PoolManager()


class Client:

    def __init__(self, appSecret, appKey):
        self.appSecret = appSecret
        self.appSecret = appSecret
        self.appKey = appKey
        self.baseURL = 'https://api.account.gloxoninc.com'

    def _post(self, url, params):
        headers = {"Content-Type": "application/json", "x-app-secret": self.appSecret, "x-app-key": self.appKey}
        params = json.dumps(params)
        response = http.request('POST', url, body=params, headers=headers)
        try:
            json_data = json.loads(response.data.decode('utf-8'))
        except Exception as e:
            return {"status": response.status, "data": {}, "success": False}
        return json_data

    def _get(self, url, token):
        headers = {
            "Content-Type": "application/json", "x-app-secret": self.appSecret, "x-app-key": self.appKey,
            "Authorization": f"Bearer {token}"
        }
        response = http.request('GET', url, headers=headers)
        try:
            json_data = json.loads(response.data.decode('utf-8'))
        except Exception as e:
            return {"status": response.status, "data": {}, "success": False}
        return json_data

    def exchangeAuthorizationCode(self, authorizationCode):
        """
        Exchanges the authentication code received with access token, use to get user information.
        """
        endpoint = "/api/v1/auth/token"
        url = f"{self.baseURL}{endpoint}"
        data = {"authorization_code": authorizationCode}
        response = self._post(url, data)
        return response

    def getUserInformation(self, token, publicId):
        endpoint = f"/api/v1/user/{publicId}"
        url = f"{self.baseURL}{endpoint}"
        response = self._get(url, token)
        return response

    def refreshUserToken(self, refreshToken):
        endpoint = "/api/v1/auth/token/refresh"
        url = f"{self.baseURL}{endpoint}"
        data = {"refresh_token": refreshToken}
        response = self._post(url, data)
        return response

