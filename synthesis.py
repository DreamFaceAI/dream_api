import requests
import logging
import time
from utils import _check_param_null
from utils import _output_result

API_ENDPOINT = "http://api.newportai.com/api/getAsyncResult"


class Synthesis(object):
    def __init__(self, api_key, error_log_file):
        self._api_key = api_key
        logging.basicConfig(filename=error_log_file)

    def get_async_result(self, task_id):
        _check_param_null(task_id)

        response = requests.post(
            API_ENDPOINT,
            json={"taskId": task_id},
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self._api_key}
        )
        response.raise_for_status()
        data = _output_result(response)
        return data

    def poll_task_result(self, task_id, interval=1, max_attempts=100):
        attempts = 0

        while attempts < max_attempts:
            # 获取任务状态
            data = self.get_async_result(task_id)
            logging.info(f"Polling attempt {attempts + 1}: {data}")

            # 提取任务状态
            status = data.get("task", {}).get("status")

            # 检查状态
            if status == 3:
                logging.info("Task completed successfully.")
                return data  # 成功结果
            elif status == 4:
                logging.error("Task failed.")
                return data  # 失败结果

            # 状态为 "1" 或 "2"，继续轮询
            logging.info("Task in progress. Retrying...")
            attempts += 1
            time.sleep(interval)

        # 超过最大轮询次数，返回超时结果
        logging.error("Polling exceeded maximum attempts. Task may still be in progress.")
        return {"error": "Polling timeout"}
