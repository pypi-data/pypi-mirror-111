import logging
import requests

from vc.libs.decoratos import response_builder
from .schema_base import HeadersSoldoBase, HeadersSoldo, JWTData


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequesterSoldoBase(object):
    default_authorize = HeadersSoldoBase
    advanced_authorize = HeadersSoldo
    auth2_data: JWTData

    @response_builder(data_schema=JWTData)
    def oauth_authorize(self):
        from vc.client.soldo.client import Soldo
        api_path = f'/oauth/authorize'
        response_data = self.request(
            api_path, method='post',
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"client_id": Soldo.settings.CLIENT_ID, "client_secret": Soldo.settings.CLIENT_SECRET})
        return response_data

    def request(
            self, path: str, method: str = "get", *,
            headers: dict = None,
            params: str = None, data: dict = None,
            json: dict = None,
            **kwargs):
        from vc.client.soldo.client import Soldo
        r = requests.request(url=Soldo.settings.API_URL + path, method=method, headers=headers, json=json, data=data, params=params, **kwargs)
        if r.status_code == 401 and "invalid_token" in r.text:
            response_data = self.oauth_authorize()
            Soldo.settings.ACCESS_TOKEN = response_data.data.access_token
            return self.request(path, method,  headers=self.default_authorize().dict(),
                                params=params, data=data, json=json)

        data = r.text
        try:
            data = r.json()
        except:
            pass
        finally:
            # fix long response
            if isinstance(data, str):
                data = data[:400]
        return data, r.status_code, r.url
