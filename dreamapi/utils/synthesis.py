import logging
import time
from .utils import _validate_param
from .utils import _post_request

# Constants
API_URL = "https://api.newportai.com/api/getAsyncResult"
DEFAULT_TIMEOUT = 10  # Timeout for HTTP requests in seconds


class Synthesis(object):
    def __init__(self, api_key):
        self._api_key = api_key

    def get_async_result(self, task_id):
        """Fetches the result of an asynchronous task.

        Args:
            task_id (str): The unique identifier for the task.

        Returns:
            dict: The task result data.

        Raises:
            ValueError: If task_id is invalid.
            Exception: If the API request fails or returns an error.
        """
        _validate_param(task_id)

        payload = {"taskId": task_id}
        return _post_request(self, API_URL, payload, DEFAULT_TIMEOUT)

    def poll_task_result(self, task_id, interval=1, max_attempts=100):
        """Polls the status of an asynchronous task until completion or timeout.

        Args:
            task_id (str): The unique identifier for the task.
            interval (int, optional): Time in seconds between polling attempts. Default is 1.
            max_attempts (int, optional): Maximum number of polling attempts. Default is 100.

        Returns:
            dict: The task result data, or a timeout error message.

        Raises:
            Exception: If the task fails or polling exceeds maximum attempts.
        """
        _validate_param(task_id)

        attempts = 0

        while attempts < max_attempts:
            try:
                data = self.get_async_result(task_id)
                logging.info(f"Polling attempt {attempts + 1}: {data}")

                status = data.get("task", {}).get("status")

                if status == 3:
                    logging.info("Task completed successfully.")
                    return data
                elif status == 4:
                    logging.error("Task failed.")
                    return data

                logging.info("Task in progress. Retrying...")
                attempts += 1
                time.sleep(interval)
            except Exception as e:
                logging.error(f"Polling error: {e}")
                raise

        logging.error("Polling exceeded maximum attempts. Task may still be in progress.")
        return {"error": "Polling timeout"}
