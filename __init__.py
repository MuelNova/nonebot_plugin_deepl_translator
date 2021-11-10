from nonebot import get_driver, on_message
from nonebot.typing import T_State
from nonebot.rule import Rule
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment

from .config import Config
from .deepl import DeepL

global_config = get_driver().config
config = Config(**global_config.dict())

country_code = {"cn": "ZH", "jp": "JA", "en": "EN-US", "fr": "FR", "ru": "RU", "de": "DE", "es": "ES"}
DeepL = DeepL(config.api_keys)


# Rules
def isReplyTrans() -> Rule:
    async def _is_reply_trans(bot: Bot, event: Event, state: T_State) -> bool:
        if event.dict().get('reply'):
            msg = str(event.get_message()).strip().lower()
            for i in country_code:
                if i in msg:
                    return True
        return False

    return Rule(_is_reply_trans)


def isTransMsg() -> Rule:
    async def _is_trans_msg(bot: Bot, event: Event, state: T_State) -> bool:
        if not event.dict().get('reply'): # To prevent translating many times
            if str(event.get_message()).strip().lower()[:2] in country_code:
                return True
        return False
    return Rule(_is_trans_msg)


reply_trans = on_message(priority=1, rule=isReplyTrans(), block=True)
trans_msg = on_message(priority=1, rule=isTransMsg(), block=True)


@reply_trans.handle()
async def _(bot: Bot, event: Event, state: T_State):
    msg_dict = event.dict()
    reply_info = msg_dict['reply']
    raw_message = reply_info['message']
    msg_to_trans = [i.data['text'].strip().replace("\n", "") for i in raw_message if i.type == 'text']
    if len(msg_to_trans) == 1:
        msg_to_trans = msg_to_trans[0]
    resp = await DeepL.translate(msg_to_trans, country_code[str(event.get_message()).strip()])
    if resp['success']:
        message = MessageSegment.reply(id_=reply_info['message_id']) + resp['data']['target_text']
        await reply_trans.finish(message)
    else:
        await reply_trans.finish('出错了阿巴阿巴\n--------------\n' + resp['message'])


@trans_msg.handle()
async def _(bot: Bot, event: Event, state: T_State):
    msg_to_trans = [i.data['text'].strip() for i in event.dict()['message'] if i.type == 'text']
    countrycode = msg_to_trans[0][:2].lower()
    msg_to_trans[0] = msg_to_trans[0][2:]
    if len(msg_to_trans) == 1:
        msg_to_trans = msg_to_trans[0]
    resp = await DeepL.translate(msg_to_trans, country_code[countrycode])
    if resp['success']:
        message = MessageSegment.reply(id_=event.dict()['message_id']) + resp['data']['target_text']
        await reply_trans.finish(message)
    else:
        await reply_trans.finish('出错了阿巴阿巴\n--------------\n' + resp['message'])
