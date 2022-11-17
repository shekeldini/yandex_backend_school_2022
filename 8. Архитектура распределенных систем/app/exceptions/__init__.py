class MyException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail


class TooMuchRetry(MyException):
    def __init__(self, status_code, detail):
        super().__init__(status_code, detail)


class NoId(MyException):
    def __init__(self, status_code, detail):
        super().__init__(status_code, detail)


class NoTimeStamp(MyException):
    def __init__(self, status_code, detail):
        super().__init__(status_code, detail)


class NoOneAvailableService(MyException):
    def __init__(self, status_code, detail):
        super().__init__(status_code, detail)


class InvalidStrategy(MyException):
    def __init__(self, status_code, detail):
        super().__init__(status_code, detail)


exception_list = [
    TooMuchRetry,
    NoId,
    NoTimeStamp,
    NoOneAvailableService,
    InvalidStrategy
]

__all__ = [
    exception_list
]
