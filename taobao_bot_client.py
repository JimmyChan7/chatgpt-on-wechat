import io
import os
import random
import time

import requests

from common.taobao_common import save_pic, del_pic
from common.utils import fsize, compress_imgfile
from lib import itchat
from lib.itchat.utils import logger
from topsdk.ability375.request.taobao_tbk_tpwd_create_request import TaobaoTbkTpwdCreateRequest
from topsdk.client import TopApiClient
from topsdk.defaultability.defaultability import Defaultability
from topsdk.defaultability.request.taobao_tbk_dg_material_optional_upgrade_request import \
    TaobaoTbkDgMaterialOptionalUpgradeRequest
from topsdk.defaultability.request.taobao_tbk_dg_material_recommend_request import TaobaoTbkDgMaterialRecommendRequest


class TaoBaoBotClient():
    def __init__(self):
        self.client = TopApiClient(appkey="34692808",app_sercet="3d381454e8a07d42cd66c5c20867b8ca",top_gateway_url="https://eco.taobao.com/router/rest")
        self.current_page = 1
        self.page_size = 1

    def get_file_full_path(self,directory, filename):
        # 使用 os.path.join 构建文件路径
        full_path = os.path.join(directory, filename)

        # 获取文件的绝对路径
        full_path = os.path.abspath(full_path)

        return full_path
    #  品牌大额券物料id
    # 女装
    # 86623
    # 家居家装
    # 86622
    # 数码家电
    # 86621
    # 鞋包配饰
    # 86620
    # 美妆个护
    # 86619
    # 男装
    # 86618
    # 内衣
    # 86617
    # 母婴
    # 86616
    # 食品
    # 86614
    # 运动户外
    # 86615
    def getRecommend(self,group_name):
        try:
            defaultability = Defaultability(client=self.client)
            # 27798 家具家装
            # 27453 女装
            # 86619 美妆大额券
            recommend_request = TaobaoTbkDgMaterialRecommendRequest(material_id="86619", adzone_id="115701900264",
                                                                    page_size=self.page_size,page_no=self.current_page)
            result = defaultability.taobao_tbk_dg_material_recommend(request=recommend_request)
            json_data = result['result_list']
            self.current_page = self.current_page+1
            if len(json_data)<=0:
                result = defaultability.taobao_tbk_dg_material_recommend(request=recommend_request)
                json_data = result['result_list']
                self.current_page = self.current_page + 1

            if self.current_page>200:
                self.current_page = 1
            # print(result)
            self.sendGoods(json_data,group_name)

        except Exception as e:
            logger.exception(e)

    def getCustomSearch(self,group_name):
        try:
            defaultability = Defaultability(client=self.client)
            # 27798 家具家装
            # 27453 女装
            # 86619 美妆大额券
            # 50010788 分类 彩妆/香水/美妆工具
            # 50023282 分类 美发护发/假发
            # 50025705 分类 洗护清洁剂/卫生巾/纸/香薰
            # 1801 分类 美容护肤/美体/精油
            # 50023717 分类 保健用品
            # 126762001 分类 美容美体仪器
            # 50013864 分类 饰品/流行首饰/时尚饰品新
            # 16 分类 女装/女士精品
            # 50006843 分类 女鞋
            # cat = "50010788"
            # cat = "50010788,50023282,50025705,1801,50023717,50023717,126762001,50013864,16,50006843"
            request = TaobaoTbkDgMaterialOptionalUpgradeRequest(adzone_id="115701900264",
                                                                cat="50010788,50023282,1801,50023717,50023717,126762001,50013864,16,50006843",
                                                                sort="tk_total_sales", has_coupon=True,page_size=self.page_size,page_no=self.current_page)
            result = defaultability.taobao_tbk_dg_material_optional_upgrade(request=request)
            json_data = result['result_list']
            self.current_page = self.current_page+1
            if len(json_data)<=0:
                self.getCustomSearch(group_name)

            if self.current_page>400:
                self.current_page = 1
            # print(result)
            self.sendGoods(json_data,group_name)

        except Exception as e:
            logger.exception(e)

    def sendGoods(self,json_data,group_name):

        for item in json_data:
            coupon_share_url = ""
            title = ""
            if str(item).find("coupon_share_url") > -1:
                coupon_share_url = "https:" + item['publish_info']['coupon_share_url']

                if str(item['item_basic_info']['pict_url']).find("https:") == -1:
                    pict_url = "https:" + str(item['item_basic_info']['pict_url'])
                else:
                    pict_url = str(item['item_basic_info']['pict_url'])
                print(pict_url)
                title = item['item_basic_info']['title']
                item_id = item['item_id']
                # filename = save_pic(pict_url, item_id)
                zk_final_price = item['price_promotion_info']['zk_final_price']
                final_promotion_price = item['price_promotion_info']['final_promotion_price']
                try:
                    pic_res = requests.get(pict_url, stream=True)
                    image_storage = io.BytesIO()
                    for block in pic_res.iter_content(1024):
                        image_storage.write(block)
                    sz = fsize(image_storage)
                    if sz >= 40 * 1000:
                        logger.info("[wechat] image too large, ready to compress, sz={}".format(sz))
                        image_storage = compress_imgfile(image_storage, 40 * 1000 - 100)
                        logger.info("[wechat] image compressed, sz={}".format(fsize(image_storage)))
                    image_storage.seek(0)
                    print("发送图片")
                    itchat.send_image(image_storage, toUserName=group_name)
                except Exception as e:
                    logger.exception(e)

                time.sleep(2)
                print(f'''{title}\n【在售价】¥{zk_final_price}\n【领券到手价】¥{final_promotion_price}''')

                # itchat.send(f'''{title}\n【在售价】¥{zk_final_price}\n【领券到手价】¥{final_promotion_price}''', group_name)
                time.sleep(random.randint(1, 3))
                transform_request = TaobaoTbkTpwdCreateRequest(url=coupon_share_url)

                transform_result = self.client.execute(transform_request.get_api_name(), transform_request.to_dict(),
                                                       transform_request.get_file_param_dict())
                # print(transform_result)
                transform_data = transform_result['data']
                password_simple = transform_data['password_simple']
                model = transform_data['model']
                print(password_simple)
                itchat.send(
                    f'''{title}\n----------\n【在售价】¥{zk_final_price}\n【领券到手价】¥{final_promotion_price}\n---复制打开Tao寳-------\n1{password_simple}/:/''',
                    group_name)

                # text = f'''{transform_result}'''
                # start_index = text.find('￥')
                # itchat.send(f'''({text[start_index: 13+start_index]})''', group_name)
                time.sleep(2)
                # del_pic(filename)
    def replyGoods(self,queryKey):
        try:
            defaultability = Defaultability(client=self.client)

            request = TaobaoTbkDgMaterialOptionalUpgradeRequest(adzone_id="115701900264",
                                                                # cat="50010788,50023282,1801,50023717,50023717,126762001,50013864,16,50006843",
                                                                q=queryKey,
                                                                sort="tk_total_sales", has_coupon=True,page_size=3,page_no=1)
            result = defaultability.taobao_tbk_dg_material_optional_upgrade(request=request)
            json_data = result['result_list']
            self.current_page = self.current_page+1
            if len(json_data)<=0:
                return ""

            # print(result)
            return self.getReplyContent(json_data)

        except Exception as e:
            logger.exception(e)
            return ""

    def getReplyContent(self,json_data):
        content=""
        for item in json_data:
            coupon_share_url = ""
            title = ""
            if str(item).find("coupon_share_url") > -1:
                coupon_share_url = "https:" + item['publish_info']['coupon_share_url']

                if str(item['item_basic_info']['pict_url']).find("https:") == -1:
                    pict_url = "https:" + str(item['item_basic_info']['pict_url'])
                else:
                    pict_url = str(item['item_basic_info']['pict_url'])
                print(pict_url)
                title = item['item_basic_info']['title']
                item_id = item['item_id']
                # filename = save_pic(pict_url, item_id)
                zk_final_price = item['price_promotion_info']['zk_final_price']
                final_promotion_price = item['price_promotion_info']['final_promotion_price']

                time.sleep(2)
                print(f'''{title}\n【在售价】¥{zk_final_price}\n【领券到手价】¥{final_promotion_price}''')

                # itchat.send(f'''{title}\n【在售价】¥{zk_final_price}\n【领券到手价】¥{final_promotion_price}''', group_name)
                time.sleep(random.randint(1, 3))
                transform_request = TaobaoTbkTpwdCreateRequest(url=coupon_share_url)

                transform_result = self.client.execute(transform_request.get_api_name(), transform_request.to_dict(),
                                                       transform_request.get_file_param_dict())
                # print(transform_result)
                transform_data = transform_result['data']
                password_simple = transform_data['password_simple']
                model = transform_data['model']
                print(password_simple)

                content = content + f'''{pict_url}\n{title}\n----------\n【在售价】¥{zk_final_price}\n【领券到手价】¥{final_promotion_price}\n---复制打开Tao寳-------\n1{password_simple}/:/\n'''
        return content