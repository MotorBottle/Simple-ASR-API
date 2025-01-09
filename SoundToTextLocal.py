#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# SoundToTextLocal: Convert WAV file to text using FunASR

import os
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
        )
        print("ASR model loaded successfully.")

    def recognize(self, audio_path):
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
                data, return_raw_text=True, is_final=True, sentence_timestamp=False
            )
            return result[0]["text"]

        except Exception as e:
            raise RuntimeError(f"Error processing audio file: {e}")


if __name__ == "__main__":
    import argparse

    # 设置命令行参数
    parser = argparse.ArgumentParser(description="Convert WAV file to text using FunASR.")
    parser.add_argument(
        "audio_path", type=str, help="Path to the input WAV file."
    )
    args = parser.parse_args()

    # 初始化 SoundToText 实例
    sound_to_text = SoundToText()

    # 识别音频
    try:
        text_result = sound_to_text.recognize(args.audio_path)
        print(f"Recognition Result:\n{text_result}")
    except Exception as e:
        print(f"Error: {e}")