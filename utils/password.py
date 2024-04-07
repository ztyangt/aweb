import bcrypt


class PasswordUtil:
    @staticmethod
    def create(password: str) -> str:
        # 生成bcrypt加密的密码
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()

    @staticmethod
    def verify(encoded_password: str, password: str) -> bool:
        # 验证密码
        return bcrypt.checkpw(password.encode(), encoded_password.encode())
