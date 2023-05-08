from typing import Any
from pydantic import BaseModel


class ResponseModel(BaseModel):
    success: bool
    data: dict = {}
    errorCode: str = ""
    errorMessage: str = ""
    showType: int = 0
    traceId: str = ""
    host: str = ""


# export interface response {
#   success: boolean; // if request is success
#   data?: any; // response data
#   errorCode?: string; // code for errorType
#   errorMessage?: string; // message display to user
#   showType?: number; // error display type： 0 silent; 1 message.warn; 2 message.error; 4 notification; 9 page
#   traceId?: string; // Convenient for back-end Troubleshooting: unique request ID
#   host?: string; // onvenient for backend Troubleshooting: host of current access server
# }
