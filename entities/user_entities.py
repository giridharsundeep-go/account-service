

class User:

    def get_user(self):
        return "SELECT * FROM user_account WHERE email=%s OR phone=%s"

