import socket
from typing import Any
from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from app.common.logger import log
from app.common.response.state import State

# https://pro.ant.design/zh-CN/docs/request
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


def result(state: State, data: Any = {}, error_detail: Any = None) -> Response:
    trace_id = uuid4()
    host = socket.gethostbyname(socket.gethostname())

    # host = socket.gethostname()
    if 400 <= state.http_status < 500:
        log.warning(
            f"\nStatusCode:{state.http_status},ErrorCode:{state.error_code},ErrorMessage:{state.error_message},TraceId:{trace_id},Host:{host}"
        )
    if 500 <= state.http_status < 600:
        log.error(
            f"\nStatusCode:{state.http_status},ErrorCode:{state.error_code},ErrorMessage:{state.error_message},TraceId:{trace_id},Host:{host}"
        )
    return JSONResponse(
        status_code=state.http_status,
        content=jsonable_encoder(
            {
                "success": state.http_status == (200 or 201),
                "data": data,
                "errorCode": state.error_code,
                "errorMessage": state.error_message,
                "showType": state.show_type,
                "traceId": trace_id,
                "host": host,
                "errorDetail": error_detail,
            }
        ),
    )
