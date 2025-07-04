# 阿里云TTS文本转语音工具

这是一个使用阿里云TTS（Text-to-Speech）服务将文本转换为MP3音频文件的Python工具。

## 功能特性

- ✅ 支持中文文本转语音
- ✅ 多种发音人可选（男声、女声、童声、方言等）
- ✅ 可调节语速、音量、语调
- ✅ 支持批量转换
- ✅ 交互式转换模式
- ✅ 自动生成文件名
- ✅ 完整的错误处理

## 安装要求

### Python版本
- Python 3.6+

### 依赖包
```bash
pip install -r requirements.txt
```

或手动安装：
```bash
pip install requests
```

### 阿里云账号和密钥
1. 注册阿里云账号：https://www.aliyun.com/
2. 开通智能语音交互服务
3. 获取AccessKey ID和AccessKey Secret

## 快速开始

### 1. 配置密钥

**方法一：修改配置文件**
编辑 `config.py` 文件，将你的密钥信息填入：
```python
ALIYUN_CONFIG = {
    "access_key_id": "你的AccessKey ID",
    "access_key_secret": "你的AccessKey Secret",
    "region": "cn-shanghai",
}
```

**方法二：设置环境变量**
```bash
export ALIYUN_ACCESS_KEY_ID="你的AccessKey ID"
export ALIYUN_ACCESS_KEY_SECRET="你的AccessKey Secret"
```

### 2. 运行示例

**简单使用：**
```bash
python simple_tts_example.py
```

**完整示例：**
```bash
python aliyun_tts.py
```

## 使用方法

### 基础用法

```python
from aliyun_tts import AliyunTTS

# 创建TTS客户端
tts = AliyunTTS("你的access_key_id", "你的access_key_secret")

# 转换文本为MP3
success = tts.text_to_mp3(
    text="你好，这是测试文本",
    output_file="output.mp3",
    voice="xiaoyun"  # 发音人
)
```

### 高级用法

```python
# 自定义语音参数
success = tts.text_to_mp3(
    text="你好，这是测试文本",
    output_file="output.mp3",
    voice="xiaoyun",
    volume=80,        # 音量 (0-100)
    speech_rate=100,  # 语速 (-500到500)
    pitch_rate=50     # 语调 (-500到500)
)
```

### 批量转换

```python
from simple_tts_example import batch_text_to_mp3

texts = [
    "第一段文本",
    "第二段文本",
    "第三段文本"
]

results = batch_text_to_mp3(texts, "output_dir", "xiaoyun")
```

### 交互式转换

```python
from simple_tts_example import interactive_tts

interactive_tts()  # 启动交互式界面
```

## 发音人列表

### 常用中文发音人

| 发音人ID | 描述 | 性别 | 风格 |
|---------|------|------|------|
| xiaoyun | 小云 | 女 | 温和 |
| xiaogang | 小刚 | 男 | 标准 |
| xiaomeng | 小梦 | 女 | 甜美 |
| akira | 小明 | 男 | 标准 |
| xiaoli | 小丽 | 女 | 标准 |
| aixia | 艾夏 | 女 | 亲和 |
| aiqi | 艾琪 | 女 | 温暖 |
| aida | 艾达 | 女 | 成熟 |
| aiken | 艾柯 | 男 | 成熟 |
| xiaofeng | 小峰 | 男 | 朝气 |

### 方言发音人

| 发音人ID | 描述 | 方言类型 |
|---------|------|----------|
| guangxu | 广旭 | 粤语(男) |
| xiaowei | 小薇 | 粤语(女) |
| taozi | 桃子 | 四川话(女) |
| xiaosa | 小萨 | 东北话(女) |

### 特殊语音

| 发音人ID | 描述 | 特点 |
|---------|------|------|
| harry | 哈利 | 男童声 |
| nancy | 楠希 | 女童声 |

## 参数说明

### 语音合成参数

- **text**: 要合成的文本（必需）
- **voice**: 发音人ID（默认：xiaoyun）
- **format**: 音频格式（支持：mp3、wav、pcm）
- **sample_rate**: 采样率（8000或16000）
- **volume**: 音量（0-100）
- **speech_rate**: 语速（-500到500，0为正常语速）
- **pitch_rate**: 语调（-500到500，0为正常语调）

### 语速调节说明
- **-500到-1**: 慢速
- **0**: 正常语速
- **1到500**: 快速

### 语调调节说明
- **-500到-1**: 低音调
- **0**: 正常语调
- **1到500**: 高音调

## 文件结构

```
├── aliyun_tts.py           # 核心TTS类
├── config.py               # 配置文件
├── simple_tts_example.py   # 简单使用示例
├── requirements.txt        # 依赖包列表
├── README_TTS.md          # 使用说明
└── output_mp3/            # 默认输出目录
```

## 错误处理

### 常见错误及解决方案

1. **InvalidAccessKeyId**
   - 检查AccessKey ID是否正确
   - 确认密钥是否有效

2. **SignatureDoesNotMatch**
   - 检查AccessKey Secret是否正确
   - 确认时间同步

3. **InvalidParameter.Voice**
   - 检查发音人ID是否正确
   - 参考发音人列表选择正确的ID

4. **RequestTimeTooSkewed**
   - 检查系统时间是否正确
   - 同步系统时间

## 注意事项

1. **费用**: 阿里云TTS是付费服务，请注意使用量
2. **限制**: 每次请求的文本长度有限制（通常不超过300个字符）
3. **网络**: 需要稳定的网络连接
4. **密钥安全**: 请妥善保管你的AccessKey，不要泄露

## 服务开通

1. 登录阿里云控制台
2. 搜索"智能语音交互"
3. 开通语音合成服务
4. 创建项目并获取密钥

## 联系支持

如有问题，请参考：
- 阿里云TTS官方文档：https://help.aliyun.com/document_detail/84435.html
- 阿里云智能语音交互：https://ai.aliyun.com/nls

## 开源协议

本项目仅供学习和参考使用。 