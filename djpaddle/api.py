import requests

from . import settings


class APIException(Exception):
    pass


class APIError(Exception):
    pass


def api_request(method, uri, data=None, *args, **kwargs):
    payload = {
        "vendor_id": settings.DJPADDLE_VENDOR_ID,
        "vendor_auth_code": settings.DJPADDLE_API_KEY,
    }
    if data:
        payload.update(data)

    url = kwargs.pop("url", settings.DJPADDLE_API_BASE + uri)
    resp = requests.request(method, url, json=payload, *args, **kwargs)
    resp.raise_for_status()

    data = resp.json()

    if "error" in data:
        raise APIError(
            "API error code {code} - {message}".format(
                code=data["error"]["code"], message=data["error"]["message"]
            )
        )

    if "response" not in data:
        raise APIException('malformed API response. "response" missing.')

    return data["response"]


def retrieve(uri, data=None, *args, **kwargs):
    return api_request("get", uri, data, *args, **kwargs)
