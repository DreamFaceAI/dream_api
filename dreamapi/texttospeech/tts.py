import logging
from dreamapi.utils.utils import _validate_param
from dreamapi.utils.utils import _post_request

API_PREFIX = "https://api.newportai.com/api/async/"
DEFAULT_TIMEOUT = 10  # Timeout for HTTP requests in seconds


class TextToSpeech(object):
    def __init__(self, api_key):
        self._api_key = api_key

    def voice_clone(self, voice_url):
        """
        Initiates a Voice Cloning task.

        Args:
            voice_url (str): The URL of the voice file.

        Returns:
            str: The Task ID of the initiated voice cloning task.
        """
        _validate_param(voice_url)
        endpoint = "voice_clone"
        url = API_PREFIX + endpoint
        payload = {"voiceUrl": voice_url}
        result = _post_request(self, url, payload, DEFAULT_TIMEOUT)
        task_id = result.get("taskId")
        if not task_id:
            logging.error("Task ID not found in the API response for voice cloning.")
            raise ValueError("Invalid response: Task ID missing.")
        logging.info(f"Voice Clone Task ID: {task_id}")
        return task_id

    def tts_clone(self, clone_id, text):
        """
        Performs Text-to-Speech using a cloned voice.

        Args:
            clone_id (str): The ID of the cloned voice.
            text (str): The text to be converted to speech.

        Returns:
            str: The Task ID of the TTS clone task.
        """
        _validate_param(clone_id, text)
        endpoint = "do_tts_clone"
        url = API_PREFIX + endpoint
        payload = {"cloneId": clone_id, "text": text}
        result = _post_request(self, url, payload, DEFAULT_TIMEOUT)
        task_id = result.get("taskId")
        if not task_id:
            logging.error("Task ID not found in the API response for TTS clone.")
            raise ValueError("Invalid response: Task ID missing.")
        logging.info(f"TTS Clone Task ID: {task_id}")
        return task_id

    def tts_common(self, audio_id, text):
        """
        Performs Text-to-Speech using a common voice.

        Args:
            audio_id (str): The audio ID for the common voice.
            text (str): The text to be converted to speech.

        Returns:
            str: The Task ID of the TTS common task.
        """
        _validate_param(audio_id, text)
        endpoint = "do_tts_common"
        url = API_PREFIX + endpoint
        payload = {"audioId": audio_id, "text": text}
        result = _post_request(self, url, payload, DEFAULT_TIMEOUT)
        task_id = result.get("taskId")
        if not task_id:
            logging.error("Task ID not found in the API response for TTS common.")
            raise ValueError("Invalid response: Task ID missing.")
        logging.info(f"TTS Common Task ID: {task_id}")
        return task_id

    def tts_pro(self, audio_id, text):
        """
        Performs Text-to-Speech using a professional voice.

        Args:
            audio_id (str): The audio ID for the professional voice.
            text (str): The text to be converted to speech.

        Returns:
            str: The Task ID of the TTS pro task.
        """
        _validate_param(audio_id, text)
        endpoint = "do_tts_pro"
        url = API_PREFIX + endpoint
        payload = {"audioId": audio_id, "text": text}
        result = _post_request(self, url, payload, DEFAULT_TIMEOUT)
        task_id = result.get("taskId")
        if not task_id:
            logging.error("Task ID not found in the API response for TTS pro.")
            raise ValueError("Invalid response: Task ID missing.")
        logging.info(f"TTS Pro Task ID: {task_id}")
        return task_id
