import socket
from typing import Any
from uuid import UUID, uuid4

from fastapi import status as http_status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

# export interface response {
#   success: boolean; // if request is success
#   data?: any; // response data
#   errorCode?: string; // code for errorType
#   errorMessage?: string; // message display to user
#   showType?: number; // error display type： 0 silent; 1 message.warn; 2 message.error; 4 notification; 9 page
#   traceId?: string; // Convenient for back-end Troubleshooting: unique request ID
#   host?: string; // onvenient for backend Troubleshooting: host of current access server
# }


class Resp(object):
    def __init__(self, errorCode: int, errorMessage: str, code: int, showType: int):
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        self.code = code
        self.showType = showType
        self.traceId = Field(default_factory=uuid4)
        self.host = (socket.gethostname(),)

    def set_msg(self, msg):
        self.msg = msg
        return self


InvalidRequest: Resp = Resp(1000, "无效的请求", http_status.HTTP_400_BAD_REQUEST, 1)
InvalidParams: Resp = Resp(1002, "无效的参数", http_status.HTTP_400_BAD_REQUEST, 1)
BusinessError: Resp = Resp(1003, "业务错误", http_status.HTTP_400_BAD_REQUEST, 1)
DataNotFound: Resp = Resp(1004, "查询失败", http_status.HTTP_400_BAD_REQUEST, 1)
DataStoreFail: Resp = Resp(1005, "新增失败", http_status.HTTP_400_BAD_REQUEST, 1)
DataUpdateFail: Resp = Resp(1006, "更新失败", http_status.HTTP_400_BAD_REQUEST, 1)
DataDestroyFail: Resp = Resp(1007, "删除失败", http_status.HTTP_400_BAD_REQUEST, 1)
PermissionDenied: Resp = Resp(1008, "权限拒绝", http_status.HTTP_403_FORBIDDEN, 1)
ServerError: Resp = Resp(5000, "服务器繁忙", http_status.HTTP_500_INTERNAL_SERVER_ERROR, 1)


def success(
    success: bool,
    data: Any = {},
    errorCode: str = "",
    errorMessage: str = "",
    showType: int = 0,
    traceId: UUID = Field(default_factory=uuid4),
    # host: str = socket.gethostbyname(socket.gethostname()),
    host: str = socket.gethostname(),
) -> Response:
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                "success": True,
                "data": data,
                "errorCode": errorCode,
                "errorMessage": errorMessage,
                "showType": showType,
                "traceId": traceId,
                "host": host,
            }
        ),
    )


def fail(resp: Resp) -> Response:
    return JSONResponse(
        status_code=resp.code,
        content=jsonable_encoder(
            {
                "success": False,
                "data": {},
                "errorCode": resp.errorCode,
                "errorMessage": resp.errorMessage,
                "showType": resp.showType,
                "traceId": resp.traceId,
                "host": resp.host,
            }
        ),
    )
