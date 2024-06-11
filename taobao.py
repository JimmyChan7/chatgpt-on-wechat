# encoding:utf-8
import json
import os
import random
import time
from common.log import logger
from common.taobao_common import del_pic, save_pic
from topsdk.ability375.request.taobao_tbk_tpwd_create_request import TaobaoTbkTpwdCreateRequest
from topsdk.client import TopApiClient
from topsdk.defaultability.defaultability import Defaultability
from topsdk.defaultability.request.taobao_tbk_dg_material_recommend_request import TaobaoTbkDgMaterialRecommendRequest


def get_full_path(directory, filename):
    # 使用 os.path.join 构建文件路径
    full_path = os.path.join(directory, filename)

    # 获取文件的绝对路径
    full_path = os.path.abspath(full_path)

    return full_path

def run():
    try:
        client = TopApiClient(appkey="34692808",app_sercet="3d381454e8a07d42cd66c5c20867b8ca",top_gateway_url="https://eco.taobao.com/router/rest")
        defaultability = Defaultability(client=client)
        # 87575 mac
        # 27798 家装
        # 86619  品牌券
        recommend_request = TaobaoTbkDgMaterialRecommendRequest(material_id="86619",adzone_id="115701900264",page_size=100)
        result = defaultability.taobao_tbk_dg_material_recommend(request=recommend_request)
        json_data = result['result_list']
        # print(result)
        for item in json_data:
                coupon_share_url = ""
                title = ""
                if str(item).find("coupon_share_url") > -1:
                    coupon_share_url = "https:" + item['publish_info']['coupon_share_url']
                    
                    pict_url = "https:" + str(item['item_basic_info']['pict_url'])
                    print(pict_url)
                    title = item['item_basic_info']['title']
                    item_id = item['item_id']
                    # filename = save_pic(pict_url, item_id)
                    zk_final_price = item['price_promotion_info']['zk_final_price']
                    final_promotion_price = item['price_promotion_info']['final_promotion_price']

                    # 发送图片
                    # itchat.send('@img@%s' % (f'''{filename}'''), group_name)
                    time.sleep(2)
                    print(f'''{title}\n【在售价】¥{zk_final_price}\n【券后价】¥{final_promotion_price}''')
                    
                    # itchat.send(f'''{title}\n【在售价】¥{zk_final_price}\n【券后价】¥{final_promotion_price}''', group_name)
                    time.sleep(random.randint(1, 3))
                    transform_request = TaobaoTbkTpwdCreateRequest(url=coupon_share_url)
                    
                    transform_result = client.execute(transform_request.get_api_name(), transform_request.to_dict(), transform_request.get_file_param_dict())
                    # print(transform_result)
                    transform_data = transform_result['data']
                    password_simple = transform_data['password_simple']
                    model = transform_data['model']
                    print(password_simple)
                    
                    # text = f'''{transform_result}'''
                    # start_index = text.find('￥')
                    # itchat.send(f'''({text[start_index: 13+start_index]})''', group_name)
                    time.sleep(2)
                    # del_pic(filename)
               
        while True:
            time.sleep(1)
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)



if __name__ == "__main__":
    run()
