from typing import List
from topsdk.client import BaseRequest
from topsdk.util import convert_struct_list,convert_basic_list,convert_struct,convert_basic
from datetime import datetime


class TaobaoTbkDgCpaActivityDetailRequest(BaseRequest):

    def __init__(
        self,
        query_type: int = None,
        page_size: int = None,
        page_no: int = None,
        event_id: int = None,
        indicator_alias: str = None,
        start_id: int = None,
        runtime: datetime = None
    ):
        """
            明细类型，1：预估明细，2：结算明细
        """
        self._query_type = query_type
        """
            每页条数
        """
        self._page_size = page_size
        """
            页码
        """
        self._page_no = page_no
        """
            CPA活动ID
        """
        self._event_id = event_id
        """
            CPA活动奖励的统计口径，相关说明见文档：https://www.yuque.com/docs/share/7ecf8cf1-7f99-4633-a2ed-f9b6f8116af5?#
        """
        self._indicator_alias = indicator_alias
        """
            下一页开始查询的记录主键id
        """
        self._start_id = start_id
        """
            指定数据批次号(时间戳)
        """
        self._runtime = runtime

    @property
    def query_type(self):
        return self._query_type

    @query_type.setter
    def query_type(self, query_type):
        if isinstance(query_type, int):
            self._query_type = query_type
        else:
            raise TypeError("query_type must be int")

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        if isinstance(page_size, int):
            self._page_size = page_size
        else:
            raise TypeError("page_size must be int")

    @property
    def page_no(self):
        return self._page_no

    @page_no.setter
    def page_no(self, page_no):
        if isinstance(page_no, int):
            self._page_no = page_no
        else:
            raise TypeError("page_no must be int")

    @property
    def event_id(self):
        return self._event_id

    @event_id.setter
    def event_id(self, event_id):
        if isinstance(event_id, int):
            self._event_id = event_id
        else:
            raise TypeError("event_id must be int")

    @property
    def indicator_alias(self):
        return self._indicator_alias

    @indicator_alias.setter
    def indicator_alias(self, indicator_alias):
        if isinstance(indicator_alias, str):
            self._indicator_alias = indicator_alias
        else:
            raise TypeError("indicator_alias must be str")

    @property
    def start_id(self):
        return self._start_id

    @start_id.setter
    def start_id(self, start_id):
        if isinstance(start_id, int):
            self._start_id = start_id
        else:
            raise TypeError("start_id must be int")

    @property
    def runtime(self):
        return self._runtime

    @runtime.setter
    def runtime(self, runtime):
        if isinstance(runtime, datetime):
            self._runtime = runtime
        else:
            raise TypeError("runtime must be datetime")


    def get_api_name(self):
        return "taobao.tbk.dg.cpa.activity.detail"

    def to_dict(self):
        request_dict = {}
        if self._query_type is not None:
            request_dict["query_type"] = convert_basic(self._query_type)

        if self._page_size is not None:
            request_dict["page_size"] = convert_basic(self._page_size)

        if self._page_no is not None:
            request_dict["page_no"] = convert_basic(self._page_no)

        if self._event_id is not None:
            request_dict["event_id"] = convert_basic(self._event_id)

        if self._indicator_alias is not None:
            request_dict["indicator_alias"] = convert_basic(self._indicator_alias)

        if self._start_id is not None:
            request_dict["start_id"] = convert_basic(self._start_id)

        if self._runtime is not None:
            request_dict["runtime"] = convert_basic(self._runtime)

        return request_dict

    def get_file_param_dict(self):
        file_param_dict = {}
        return file_param_dict

