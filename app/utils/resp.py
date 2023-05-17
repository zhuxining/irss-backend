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


class Resp(object):
    def __init__(
        self,
        errorCode: str,
        errorMessage: str,
        http_status: int,
        showType: int,
    ):
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        self.http_status = http_status
        self.showType = showType

    def set_msg(self, errorMessage):
        self.errorMessage = errorMessage
        return self


OK: Resp = Resp("0000", "ok", status.HTTP_200_OK, 0)
InvalidRequest: Resp = Resp("1000", "无效的请求", status.HTTP_400_BAD_REQUEST, 1)
InvalidParams: Resp = Resp("1002", "无效的参数", status.HTTP_400_BAD_REQUEST, 1)
BusinessError: Resp = Resp("1003", "业务错误", status.HTTP_400_BAD_REQUEST, 1)
DataNotFound: Resp = Resp("1004", "查询失败", status.HTTP_400_BAD_REQUEST, 1)
DataStoreFail: Resp = Resp("1005", "新增失败", status.HTTP_400_BAD_REQUEST, 1)
DataUpdateFail: Resp = Resp("1006", "更新失败", status.HTTP_400_BAD_REQUEST, 1)
DataDestroyFail: Resp = Resp("1007", "删除失败", status.HTTP_400_BAD_REQUEST, 1)
PermissionDenied: Resp = Resp("1008", "权限拒绝", status.HTTP_403_FORBIDDEN, 1)
ServerError: Resp = Resp("5000", "服务器繁忙", status.HTTP_500_INTERNAL_SERVER_ERROR, 1)


def result(
    resp: Resp,
    data: Any = {},
) -> Response:
    traceId = uuid4()
    host = socket.gethostbyname(socket.gethostname())
    # host = socket.gethostname()
    if 400 <= resp.http_status < 500:
        logger.warning(
            f"status_code:{resp.http_status},errorCode:{resp.errorCode},errorMessage:{resp.errorMessage},traceId:{traceId},host:{host}"
        )
    if 500 <= resp.http_status < 600:
        logger.error(
            f"status_code:{resp.http_status},errorCode:{resp.errorCode},errorMessage:{resp.errorMessage},traceId:{traceId},host:{host}"
        )
    return JSONResponse(
        status_code=resp.http_status,
        content=jsonable_encoder(
            {
                "success": resp.http_status == 200,
                "data": data,
                "errorCode": resp.errorCode,
                "errorMessage": resp.errorMessage,
                "showType": resp.showType,
                "traceId": traceId,
                "host": host,
            }
        ),
    )
