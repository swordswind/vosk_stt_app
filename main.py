import json
import os
import wave
from threading import Thread
from tkinter import scrolledtext
import vosk
import pyaudio
import numpy as np
import tkinter as tk


def speech_to_text():
    global result
    CHUNK = 1024  # 录音参数配置，指定每次读取音频数据的大小
    FORMAT = pyaudio.paInt16  # 音频格式
    CHANNELS = 1  # 声道数
    RATE = 16000  # 采样率
    p = pyaudio.PyAudio()  # 创建PyAudio对象
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)  # 打开音频输入流
    notice("正在录音...安静2秒后自动结束")
    frames = []  # 存储音频数据
    silent_count = 0  # 静音计数器，用于判断是否结束录音
    while True:  # 持续录音，直到检测到2秒钟内没有声音
        data = stream.read(CHUNK)  # 从音频输入流中读取数据
        frames.append(data)  # 将数据添加到frames列表中
        audio_data = np.frombuffer(data, dtype=np.int16)  # 将二进制数据转换为numpy数组
        rms = np.sqrt(np.mean(np.square(audio_data)))  # 计算音量大小（RMS）
        if rms < 2000:  # 判断是否静音
            silent_count += 1
        else:
            silent_count = 0
        if silent_count > 2 * RATE / CHUNK:  # 如果持续2秒钟（40分贝以下），则停止录音
            break
    notice("录音结束,正在转文字,请稍后...")
    stream.stop_stream()  # 关闭音频输入流
    stream.close()
    p.terminate()  # 关闭PyAudio对象
    filename = "cache/record.wav"  # 保存录音文件的路径和文件名
    wf = wave.open(filename, 'wb')  # 创建一个Wave_write对象，用于写入音频数据
    wf.setnchannels(CHANNELS)  # 设置声道数
    wf.setsampwidth(p.get_sample_size(FORMAT))  # 设置采样宽度
    wf.setframerate(RATE)  # 设置采样率
    wf.writeframes(b''.join(frames))  # 将音频数据写入文件
    wf.close()  # 关闭文件
    model_path = "model/vosk-model-small-cn-0.22"  # vosk模型文件的路径
    sample_rate = 16000  # 样本采样率
    if not os.path.exists(model_path):  # 检查模型文件是否存在
        notice(f"模型路径 {model_path} 不存在，请确保已下载正确的模型文件.")
        return
    model = vosk.Model(model_path)  # 加载vosk模型
    recognizer = vosk.KaldiRecognizer(model, sample_rate)  # 创建识别器对象
    wf = wave.open(filename, 'rb')  # 打开录音文件
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":  # 检查录音文件格式是否符合要求
        notice("录音文件格式不符合要求.")
        return
    recognizer.SetWords(True)  # 设置识别器输出结果中包含单词信息
    while True:
        data = wf.readframes(4000)  # 一次读取4000个字节的音频数据
        if len(data) == 0:  # 音频数据已全部读取完毕
            break
        if recognizer.AcceptWaveform(data):  # 将音频数据传入识别器进行识别
            result = recognizer.Result()  # 获取识别结果
    try:
        result_json = json.loads(result)  # 将字符串转换为JSON对象
        result_text = result_json["text"].replace(" ", "")  # 提取"text"中的文字并去掉空格
        notice("录音已成功转文字")
    except:
        result_text = ""
        notice("录音转文字失败，请重试")
    return result_text


def notice(info):
    state_box.delete("1.0", tk.END)  # 清空状态框
    state_box.insert(tk.END, info)  # 在状态框中插入新的状态信息


def run():
    def run_th():
        output = speech_to_text()
        output_box.insert(tk.END, output)  # 在输出框中显示转换后的文本
        output_box.see(tk.END)  # 滚动到末尾

    Thread(target=run_th).start()


root = tk.Tk()  # 创建一个Tkinter窗口
root.title("基于vosk的本地轻量化语音识别程序")  # 设置窗口标题
root.geometry("640x360")  # 设置窗口大小
root.option_add('*Font', '宋体 15')  # 设置字体
label = tk.Label(root, text="基于vosk的本地轻量化语音识别程序", font=("宋体", 20))  # 创建标签，显示程序标题
label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)  # 设置标签位置和大小
output_box = scrolledtext.ScrolledText(root, width=60, height=11)  # 创建滚动文本框，用于显示转换后的文本
output_box.grid(row=1, column=0, padx=10, pady=10, columnspan=2)  # 设置文本框位置和大小
state_box = tk.Text(root, width=30, height=1)  # 创建文本框，用于显示程序状态信息
state_box.grid(row=2, column=0, padx=10, pady=10)  # 设置文本框位置和大小
state_box.insert(tk.END, "点击右侧按钮开始录音")  # 在文本框中插入初始状态信息
record_button = tk.Button(root, text="点击录音", command=run)  # 创建按钮，用于开始录音
record_button.grid(row=2, column=1, padx=10, pady=10)  # 设置按钮位置和大小
root.mainloop()  # 进入主循环，等待事件发生
