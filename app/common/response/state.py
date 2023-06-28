from fastapi import status


class State(Exception):
    State = []

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

        State.State.append(self)

    def set_msg(self, error_message):
        self.error_message = error_message
        return self

    def __eq__(self, other):
        return self.http_status == other


Ok: State = State("0000", "Ok", status.HTTP_200_OK, 0)

InvalidRequest: State = State("4000", "Invalid Request", status.HTTP_400_BAD_REQUEST, 1)
ValidationError: State = State(
    "4022", "Validation Error", status.HTTP_422_UNPROCESSABLE_ENTITY, 1
)
UnAthenticated: State = State("4001", "UnAthenticated", status.HTTP_401_UNAUTHORIZED, 9)
PermissionDenied: State = State(
    "4003", "Permission Denied", status.HTTP_403_FORBIDDEN, 1
)
NotFound: State = State("4004", "Not Found", status.HTTP_404_NOT_FOUND, 9)
AlreadyExists: State = State("4009", "Already Exists", status.HTTP_409_CONFLICT, 1)
ResourceExhausted: State = State(
    "4029", "Resource Exhausted", status.HTTP_429_TOO_MANY_REQUESTS, 1
)

ServerError: State = State("5000", "服务器开小差了", status.HTTP_500_INTERNAL_SERVER_ERROR, 1)
BadGateway: State = State("5002", "网关错误", status.HTTP_502_BAD_GATEWAY, 1)
ServiceUnavailable: State = State(
    "5003", "服务器繁忙", status.HTTP_503_SERVICE_UNAVAILABLE, 1
)
GatewayTimeout: State = State("5004", "网关超时", status.HTTP_504_GATEWAY_TIMEOUT, 1)
SqlFail: State = State("5100", "数据库执行失败", status.HTTP_500_INTERNAL_SERVER_ERROR, 1)

BusinessError: State = State("1000", "业务错误", status.HTTP_400_BAD_REQUEST, 1)
DataNotFound: State = State("1001", "未查询到", status.HTTP_400_BAD_REQUEST, 1)
DataStoreFail: State = State("1002", "新增失败", status.HTTP_400_BAD_REQUEST, 1)
DataUpdateFail: State = State("1003", "更新失败", status.HTTP_400_BAD_REQUEST, 1)
DataDestroyFail: State = State("1004", "删除失败", status.HTTP_400_BAD_REQUEST, 1)
