
class FrontendApi:
    def __init__(self, service, validator):
        self.serv = service
        self.validator = validator
    
    def create_account(self, creds):
        valid = self.validator.account_validator(creds, new=True)

        if not valid:
            #TODO: Creation of account failed message due to some validation failure
            raise ValidationError("")

        return self.serv.create_account(creds)

    def find_account(self, creds):
        valid = self.validator.account_validator(creds, new=False)

        if not valid:
            #TODO: Invalid credentials entered msg
            raise ValidationError("")

        login = creds[0]

        return self.serv.find_account(login)


