import logging
from urllib.parse import urlparse

import requests


def _validate_param(*args, **kwargs):
    """Validates that no positional or keyword arguments are null or empty.

    Args:
        *args: Positional arguments to validate.
        **kwargs: Keyword arguments to validate.

    Raises:
        ValueError: If any argument is null or an empty string.
    """
    for index, arg in enumerate(args):
        if arg is None or (isinstance(arg, str) and arg.strip() == ""):
            raise ValueError(f"Argument at position {index + 1} is required and cannot be empty")

    for key, value in kwargs.items():
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"Argument '{key}' is required and cannot be empty")


def _is_url(path_or_url):
    """Check if the given path is a valid URL."""
    try:
        result = urlparse(path_or_url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def _output_result(response):
    """Processes the HTTP response and extracts the result.

    Args:
        response: The HTTP response object.

    Returns:
        dict: The parsed 'data' field from the response JSON.

    Raises:
        ValueError: If the response cannot be parsed as JSON.
        Exception: If the API returns an error code.
    """
    try:
        result = response.json()
    except ValueError as e:
        logging.error("Failed to parse response as JSON.")
        raise ValueError("Invalid JSON response") from e

    if result.get("code") == 0:
        logging.info("Request successful.")
        return result.get("data")  # Return the 'data' field for further use
    else:
        error_message = result.get("message", "Unknown error occurred")
        logging.error(f"API Error: {error_message}")
        raise Exception(f"API returned an error: {error_message}")


def _get_file_size(url):
    """
    Get the file size of a remote file without downloading it.

    :param url: The URL of the file
    :return: File size in bytes
    """
    response = requests.head(url)
    response.raise_for_status()
    content_length = response.headers.get("Content-Length")
    if content_length is None:
        return 1
    return int(content_length)


def _post_request(self, url, payload, timeout):
    """
    Helper method to send a POST request to the API.

    Args:
        url (str): The API url.
        payload (dict): The JSON payload to send in the request.

    Returns:
        dict: The parsed JSON response from the API.

    Raises:
        requests.RequestException: If the HTTP request fails.
        Exception: If the API response contains an error.
    """
    try:
        response = requests.post(
            url,
            json=payload,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._api_key}'
            },
            timeout=timeout  # Set a timeout for the request
        )
        response.raise_for_status()
        return _output_result(response)
    except requests.Timeout:
        logging.error(f"Request to {url} timed out.")
        raise TimeoutError(f"The request to {url} timed out.")
    except requests.RequestException as e:
        logging.error(f"HTTP request to {url} failed: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during request to {url}: {e}")
        raise
