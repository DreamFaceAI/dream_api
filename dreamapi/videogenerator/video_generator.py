import logging

from dreamapi.utils.utils import _validate_param
from dreamapi.utils.utils import _get_file_size
from dreamapi.utils.utils import _post_request
from dreamapi.utils.file_uploader import FileUploader

# Constants
API_PREFIX = "http://api.newportai.com/api/async/"
DEFAULT_TIMEOUT = 10  # Timeout for HTTP requests in seconds


def _check_file_size(src_url, file_size, api_key):
    if file_size > 50 * 1024 * 1024:  # 50 MB in bytes
        logging.info("Source video exceeds 50 MB. Routing to a different API.")
        upload = FileUploader(src_url, api_key)
        return upload.upload_file()
    else:
        return src_url


def _check_video_param(video_bitrate, video_width, video_height, video_enhance):
    params = {
        "video_bitrate": video_bitrate,
        "video_width": video_width,
        "video_height": video_height,
        "video_enhance": video_enhance
    }

    for param_name, value in params.items():
        if not isinstance(value, int):
            raise ValueError(f"Parameter '{param_name}' must be an integer. Got: {type(value).__name__}")


class VideoParam(object):
    def __init__(self, video_bitrate, video_width, video_height, video_enhance):
        _check_video_param(video_bitrate, video_width, video_height, video_enhance)
        self.video_bitrate = video_bitrate
        self.video_width = video_width
        self.video_height = video_height
        self.video_enhance = video_enhance

    def to_dict(self):
        return {
            "video_bitrate": self.video_bitrate,
            "video_width": self.video_width,
            "video_height": self.video_height,
            "video_enhance": self.video_enhance
        }


class VideoGenerator(object):
    """Handles video generation tasks using the API."""

    def __init__(self, api_key):
        """Initializes the VideoGenerator class.

        Args:
            api_key (str): The API key for authentication.

        Raises:
            ValueError: If api_key or error_log_file are invalid.
        """
        _validate_param(api_key)
        self._api_key = api_key

    def talking_face(self, src_video_url, src_audio_url, video_params):
        """
        Initiates a 'Talking Face' task.

        Args:
            src_video_url (str): The URL of the source video.
            audio_url (str): The URL of the audio file.
            video_params (dict): Additional parameters for video generation.

        Returns:
            str: The Task ID for the initiated task.

        Raises:
            ValueError: If any of the input parameters are invalid.
            requests.RequestException: If the HTTP request fails.
            Exception: If the API returns an error.
        """
        # Validate input parameters
        _validate_param(src_video_url, src_audio_url, video_params)

        # validate file size
        try:
            # Get and validate the file size
            file_size = _get_file_size(src_video_url)
            video_url = _check_file_size(src_video_url, file_size, self._api_key)
        except Exception as e:
            logging.error(f"Error validating video file size: {e}")
            raise

        # API endpoint for talking face
        endpoint = "talking_face"
        url = API_PREFIX + endpoint
        payload = {"srcVideoUrl": video_url, "audioUrl": src_audio_url, "videoParams": video_params}
        result = _post_request(self, url, payload, DEFAULT_TIMEOUT)
        task_id = result.get("taskId")
        if not task_id:
            logging.error("Task ID not found in the API response for talking face.")
            raise ValueError("Invalid response: Task ID missing.")
        logging.info(f"Talking Face Task ID: {task_id}")
        return task_id
