#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云TTS快速测试脚本
用于验证功能是否正常工作
"""

import os
import sys
from datetime import datetime

def check_dependencies():
    """检查依赖是否安装"""
    print("🔍 检查依赖...")
    
    try:
        import requests
        print("✅ requests 已安装")
    except ImportError:
        print("❌ requests 未安装，请运行: pip install requests")
        return False
    
    # 检查其他必要模块
    required_modules = ['json', 'base64', 'hashlib', 'hmac', 'time', 'urllib.parse', 'datetime']
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} 已安装")
        except ImportError:
            print(f"❌ {module} 未安装")
            return False
    
    return True


def check_config():
    """检查配置"""
    print("\n🔍 检查配置...")
    
    try:
        from config import ALIYUN_CONFIG
        
        access_key_id = ALIYUN_CONFIG["access_key_id"]
        access_key_secret = ALIYUN_CONFIG["access_key_secret"]
        
        # 检查配置文件
        if access_key_id == "your_access_key_id":
            # 尝试从环境变量获取
            access_key_id = os.getenv("ALIYUN_ACCESS_KEY_ID")
            access_key_secret = os.getenv("ALIYUN_ACCESS_KEY_SECRET")
            
            if access_key_id and access_key_secret:
                print("✅ 从环境变量获取到密钥")
                return True
            else:
                print("❌ 未配置阿里云密钥")
                print("请修改 config.py 或设置环境变量 ALIYUN_ACCESS_KEY_ID 和 ALIYUN_ACCESS_KEY_SECRET")
                return False
        else:
            print("✅ 从配置文件获取到密钥")
            return True
            
    except ImportError:
        print("❌ 无法导入配置文件 config.py")
        return False
    except Exception as e:
        print(f"❌ 配置检查出错: {e}")
        return False


def test_tts_basic():
    """基础TTS功能测试"""
    print("\n🧪 基础TTS功能测试...")
    
    try:
        from aliyun_tts import AliyunTTS
        from config import ALIYUN_CONFIG
        
        # 获取密钥
        access_key_id = ALIYUN_CONFIG["access_key_id"]
        access_key_secret = ALIYUN_CONFIG["access_key_secret"]
        
        if access_key_id == "your_access_key_id":
            access_key_id = os.getenv("ALIYUN_ACCESS_KEY_ID")
            access_key_secret = os.getenv("ALIYUN_ACCESS_KEY_SECRET")
        
        # 创建TTS客户端
        tts = AliyunTTS(access_key_id, access_key_secret)
        print("✅ TTS客户端创建成功")
        
        # 测试语音合成
        test_text = "这是阿里云TTS功能测试"
        print(f"🎵 测试文本: {test_text}")
        
        audio_data = tts.synthesize_speech(
            text=test_text,
            voice="xiaoyun",
            volume=50,
            speech_rate=0
        )
        
        if audio_data:
            print("✅ 语音合成成功")
            
            # 保存测试文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_file = f"test_tts_{timestamp}.mp3"
            
            with open(test_file, "wb") as f:
                f.write(audio_data)
            
            file_size = len(audio_data)
            print(f"✅ 测试文件已保存: {test_file}")
            print(f"📊 文件大小: {file_size} 字节")
            
            return True
        else:
            print("❌ 语音合成失败")
            return False
            
    except Exception as e:
        print(f"❌ TTS测试出错: {e}")
        return False


def test_simple_example():
    """简单示例测试"""
    print("\n🧪 简单示例功能测试...")
    
    try:
        from simple_tts_example import simple_text_to_mp3
        
        test_text = "简单示例功能测试"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"simple_test_{timestamp}.mp3"
        
        result = simple_text_to_mp3(
            text=test_text,
            output_file=output_file,
            voice="xiaoyun"
        )
        
        if result and os.path.exists(result):
            file_size = os.path.getsize(result)
            print(f"✅ 简单示例测试成功")
            print(f"📁 输出文件: {result}")
            print(f"📊 文件大小: {file_size} 字节")
            return True
        else:
            print("❌ 简单示例测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 简单示例测试出错: {e}")
        return False


def test_voice_list():
    """测试发音人列表"""
    print("\n🧪 发音人列表测试...")
    
    try:
        from config import VOICE_OPTIONS
        
        print(f"✅ 发音人列表加载成功，共 {len(VOICE_OPTIONS)} 个发音人")
        
        # 显示前5个发音人
        print("📢 部分发音人列表:")
        for i, (voice_id, description) in enumerate(list(VOICE_OPTIONS.items())[:5]):
            print(f"  {voice_id}: {description}")
        
        return True
        
    except Exception as e:
        print(f"❌ 发音人列表测试出错: {e}")
        return False


def cleanup_test_files():
    """清理测试文件"""
    print("\n🧹 清理测试文件...")
    
    test_files = []
    for file in os.listdir('.'):
        if file.startswith('test_tts_') or file.startswith('simple_test_'):
            test_files.append(file)
    
    if test_files:
        choice = input(f"发现 {len(test_files)} 个测试文件，是否删除？(y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            for file in test_files:
                try:
                    os.remove(file)
                    print(f"🗑️  已删除: {file}")
                except Exception as e:
                    print(f"❌ 删除失败 {file}: {e}")
        else:
            print("📁 测试文件已保留")
    else:
        print("📁 没有找到测试文件")


def main():
    """主测试函数"""
    print("🧪 阿里云TTS功能测试")
    print("=" * 50)
    
    all_passed = True
    
    # 1. 检查依赖
    if not check_dependencies():
        all_passed = False
    
    # 2. 检查配置
    if not check_config():
        all_passed = False
        print("\n❌ 配置检查失败，无法继续测试")
        return
    
    # 3. 测试基础TTS功能
    if not test_tts_basic():
        all_passed = False
    
    # 4. 测试简单示例
    if not test_simple_example():
        all_passed = False
    
    # 5. 测试发音人列表
    if not test_voice_list():
        all_passed = False
    
    # 总结
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！TTS功能正常工作")
        print("💡 现在可以使用以下命令开始正式使用:")
        print("   python simple_tts_example.py")
    else:
        print("❌ 部分测试失败，请检查配置和网络连接")
    
    # 清理测试文件
    cleanup_test_files()


if __name__ == "__main__":
    main() 