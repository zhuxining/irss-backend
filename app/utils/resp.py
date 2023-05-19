import socket

from typing import Any
from uuid import UUID, uuid4

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from app.extensions.logger import logger

# export interface response {
#   success: boolean; // if request is success
#   data?: any; // response data
#   errorCode?: string; // code for errorType
#   errorMessage?: string; // message display to user
#   showType?: number; // error display type： 0 silent; 1 message.warn; 2 message.error; 4 notification; 9 page
#   traceId?: string; // Convenient for back-end Troubleshooting: unique request ID
#   host?: string; // onvenient for backend Troubleshooting: host of current access server
# }

# ErrorShowType {
#   SILENT = 0, // 不提示错误
#   WARN_MESSAGE = 1, // 警告信息提示
#   ERROR_MESSAGE = 2, // 错误信息提示
#   NOTIFICATION = 4, // 通知提示
#   REDIRECT = 9, // 页面跳转
# }


class Resp(Exception):
    resps = []

    def __init__(
        self,
        error_code: str,
        error_message: str,
        http_status: int,
        show_type: int,
    ):
        self.error_code = error_code
        self.error_message = error_message
        self.http_status = http_status
        self.show_type = show_type

        Resp.resps.append(self)

    def set_msg(self, error_message):
        self.error_message = error_message
        return self

    def __eq__(self, other):
        return self.http_status == other


Ok: Resp = Resp("0000", "Ok", status.HTTP_200_OK, 0)

InvalidRequest: Resp = Resp("4000", "无效请求", status.HTTP_400_BAD_REQUEST, 1)
ValidationError: Resp = Resp("4022", "参数验证错误", status.HTTP_422_UNPROCESSABLE_ENTITY, 1)
UnAthenticated: Resp = Resp("4001", "未验证身份", status.HTTP_401_UNAUTHORIZED, 9)
PermissionDenied: Resp = Resp("4003", "权限不足", status.HTTP_403_FORBIDDEN, 1)
NotFound: Resp = Resp("4004", "Not Found", status.HTTP_404_NOT_FOUND, 9)
AlreadyExists: Resp = Resp("4009", "已存在", status.HTTP_409_CONFLICT, 1)
ResourceExhausted: Resp = Resp("4029", "超出配额限制", status.HTTP_429_TOO_MANY_REQUESTS, 1)

ServerError: Resp = Resp("5000", "服务器开小差了", status.HTTP_500_INTERNAL_SERVER_ERROR, 1)
BadGateway: Resp = Resp("5002", "网关错误", status.HTTP_502_BAD_GATEWAY, 1)
ServiceUnavailable: Resp = Resp("5003", "服务器繁忙", status.HTTP_503_SERVICE_UNAVAILABLE, 1)
GatewayTimeout: Resp = Resp("5004", "网关超时", status.HTTP_504_GATEWAY_TIMEOUT, 1)
SqlFail: Resp = Resp("5100", "数据库执行失败", status.HTTP_500_INTERNAL_SERVER_ERROR, 1)

BusinessError: Resp = Resp("1000", "业务错误", status.HTTP_400_BAD_REQUEST, 1)
DataNotFound: Resp = Resp("1001", "未查询到", status.HTTP_400_BAD_REQUEST, 1)
DataStoreFail: Resp = Resp("1002", "新增失败", status.HTTP_400_BAD_REQUEST, 1)
DataUpdateFail: Resp = Resp("1003", "更新失败", status.HTTP_400_BAD_REQUEST, 1)
DataDestroyFail: Resp = Resp("1004", "删除失败", status.HTTP_400_BAD_REQUEST, 1)


def result(resp: Resp, data: Any = {}, error_detail: Any = None) -> Response:
    trace_id = uuid4()
    host = socket.gethostbyname(socket.gethostname())

    # host = socket.gethostname()
    if 400 <= resp.http_status < 500:
        logger.warning(
            f"\nstatus_code:{resp.http_status},errorCode:{resp.error_code},errorMessage:{resp.error_message},traceId:{trace_id},host:{host}"
        )
    if 500 <= resp.http_status < 600:
        logger.error(
            f"\nstatus_code:{resp.http_status},errorCode:{resp.error_code},errorMessage:{resp.error_message},traceId:{trace_id},host:{host}"
        )
    return JSONResponse(
        status_code=resp.http_status,
        content=jsonable_encoder(
            {
                "success": resp.http_status == 200 | 201,
                "data": data,
                "errorCode": resp.error_code,
                "errorMessage": resp.error_message,
                "showType": resp.show_type,
                "traceId": trace_id,
                "host": host,
                "errorDetail": error_detail,
            }
        ),
    )
