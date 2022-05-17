from aiohttp import ClientSession, request
from typing import List, Optional, Dict, Union


class DeepL:
    def __init__(self, apis: List):
        self.apis = apis

    async def translate(self, text: Union[str, List], target_lang: str, src_lang: Optional[str] = '') -> Dict:
        """
        Translate the text from one language to another.
        @param text: the text to be translated.
        @param target_lang: the target language.
        @param src_lang: Optional, the source language.
        @return: {'success': Bool, The status
                  'message': str, Returning Message.
                  'data': Union[Dict, None], Returning data dict, should be None if not success
                  }
                  Data Dict: {
                                'origin_text': str, Parameter text,
                                'origin_lang': str, Origin text language
                                                             which should be the param "detected_source_language"
                                                             in response, it reflects the value of
                                                             the src_lang when specified.
                                'target_text': str, The translated text.
                                'target_lang': str, Parameter target_lang.
                  }
        """
        url = 'https://api-free.deepl.com/v2/translate'
        try:
            api = await self.get_available_api("".join(text))
            if not api:
                return {'success': False, 'message': 'No API Available.\n没有可用的API。', 'data': None}
        except Exception as e:
            return {'success': False, 'message': e, 'data': None}

        data = {
            'auth_key': api,
            'target_lang': target_lang,
        }
        if src_lang:
            data['src_lang'] = src_lang
        if isinstance(text, list):
            url_param = "?text=" + "&text=".join(text)
        else:
            url_param = f"?text={text}"
        try:
            async with request("POST", url+url_param, data=data) as r:
                if r.status == 200:
                    resp = await r.json()
                    translation = resp.get("translations")
                    origin_text = "\n".join(text) if isinstance(text, list) else text
                    origin_lang = translation[0].get("detected_source_language")
                    target_text = "\n".join(i.get('text') for i in translation)
                    return {
                        'success': True,
                        'message': 'success',
                        'data': {
                            'origin_text': origin_text,
                            'origin_lang': origin_lang,
                            'target_text': target_text,
                            'target_lang': target_lang
                        }
                    }

                if r.status == 400:
                    return {'success': False, 'message': 'Bad Request.Please check error message and your '
                                                         'parameters.\n错误的请求。请检查错误消息和您的参数。', 'data': None}
                if r.status == 403:
                    return {'success': False, 'message': 'Authorization failed. Please supply a valid '
                                                         'api.\n授权失败。请提供有效的API参数。', 'data': None}
                if r.status in [413, 414]:
                    return {'success': False, 'message': 'The request size exceeds the limit.\n请求大小超过限制。', 'data': None}
                if r.status in [429, 529]:
                    return {'success': False, 'message': 'Too many requests. Please wait and resend your '
                                                         'request.\n请求太多。请稍候并重新发送您的请求。', 'data': None}
                if r.status == 456:
                    return {'success': False, 'message': 'Quota exceeded. The character limit has been '
                                                         'reached.\n超出配额。已达到字符数限制。', 'data': None}
                else:
                    return {'success': False, 'message': 'Unknown error.\n未知错误。', 'data': None}
        except Exception as e:
            return {'success': False, 'message': e, 'data': None}

    async def get_available_api(self, text: str) -> str:
        """
        Return the first available api.
        @param text: the text to be translated.
        @return: available api, returns '' if no api fits.
        """
        check_url = "https://api-free.deepl.com/v2/usage?auth_key="
        async with ClientSession() as session:
            for i in self.apis:
                async with session.post(check_url+i) as r:
                    resp = await r.json()
                    if r.status == 200:
                        if resp['character_count'] >= resp['character_limit']:
                            self.apis.remove(i)
                            continue
                        if resp['character_count'] + len(text) <= resp['character_limit']:
                            return i
        return ''
