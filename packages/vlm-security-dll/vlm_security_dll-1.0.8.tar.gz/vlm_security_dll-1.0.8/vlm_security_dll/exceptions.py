
class VLM_Security_Exception(Exception):
    def __init__(self, error_code, error_description, *args):
        super(VLM_Security_Exception, self).__init__(
            "[{}:{}]".format(error_code, error_description)
        )
        self.error_description = error_description
        self.error_code = error_code

VLM_Security_Exception = VLM_Security_Exception

class RegistrationDisabledException(VLM_Security_Exception):
    def __init__(self):
        msg = "Registration code is disabled"
        super(RegistrationDisabledException, self).__init__(-2, msg)

class BindingLimitException(VLM_Security_Exception):
    def __init__(self):
        msg = "Number of binding machines exceeded limit"
        super(BindingLimitException, self).__init__(-3, msg)

class OnlineException(VLM_Security_Exception):
    def __init__(self):
        msg = "Registration code is already online"
        super(OnlineException, self).__init__(-4, msg)

class ExpiredException(VLM_Security_Exception):
    def __init__(self):
        msg = "Expired"
        super(ExpiredException, self).__init__(-5, msg)

class BalanceException(VLM_Security_Exception):
    def __init__(self):
        msg = "Insufficient user balance"
        super(BalanceException, self).__init__(-6, msg)

class InvalidUserException(VLM_Security_Exception):
    def __init__(self):
        msg = "Invalid user"
        super(InvalidUserException, self).__init__(-6, msg)


