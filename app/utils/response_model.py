import socket
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ResponseModel(BaseModel):
    success: bool = True
    data: Any = {}
    errorCode: str = ""
    errorMessage: str = ""
    showType: int = 0
    traceId: UUID = Field(default_factory=uuid4)
    # host: str = socket.gethostbyname(socket.gethostname())
    host: str = socket.gethostname()


# export interface response {
#   success: boolean; // if request is success
#   data?: any; // response data
#   errorCode?: string; // code for errorType
#   errorMessage?: string; // message display to user
#   showType?: number; // error display type： 0 silent; 1 message.warn; 2 message.error; 4 notification; 9 page
#   traceId?: string; // Convenient for back-end Troubleshooting: unique request ID
#   host?: string; // onvenient for backend Troubleshooting: host of current access server
# }
