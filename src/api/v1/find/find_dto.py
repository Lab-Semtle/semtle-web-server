from var.dto import BaseDTO
class FindPWRequest(BaseDTO):
    email: str
    phone: str

class FindPWResponse(BaseDTO):
    password: str
