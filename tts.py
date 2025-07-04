# coding=utf-8
import sys
import json

IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

API_KEY = '87LvwkSFbDeVjR3lYsnrNpLB'
SECRET_KEY = 'FRhqRcmPq0ArkcIcx8waZaAo2EwZqIun'

# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美 
DEFAULT_PER = 0
# 语速，取值0-15，默认为5中语速
DEFAULT_SPD = 5
# 音调，取值0-15，默认为5中语调
DEFAULT_PIT = 5
# 音量，取值0-9，默认为5中音量
DEFAULT_VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
DEFAULT_AUE = 3

FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}

CUID = "123456PYTHON"
TTS_URL = 'http://tsn.baidu.com/text2audio'


class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选


def fetch_token():
    print("fetch token begin")
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """


def text_to_speech(text, output_path, per=DEFAULT_PER, spd=DEFAULT_SPD, pit=DEFAULT_PIT, vol=DEFAULT_VOL, aue=DEFAULT_AUE):
    """
    Convert text to speech using Baidu TTS API
    
    Args:
        text (str): 要转换的文本
        output_path (str): 输出文件路径
        per (int): 发音人选择，0-4为基础音库，其他为精品音库，默认0
        spd (int): 语速，取值0-15，默认5
        pit (int): 音调，取值0-15，默认5
        vol (int): 音量，取值0-9，默认5
        aue (int): 音频格式，3:mp3 4:pcm-16k 5:pcm-8k 6:wav，默认3
    
    Returns:
        bool: 转换是否成功
    """
    try:
        token = fetch_token()
        tex = quote_plus(text)  # 此处TEXT需要两次urlencode
        print(f"Encoded text: {tex}")
        
        params = {'tok': token, 'tex': tex, 'per': per, 'spd': spd, 'pit': pit, 'vol': vol, 'aue': aue, 'cuid': CUID,
                  'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

        data = urlencode(params)
        print('Request URL: ' + TTS_URL + '?' + data)

        req = Request(TTS_URL, data.encode('utf-8'))
        has_error = False
        
        try:
            f = urlopen(req)
            result_str = f.read()

            headers = dict((name.lower(), value) for name, value in f.headers.items())
            has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
        except URLError as err:
            print('TTS http response http code : ' + str(err.code))
            result_str = err.read()
            has_error = True

        # 根据是否出错决定文件扩展名
        if has_error:
            save_file = output_path + "_error.txt"
        else:
            format_ext = FORMATS.get(aue, "mp3")
            # 如果用户提供的路径已有扩展名就使用，否则添加对应格式扩展名
            if '.' in output_path:
                save_file = output_path
            else:
                save_file = output_path + '.' + format_ext

        with open(save_file, 'wb') as of:
            of.write(result_str)

        if has_error:
            if (IS_PY3):
                result_str = str(result_str, 'utf-8')
            print("TTS API error:" + result_str)
            return False

        print(f"Speech synthesis successful. Result saved as: {save_file}")
        return True
        
    except Exception as e:
        print(f"Error during text-to-speech conversion: {str(e)}")
        return False


if __name__ == '__main__':
    # 示例用法
    test_text = "快的，迅速的"
    output_file = "cnresult/result.mp3"
    
    success = text_to_speech(test_text, output_file)
    if success:
        print("TTS conversion completed successfully!")
    else:
        print("TTS conversion failed!")
