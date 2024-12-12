import os
from io import BytesIO
from urllib.parse import urlsplit, urlunsplit, urlparse

import requests
import logging
from .utils import _validate_param
from .utils import _output_result
from .utils import _post_request
from .utils import _is_url

API_PREFIX = "https://api.newportai.com/api/file/v1/"
DEFAULT_TIMEOUT = 10


def remove_query_from_url(url):
    """
    Removes the query parameters from a given URL.

    Args:
        url (str): The URL to clean.

    Returns:
        str: The cleaned URL without query parameters.
    """
    parsed_url = urlsplit(url)
    clean_url = urlunsplit((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', ''))
    return clean_url


def get_upload_policy(self):
    """
    Fetches the upload policy from the API.

    Returns:
        dict: The upload policy details from the API response.

    Raises:
        Exception: If the request fails or the response is invalid.
    """
    endpoint = "get_policy"
    url = API_PREFIX + endpoint
    payload = {"Enum": "Dream-CN"}
    logging.info("Fetching upload policy...")
    return _post_request(self, url, payload, DEFAULT_TIMEOUT)


def upload(self, policy_result):
    """
    Uploads a file to the remote storage using the provided policy.

    Args:
        policy_result (dict): The upload policy details.

    Returns:
        str: The request ID returned after a successful upload.

    Raises:
        Exception: If the upload fails or the response is invalid.
    """
    logging.info("Starting file upload...")
    url = "https://dreamapi-oss.oss-cn-hongkong.aliyuncs.com"
    try:
        # Extract policy details
        access_id = policy_result.get("accessId")
        policy = policy_result.get("policy")
        signature = policy_result.get("signature")
        dir_path = policy_result.get("dir")
        callback = policy_result.get("callback")

        if not all([access_id, policy, signature, dir_path, callback]):
            logging.error("Incomplete policy details provided.")
            raise ValueError("Incomplete policy details provided.")

        if _is_url(self._src_url):
            # Download the file from the source URL
            logging.info(f"Downloading file from: {self._src_url}")
            response = requests.get(self._src_url, stream=True, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            file_content = BytesIO(response.content)
            file_content.name = self._src_url.split("/")[-1]
        else:
            logging.info(f"Reading file from local path: {self._src_url}")
            if not os.path.isfile(self._src_url):
                logging.error("Local file not found.")
                raise FileNotFoundError(f"File not found: {self._src_url}")
            with open(self._src_url, "rb") as file:
                file_content = BytesIO(file.read())
            file_content.name = os.path.basename(self._src_url)

        # Prepare the upload payload
        files = {
            "policy": ("", policy),
            "OSSAccessKeyId": ("", access_id),
            "success_action_status": ("", "200"),
            "signature": ("", signature),
            "key": ("", dir_path + file_content.name),
            "callback": ("", callback),
            "file": (file_content.name, file_content, "application/octet-stream"),
        }

        # Upload the file
        logging.info(f"Uploading file to: {url}")
        upload_response = requests.post(url, files=files, timeout=300)
        upload_response.raise_for_status()
        logging.info("File upload successful.")
        return _output_result(upload_response).get("reqId")
    except requests.Timeout:
        logging.error("File upload request timed out.")
        raise TimeoutError("The request to upload the file timed out.")
    except Exception as e:
        logging.error(f"File upload failed: {e}")
        raise


def get_upload_result(self, req_id):
    """
    Fetches the upload result and cleans the returned URL.

    Args:
        req_id (str): The request ID for the upload.

    Returns:
        str: The cleaned URL of the uploaded file.

    Raises:
        Exception: If the request fails or the response is invalid.
    """
    endpoint = "policy_upload_finish"
    url = API_PREFIX + endpoint
    payload = {"reqId": req_id}
    logging.info("Fetching upload result...")
    result = _post_request(self, url, payload, DEFAULT_TIMEOUT)
    url = result.get("url")
    if not url:
        logging.error("url not found in the API response for get upload result.")
        raise ValueError("Invalid response: url missing.")
    clean_url = remove_query_from_url(url)
    logging.info(f"Talking Face Task ID: {clean_url}")
    return clean_url


class FileUploader(object):
    """
    Handles uploading and retrieving the URL of a large video.

    Args:
        src_url (str): The source URL of the video.
        api_key (str): The API key for authorization.

    Returns:
        str: The cleaned URL of the uploaded video.

    Raises:
        Exception: If any step in the process fails.
    """
    def __init__(self, src_url, api_key):
        _validate_param(api_key, src_url)
        self._src_url = src_url
        self._api_key = api_key

    def upload_file(self):
        try:
            # upload step 1
            policy_result = get_upload_policy(self)
            _validate_param(policy_result)
            # upload step 2
            req_id = upload(self, policy_result)
            _validate_param(req_id)
            # upload step 3
            return get_upload_result(self, req_id)
        except Exception as e:
            raise Exception(f"Failed to handle large video upload: {e}")




