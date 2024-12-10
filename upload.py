from io import BytesIO
from urllib.parse import urlsplit, urlunsplit

import requests
from utils import _check_param_null
from utils import _output_result

API_PREFIX = "https://api.newportai.com/api/file/v1/"


def remove_query_from_url(url):
    parsed_url = urlsplit(url)
    clean_url = urlunsplit((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', ''))
    return clean_url


def get_upload_policy(api_key):

    endpoint = "get_policy"

    response = requests.post(
        API_PREFIX + endpoint,
        json={"Enum": "Dream-CN"},
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}
    )
    response.raise_for_status()
    result = _output_result(response)
    return result


def upload(src_url, policy_result):

    url = "https://dreamapi-oss.oss-cn-hongkong.aliyuncs.com"

    access_id = policy_result.get("accessId")
    policy = policy_result.get("policy")
    signature = policy_result.get("signature")
    dir = policy_result.get("dir")
    callback = policy_result.get("callback")

    response = requests.get(src_url, stream=True)
    response.raise_for_status()

    file_content = BytesIO(response.content)
    file_content.name = src_url.split("/")[-1]

    files = {
        "policy": ("", policy),
        "OSSAccessKeyId": ("", access_id),
        "success_action_status": ("", "200"),
        "signature": ("", signature),
        "key": ("", dir + file_content.name),
        "callback": ("", callback),
        "file": (file_content.name, file_content, "application/octet-stream"),
    }

    response = requests.post(url, files=files)
    response.raise_for_status()
    result = _output_result(response)
    req_id = result.get("reqId")
    return req_id


def get_upload_result(req_id, api_key):

    endpoint = "policy_upload_finish"

    response = requests.post(
        API_PREFIX + endpoint,
        json={"reqId": req_id},
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}
    )
    response.raise_for_status()
    result = _output_result(response)
    url = result.get("url")
    clean_url = remove_query_from_url(url)
    return clean_url


def _handle_large_video(src_video_url, api_key):

    policy_result = get_upload_policy(api_key)
    _check_param_null(policy_result)

    req_id = upload(src_video_url, policy_result)
    _check_param_null(req_id)

    url = get_upload_result(req_id, api_key)
    _check_param_null(url)

    return url




