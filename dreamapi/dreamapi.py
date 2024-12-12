import logging
from .videogenerator.video_generator import VideoGenerator
from .texttospeech.tts import TextToSpeech
from .utils.synthesis import Synthesis
from dreamapi.utils.file_uploader import FileUploader


class DreamAPI(object):

    def __init__(self, api_key, error_log_file):
        if not api_key or not isinstance(api_key, str):
            raise ValueError("API key must be a non-empty string.")
        if not error_log_file or not isinstance(error_log_file, str):
            raise ValueError("Error log file path must be a non-empty string.")

        self._api_key = api_key
        self.error_log_file = error_log_file
        logging.basicConfig(filename=error_log_file,
                            level=logging.DEBUG,
                            format="%(asctime)s [%(levelname)s] %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.synthesis = Synthesis(self._api_key)
        self.text_to_speech = TextToSpeech(self._api_key)
        self.video_generator = VideoGenerator(self._api_key)

    def poll_task_result(self, task_id):
        try:
            return self.synthesis.poll_task_result(task_id)
        except Exception as e:
            logging.error(f"Error in poll_task_result: {e}")
            raise

    def talking_face_from_url(self, src_video_url, audio_url, video_params):
        try:
            return self.video_generator.talking_face(src_video_url, audio_url, video_params)
        except Exception as e:
            logging.error(f"Error in talking_face: {e}")
            raise

    def talking_face_from_file(self, src_video_url, src_audio_url, video_params):
        try:
            upload_video = FileUploader(src_video_url, self._api_key)
            video_url = upload_video.upload_file()
            upload_audio = FileUploader(src_audio_url, self._api_key)
            audio_url = upload_audio.upload_file()
            return self.video_generator.talking_face(video_url, audio_url, video_params)
        except Exception as e:
            logging.error(f"Error in talking_face: {e}")
            raise

    def voice_clone(self, voice_url):
        try:
            return self.text_to_speech.voice_clone(voice_url)
        except Exception as e:
            logging.error(f"Error in voice_clone: {e}")
            raise

    def tts_clone(self, clone_id, text):
        try:
            return self.text_to_speech.tts_clone(clone_id, text)
        except Exception as e:
            logging.error(f"Error in tts_clone: {e}")
            raise

    def tts_common(self, audio_id, text):
        try:
            return self.text_to_speech.tts_common(audio_id, text)
        except Exception as e:
            logging.error(f"Error in tts_common: {e}")
            raise

    def tts_pro(self, audio_id, text):
        try:
            return self.text_to_speech.tts_pro(audio_id, text)
        except Exception as e:
            logging.error(f"Error in tts_pro: {e}")
            raise
