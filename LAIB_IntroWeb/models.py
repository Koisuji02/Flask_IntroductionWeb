from flask_login import UserMixin

class User(UserMixin):
    def __init__ (self, id, nickname, password, locatore):
        self.id=id
        self.nickname=nickname
        self.password=password
        self.locatore=locatore