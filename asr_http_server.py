#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# ASR HTTP Server using Flask

import os
from flask import Flask, request, jsonify
import torch
import librosa
from funasr import AutoModel
from trans_utils import convert_pcm_to_float


class SoundToText:
    def __init__(self):
        # 自动检测设备
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

        # 加载模型
        self.model = AutoModel(
            model="iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
            vad_model="damo/speech_fsmn_vad_zh-cn-16k-common-pytorch",
            punc_model="damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
            device=device,
            disable_update=True
        )
        print("ASR model loaded successfully.")

    def recognize(self, audio_path, hotwords):
        try:
            # 检查音频文件是否存在
            if not os.path.isfile(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

            # 加载音频文件
            data, sr = librosa.load(audio_path, sr=None, mono=True)
            data = convert_pcm_to_float(data)

            # 重采样到 16kHz
            if sr != 16000:
                data = torch.tensor(data, dtype=torch.float32)
                resampler = torch.nn.Sequential(torch.nn.Upsample(scale_factor=16000 / sr))
                data = resampler(data).numpy()

            # 进行语音识别
            result = self.model.generate(
                data, 
                return_raw_text=True, 
                is_final=True, 
                sentence_timestamp=False,
                hotword=hotwords  # Pass the hotwords as a string to the model
            )
            return result[0]["text"]

        except Exception as e:
            raise RuntimeError(f"Error processing audio file: {e}")


# 创建 Flask 应用
app = Flask(__name__)

# 初始化 SoundToText 实例
sound_to_text = SoundToText()


@app.route('/asr', methods=['POST'])
def recognize_audio():
    """
    Receive an audio file from the client and return the transcribed text.
    """
    try:
        # Get the uploaded audio file
        audio_file = request.files.get('audio')
        if not audio_file:
            return jsonify({"error": "No audio file provided"}), 400

        # Get hotwords from request if provided
        hotwords = request.form.get('hotwords', "")  # hotwords should be a string like 'word1 word2'

        # Save the audio file to a temporary location
        temp_path = "temp_audio.wav"
        audio_file.save(temp_path)

        # Call SoundToText for recognition, passing hotwords
        result = sound_to_text.recognize(temp_path, hotwords=hotwords)

        # Delete the temporary file
        os.remove(temp_path)

        # Return the recognition result
        return jsonify({"text": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Start Flask server and listen for requests from any host
    app.run(host='0.0.0.0', port=7869, debug=False)