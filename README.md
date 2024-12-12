# DreamAPI Python SDK

The `DreamAPI` Python SDK provides tools for generating talking faces, voice cloning, and text-to-speech (TTS)
functionalities. The library is designed for seamless interaction with the NewportAI platform.

---

## Requirements

---

```
python > 3.0
requests
```

## Installation

---

```bash
pip install dream-api
```

## Initialization

```angular2html
from dreamapi import DreamAPI

api_key = "your_api_key"
log_file = "path/to/your_log_file"
dream_api = DreamApi(api_key, log_file)
```

## Method and Examples

1. Talking Face From URL

   Generates a talking face using video and audio provided via URLs.

   1. Use `talking_face_form_url` to get task_id with video and audio urls.
   ```
   from dreamapi import VideoParam
   
   video_param = VideoParam(video_bitrate, video_width, video_height, video_enhance).to_dict()
   # video_bitrate: When setting the bitrate, if it is set to 0, it means that the output video bitrate is not specified.
   # video_width: When setting the width, if it is set to 0, it means that the output video width is not specified.
   # video_height: Set the height, when set to 0, it means not to specify the output video height.
   # video_enhance: Whether it is oversampled or not: 0 - no, 1 - yes, default 0.
   
   audio_url = "your_audio_url"
   video_url = "your_video_url"
   task_id = dream_api.talking_face_from_url(video_url, audio_url, video_param)
   ```
   2. Use `poll_task_result` to get result
   ```
   result = dream_api.poll_task_result(task_id)
   print(result)
   ```
   result example:
   ```
   {'task': {'taskId': 'b0c46bc5fc7e4141a54fef63aaa76730', 'status': 3, 'reason': '', 'executionTime': 57128, 'taskType': 'talking_face'}, 'videos': [{'videoUrl': 'https://dreamface-resource-new.s3.amazonaws.com/server/aigc/file-transfer/2024-12-11/2bafeaadd9e040a49aa827bebfe5c93d.mp4', 'videoType': 'mp4'}]}
   ```

2. Talking Face From Local File

   Generates a talking face using video and audio provided via local files.

   1. Use `talking_face_form_file` to get task_id with video and audio files
   ```
   from dreamapi import VideoParam
   
   video_param = VideoParam(video_bitrate, video_width, video_height, video_enhance).to_dict()
   # video_bitrate: When setting the bitrate, if it is set to 0, it means that the output video bitrate is not specified.
   # video_width: When setting the width, if it is set to 0, it means that the output video width is not specified.
   # video_height: Set the height, when set to 0, it means not to specify the output video height.
   # video_enhance: Whether it is oversampled or not: 0 - no, 1 - yes, default 0.
   
   audio_url = "path/to/your_audio_file"
   video_url = "path/to/your_video_file"
   task_id = dream_api.talking_face_from_file(video_url, audio_url, video_param)
   ```

   2. Use `poll_task_result` to get result
   ```
   result = dream_api.poll_task_result(task_id)
   print(result)
   ```
   result example:
   ```
   {'task': {'taskId': 'b0c46bc5fc7e4141a54fef63aaa76730', 'status': 3, 'reason': '', 'executionTime': 57128, 'taskType': 'talking_face'}, 'videos': [{'videoUrl': 'https://dreamface-resource-new.s3.amazonaws.com/server/aigc/file-transfer/2024-12-11/2bafeaadd9e040a49aa827bebfe5c93d.mp4', 'videoType': 'mp4'}]}
   ```

3. Text To Speech Common version

   Generates speech using an existing audio template.

   1. Check `https://api.newportai.com/playground/speech` to get a common version audio_id.

   2. Use `tts_common` to get task_id with audio_id and text.
   ```
   audio_id = "51a47229e5244920b69f0da4746d61f6"
   text = "Today is a beautiful day."
   task_id = dream_api.tts_common(audio_id, text)
   ```
   3. Use `poll_task_result` to get result.
   ```
   result = dream_api.poll_task_result(task_id)
   print(result)
   ```
   result example:
   ```
   {"task": {"taskId": "9af2a0cee7734bbdabea229265d09869", "status": 3, "taskType": "tts_common"}, "audios": [{"audioUrl": "https://s3.amazonaws.com/pt-tts-new/oneshot_tts_result/20241113/_/4169774.wav", "audioType": ".wav"}]}}
   ```

4. Text To Speech PRO version

   Generates speech using an existing audio template.

   1. Check `https://api.newportai.com/playground/speech` to get a pro version audio_id.

   2. Use `tts_pro` to get task_id with audio_id and text.
   ```
   audio_id = "51a47229e5244920b69f0da4746d61f6"
   text = "Today is a beautiful day."
   task_id = dream_api.tts_pro(audio_id, text)
   ```
   3. Use `poll_task_result` to get result.
   ```
   result = dream_api.poll_task_result(task_id)
   print(result)
   ```
   result example:
   ```
   {"task": {"taskId": "4bbdabea229265d098699af2a0cee773", "status": 3, "taskType": "tts_pro"}, "audios": [{"audioUrl": "https://s3.amazonaws.com/pt-tts-new/oneshot_tts_result/20241113/_/743312.wav", "audioType": ".wav"}]}}
   ```

5. Text To Speech with Voice Clone

   Generates speech with cloning a target speaker's voice.

   1. Use `voice_clone` to get a cloneId with target voice URL.
   ```
   voice_url = "your_voice_url"
   task_id = dream_api.voice_clone(voice_url)
   ```
   2. Use `poll_task_result` to get clone_id.
   ```
   result = dream_api.poll_task_result(task_id)
   print(result)
   ```
   result example:
   ```
   {"task": {"taskId": "9265d098699af2a0cee7734bbdabea22", "status": 3, "taskType": "voice_clone"}, "cloneId": 40dc8e22ab179680ec5480f9fb32d1ec}}
   ```
   3. Use `tts_clone` to get tts_clone task_id with text and clone_id.
   ```
   text = "Today is a beautiful day."
   clone_id = 40dc8e22ab179680ec5480f9fb32d1ec
   task_id = dream_api.tts_clone(clone_id, text)
   ```
   4. Use `poll_task_result` to get result.
   ```
   result = dream_api.poll_task_result(task_id)
   print(result)
   ```
   result example:
   ```
   {"task": {"taskId": "9af2a0cee7734bbdabea229265d09869", "status": 3, "taskType": "tts_clone"}, "audios": [{"audioUrl": "https://s3.amazonaws.com/pt-tts-new/oneshot_tts_result/20241113/_/174332.wav", "audioType": ".wav"}]}}
   ```
   






