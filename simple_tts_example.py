#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的阿里云TTS使用示例
"""

import os
from datetime import datetime
from aliyun_tts import AliyunTTS
from config import ALIYUN_CONFIG, TTS_DEFAULT_PARAMS, VOICE_OPTIONS


def simple_text_to_mp3(text: str, output_file: str = None, voice: str = "xiaoyun"):
    """
    简单的文本转MP3函数
    
    Args:
        text: 要转换的文本
        output_file: 输出文件路径，如果不指定则自动生成
        voice: 发音人，默认为xiaoyun
    
    Returns:
        成功返回输出文件路径，失败返回None
    """
    # 从配置或环境变量获取密钥
    access_key_id = ALIYUN_CONFIG["access_key_id"]
    access_key_secret = ALIYUN_CONFIG["access_key_secret"]
    
    # 如果配置文件中是默认值，尝试从环境变量获取
    if access_key_id == "your_access_key_id":
        access_key_id = os.getenv("ALIYUN_ACCESS_KEY_ID")
        access_key_secret = os.getenv("ALIYUN_ACCESS_KEY_SECRET")
    
    if not access_key_id or not access_key_secret:
        print("❌ 请先配置阿里云访问密钥！")
        print("方法1: 修改 config.py 中的 ALIYUN_CONFIG")
        print("方法2: 设置环境变量 ALIYUN_ACCESS_KEY_ID 和 ALIYUN_ACCESS_KEY_SECRET")
        return None
    
    # 创建TTS客户端
    tts = AliyunTTS(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        region=ALIYUN_CONFIG["region"]
    )
    
    # 如果没有指定输出文件，自动生成文件名
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"tts_{timestamp}.mp3"
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 转换文本为MP3
    success = tts.text_to_mp3(
        text=text,
        output_file=output_file,
        voice=voice,
        **TTS_DEFAULT_PARAMS
    )
    
    if success:
        return output_file
    else:
        return None


def batch_text_to_mp3(texts: list, output_dir: str = "output", voice: str = "xiaoyun"):
    """
    批量转换文本为MP3
    
    Args:
        texts: 文本列表
        output_dir: 输出目录
        voice: 发音人
    
    Returns:
        成功转换的文件列表
    """
    successful_files = []
    
    for i, text in enumerate(texts, 1):
        output_file = os.path.join(output_dir, f"text_{i:03d}.mp3")
        print(f"\n🎵 正在转换第 {i} 个文本: {text[:30]}{'...' if len(text) > 30 else ''}")
        
        result = simple_text_to_mp3(text, output_file, voice)
        if result:
            successful_files.append(result)
            print(f"✅ 转换成功！")
        else:
            print(f"❌ 转换失败！")
    
    return successful_files


def interactive_tts():
    """交互式TTS转换"""
    print("🎵 阿里云TTS交互式转换工具")
    print("=" * 50)
    
    # 显示可用的发音人
    print("\n📢 可用的发音人:")
    for voice_id, description in list(VOICE_OPTIONS.items())[:10]:  # 显示前10个
        print(f"  {voice_id}: {description}")
    print("  ...")
    print(f"  (共 {len(VOICE_OPTIONS)} 个发音人可选)")
    
    while True:
        print("\n" + "-" * 50)
        
        # 输入文本
        text = input("请输入要转换的文本 (输入 'quit' 退出): ").strip()
        if text.lower() == 'quit':
            print("👋 再见！")
            break
        
        if not text:
            print("❌ 文本不能为空！")
            continue
        
        # 选择发音人
        voice = input(f"请输入发音人 (默认: {TTS_DEFAULT_PARAMS['voice']}): ").strip()
        if not voice:
            voice = TTS_DEFAULT_PARAMS['voice']
        
        if voice not in VOICE_OPTIONS:
            print(f"⚠️  发音人 '{voice}' 不在预设列表中，但仍会尝试使用")
        
        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"interactive_tts_{timestamp}.mp3"
        
        # 转换
        print(f"\n🎵 正在转换: {text}")
        print(f"🎙️  发音人: {voice} ({VOICE_OPTIONS.get(voice, '未知')})")
        
        result = simple_text_to_mp3(text, output_file, voice)
        if result:
            file_size = os.path.getsize(result)
            print(f"✅ 转换成功！")
            print(f"📁 文件位置: {result}")
            print(f"📊 文件大小: {file_size} 字节")
        else:
            print("❌ 转换失败！")


def main():
    """主函数"""
    print("🎵 阿里云TTS示例程序")
    print("=" * 50)
    
    # 示例1: 单个文本转换
    print("\n📝 示例1: 单个文本转换")
    text1 = "你好，这是阿里云文本转语音的简单示例。"
    result1 = simple_text_to_mp3(text1, "example1.mp3", "xiaoyun")
    if result1:
        print(f"✅ 示例1完成: {result1}")
    
    # 示例2: 批量转换
    print("\n📝 示例2: 批量文本转换")
    texts = [
        "今天天气真不错。",
        "学习Python编程很有趣。",
        "阿里云的TTS服务质量很高。"
    ]
    results = batch_text_to_mp3(texts, "batch_output", "xiaogang")
    print(f"✅ 批量转换完成，成功转换 {len(results)} 个文件")
    
    # 示例3: 交互式转换
    print("\n📝 示例3: 交互式转换")
    choice = input("是否要尝试交互式转换？(y/n): ").strip().lower()
    if choice == 'y' or choice == 'yes':
        interactive_tts()


if __name__ == "__main__":
    main() 