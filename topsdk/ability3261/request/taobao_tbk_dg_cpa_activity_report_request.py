from typing import List
from topsdk.client import BaseRequest
from topsdk.util import convert_struct_list,convert_basic_list,convert_struct,convert_basic
from datetime import datetime


class TaobaoTbkDgCpaActivityReportRequest(BaseRequest):

    def __init__(
        self,
        event_id: int = None,
        biz_date: str = None,
        page_no: int = None,
        query_type: int = None,
        page_size: int = None,
        pid: str = None,
        relation_id: int = None
    ):
        """
            CPA活动ID，详见https://www.yuque.com/docs/share/16905f3f-3a22-4e7c-b8c3-4d23791d42f7?#
        """
        self._event_id = event_id
        """
            日期(yyyyMMdd)
        """
        self._biz_date = biz_date
        """
            分页页数，从1开始
        """
        self._page_no = page_no
        """
            数据类型：数据类型:1预估 2结算 （选择1可查询含当天实时预估统计的累计数据，选择2可查询最晚截止昨天结算的累计数据，具体逻辑以活动规则描述为准；）
        """
        self._query_type = query_type
        """
            分页大小
        """
        self._page_size = page_size
        """
            媒体三段式id（如果传入pid则返回pid汇总数据，不传则返回member维度统计数据，pid和relationid不可同时传入）
        """
        self._pid = pid
        """
            代理id（如果传入rid则返回rid统计数据，不传则返回member维度统计数据）
        """
        self._relation_id = relation_id

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
    def biz_date(self):
        return self._biz_date

    @biz_date.setter
    def biz_date(self, biz_date):
        if isinstance(biz_date, str):
            self._biz_date = biz_date
        else:
            raise TypeError("biz_date must be str")

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
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, pid):
        if isinstance(pid, str):
            self._pid = pid
        else:
            raise TypeError("pid must be str")

    @property
    def relation_id(self):
        return self._relation_id

    @relation_id.setter
    def relation_id(self, relation_id):
        if isinstance(relation_id, int):
            self._relation_id = relation_id
        else:
            raise TypeError("relation_id must be int")


    def get_api_name(self):
        return "taobao.tbk.dg.cpa.activity.report"

    def to_dict(self):
        request_dict = {}
        if self._event_id is not None:
            request_dict["event_id"] = convert_basic(self._event_id)

        if self._biz_date is not None:
            request_dict["biz_date"] = convert_basic(self._biz_date)

        if self._page_no is not None:
            request_dict["page_no"] = convert_basic(self._page_no)

        if self._query_type is not None:
            request_dict["query_type"] = convert_basic(self._query_type)

        if self._page_size is not None:
            request_dict["page_size"] = convert_basic(self._page_size)

        if self._pid is not None:
            request_dict["pid"] = convert_basic(self._pid)

        if self._relation_id is not None:
            request_dict["relation_id"] = convert_basic(self._relation_id)

        return request_dict

    def get_file_param_dict(self):
        file_param_dict = {}
        return file_param_dict

