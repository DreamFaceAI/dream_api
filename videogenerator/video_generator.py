import requests
import logging
from utils import _check_param_null
from utils import _output_result
from utils import _get_file_size
from upload import _handle_large_video

API_PREFIX = "http://api.newportai.com/api/async/"


def _check_file_size(src_url, file_size, api_key):
    if file_size > 50 * 1024 * 1024:  # 50 MB in bytes
        logging.info("Source video exceeds 50 MB. Routing to a different API.")
        return _handle_large_video(src_url, api_key)
    else:
        return src_url


class VideoGenerator(object):
    def __init__(self, api_key, error_log_file):
        self._api_key = api_key
        logging.basicConfig(filename=error_log_file)

    def talking_face(self, src_video_url, audio_url, video_params):
        _check_param_null(src_video_url, audio_url, video_params)
        file_size = _get_file_size(src_video_url)
        video_url = _check_file_size(src_video_url, file_size, self._api_key)

        endpoint = "talking_face"

        response = requests.post(
            API_PREFIX + endpoint,
            json={"srcVideoUrl": video_url, "audioUrl": audio_url, "videoParams": video_params},
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self._api_key}
        )
        response.raise_for_status()
        result = _output_result(response)
        task_id = result.get("taskId")
        logging.info(f"Talking Face Task ID: {task_id}")
        return task_id
