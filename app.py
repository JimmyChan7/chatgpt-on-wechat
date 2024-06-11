# encoding:utf-8

import os
import signal
import sys
import time

from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.schedulers.blocking import BlockingScheduler

from bridge.context import Context
from bridge.reply import Reply, ReplyType
from channel import channel_factory
from channel.channel import Channel
from common import const
from config import load_config
from plugins import *
import threading

from lib import itchat
from taobao_bot_client import TaoBaoBotClient


def sigterm_handler_wrap(_signo):
    old_handler = signal.getsignal(_signo)

    def func(_signo, _stack_frame):
        logger.info("signal {} received, exiting...".format(_signo))
        conf().save_user_datas()
        if callable(old_handler):  #  check old_handler
            return old_handler(_signo, _stack_frame)
        sys.exit(0)

    signal.signal(_signo, func)


def start_channel(channel_name: str):

    channel = channel_factory.create_channel(channel_name)
    if channel_name in ["wx", "wxy", "terminal", "wechatmp", "wechatmp_service", "wechatcom_app", "wework",
                        const.FEISHU, const.DINGTALK]:
        PluginManager().load_plugins()

    if conf().get("use_linkai"):
        try:
            from common import linkai_client
            threading.Thread(target=linkai_client.start, args=(channel,)).start()
        except Exception as e:
            pass

    taoBaoBotClient = TaoBaoBotClient()
    scheduler = BackgroundScheduler()
    # 每隔 5 秒执行一次
    scheduler.add_job(auto_send_coupon, "interval", minutes=15,args=[taoBaoBotClient])
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    channel.startup()


def auto_send_coupon(taoBaoBotClient):
    print(f'请求淘宝物料发送')
    # 获取名字中含有特定字符的群聊，返回值为一个字典的列表
    group=itchat.search_chatrooms(name='美丽精致捡漏群')[0]
    group_name = group["UserName"]
    taoBaoBotClient.getRecommend(group_name)
    # itchat.send("请求淘宝物料发送",toUserName=group_name["UserName"])
    # if obj is not None:
    #     taoBaoBotClient.getRecommend()
    #     reply = Reply(ReplyType.TEXT, "请求淘宝物料发送")
    #     context = Context()
    #     # context["receiver"] = "我的助力群"
    #     context["receiver"] = group_name["UserName"]
    #     obj.send(reply,context)

def run():
    try:
        # load config
        load_config()
        # ctrl + c
        sigterm_handler_wrap(signal.SIGINT)
        # kill signal
        sigterm_handler_wrap(signal.SIGTERM)

        # create channel
        channel_name = conf().get("channel_type", "wx")

        if "--cmd" in sys.argv:
            channel_name = "terminal"

        if channel_name == "wxy":
            os.environ["WECHATY_LOG"] = "warn"

        start_channel(channel_name)

        while True:
            time.sleep(1)
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)


if __name__ == "__main__":
    run()
