from collections import OrderedDictfrom rest_framework.response import Responseres_code = {    'success': '10000',    'error': '10001'}res = {    'msg': '',    'data': '',    'rescode': res_code['success'],}class ResCode(tuple):    Success = '10000'    Error = '10001'    # 验证    TOKEN_NOT = '900001'    Token_Missing = '20001'    Token_Timed_Out = '20002'    Token_Invalid = '20003'    Login_Timed_Out = '20004'    # 授权    Access_Denied = '30001'class HttpResponse(Response):    status_code = 200    def __init__(self,success=True,data=None,rescode=res_code['success'],msg='',headers=None,count=0):        '''        rescode与success参数只需传入其中任意一个。传入success，则状态码为全局成功\错误状态码；传入rescode，为自定义错误状态码        :param rescode: 状态码        :param success: 是否成功        :param data: 输出数据        :param msg: 提示信息        '''        if self.status_code != 200:            success = False        if rescode != res_code['success']:            res['rescode'] = rescode            res['msg'] = msg if msg else '请求出错,请稍后再试！'        else:            if success:                res['rescode'] = res_code['success']                res['msg'] = msg if msg else '操作成功'            else:                res['rescode'] = res_code['error']                res['msg'] = msg if msg else '请求出错,请稍后再试！'        res['data'] = data        res['count'] = count        super().__init__(data=OrderedDict(res),headers=headers)from rest_framework.exceptions import APIExceptionclass HttpResponse1(APIException):    status_code = 200class HttpResponseBadRequest(HttpResponse):    status_code = 400class HttpResponseUnauthorized(HttpResponse):    status_code = 401class HttpResponseForbidden(HttpResponse):    status_code = 403class HttpResponseNotFound(HttpResponse):    status_code = 404class HttpResponseNotAllowed(HttpResponse):    status_code = 405class HttpResponseNotAcceptable(HttpResponse):    status_code = 406class HttpResponseException(HttpResponse):    status_code = 500http_response = {    200: HttpResponse,    400: HttpResponseBadRequest,    401: HttpResponseUnauthorized,    403: HttpResponseForbidden,    404: HttpResponseNotFound,    405: HttpResponseNotAllowed,    406: HttpResponseNotAcceptable,    500: HttpResponseException}