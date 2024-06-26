# encoding:utf-8

import time




from bot.bot import Bot


from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from config import conf


from taobao_bot_client import TaoBaoBotClient

user_session = dict()


# OpenAI对话模型API (可用)
class TaobaoAPIBot(Bot):
    def __init__(self):
        super().__init__()
        

    def reply(self, query, context=None):
        # acquire reply content
        if context and context.type:
            if context.type == ContextType.TEXT:
                logger.info("[CLAUDE_API] query={}".format(query))
                # reply = None
                taoBaoBotClient = TaoBaoBotClient()
                reply_content = taoBaoBotClient.replyGoods(query)

                if len(reply_content)<=0:
                    reply = Reply(ReplyType.ERROR, "暂无查到商品")
                else:
                    reply = Reply(ReplyType.TEXT, reply_content)
                return reply
            elif context.type == ContextType.IMAGE_CREATE:
                ok, retstring = self.create_img(query, 0)
                reply = None
                if ok:
                    reply = Reply(ReplyType.IMAGE_URL, retstring)
                else:
                    reply = Reply(ReplyType.ERROR, retstring)
                return reply


