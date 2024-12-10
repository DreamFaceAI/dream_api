import json
import logging
import requests


def _check_param_null(*args, **kwargs):
    """Check if arguments are valid."""
    for index, arg in enumerate(args):
        if arg is None or (isinstance(arg, str) and arg.strip() == ""):
            raise ValueError(f"Argument at position {index + 1} is required and cannot be empty")

    for key, value in kwargs.items():
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"Argument '{key}' is required and cannot be empty")


def _output_result(response):
    try:
        # Parse the JSON response
        result = response.json()
    except ValueError as e:
        logging.error("Failed to parse response as JSON.")
        raise ValueError("Invalid JSON response") from e

    # Check for success using "code" field
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
        raise ValueError("Unable to determine file size for the URL.")
    return int(content_length)

