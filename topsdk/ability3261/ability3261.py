from topsdk.client import TopApiClient, BaseRequest

class Ability3261:

    def __init__(self, client: TopApiClient):
        self._client = client

    """
        淘宝客-推广者-CPA活动执行明细
    """
    def taobao_tbk_dg_cpa_activity_detail(self, request: BaseRequest):
        return self._client.execute(request.get_api_name(), request.to_dict(), request.get_file_param_dict())
    """
        淘宝客-推广者-任务奖励效果报表
    """
    def taobao_tbk_dg_cpa_activity_report(self, request: BaseRequest):
        return self._client.execute(request.get_api_name(), request.to_dict(), request.get_file_param_dict())
