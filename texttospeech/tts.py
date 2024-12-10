import requests
import logging
from utils import _check_param_null
from utils import _output_result

API_PREFIX = "https://api.newportai.com/api/async/"


class TextToSpeech(object):
    def __init__(self, api_key, error_log_file):
        self._api_key = api_key
        logging.basicConfig(filename=error_log_file)

    def voice_clone(self, voice_url):
        _check_param_null(voice_url)

        endpoint = "voice_clone"

        response = requests.post(
            API_PREFIX + endpoint,
            json={"voiceUrl": voice_url},
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self._api_key}
        )
        response.raise_for_status()
        result = _output_result(response)

        # Access the taskId from the returned data
        task_id = result.get("taskId")
        logging.info(f"Voice Clone Task ID: {task_id}")
        return task_id

    def tts_clone(self, clone_id, text):
        _check_param_null(clone_id, text)
        endpoint = "do_tts_clone"

        response = requests.post(
            API_PREFIX + endpoint,
            json={"cloneId": clone_id, "text": text},
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self._api_key}
        )
        response.raise_for_status()
        result = _output_result(response)

        # Access the taskId from the returned data
        task_id = result.get("taskId")
        logging.info(f"Voice Clone Task ID: {task_id}")
        return task_id

    def tts_common(self, audio_id, text):
        _check_param_null(audio_id, text)

        endpoint = "do_tts_common"

        response = requests.post(
            API_PREFIX + endpoint,
            json={"audioId": audio_id, "text": text},
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self._api_key}
        )
        response.raise_for_status()
        result = _output_result(response)

        # Access the taskId from the returned data
        task_id = result.get("taskId")
        logging.info(f"Voice Clone Task ID: {task_id}")
        return task_id

    def tts_pro(self, audio_id, text):
        _check_param_null(audio_id, text)

        endpoint = "do_tts_pro"

        response = requests.post(
            API_PREFIX + endpoint,
            json={"audioId": audio_id, 'text': text},
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self._api_key}
        )
        response.raise_for_status()
        result = _output_result(response)

        # Access the taskId from the returned data
        task_id = result.get("taskId")
        logging.info(f"Voice Clone Task ID: {task_id}")
        return task_id