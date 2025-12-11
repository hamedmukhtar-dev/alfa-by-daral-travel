from fastapi import HTTPException, status

class CredentialsException(HTTPException):
    def __init__(self, detail="بيانات الدخول غير صحيحة"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class PermissionDenied(HTTPException):
    def __init__(self, detail="ليس لديك الصلاحية"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ResourceNotFound(HTTPException):
    def __init__(self, detail="العنصر غير موجود"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InsufficientBalance(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="الرصيد غير كافٍ")


class ServiceRequestError(HTTPException):
    def __init__(self, detail="فشل في تنفيذ الخدمة"):
        super().__init__(status_code=400, detail=detail)
