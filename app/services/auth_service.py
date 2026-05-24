class AuthService:
    def __init__(self, admins: list[int], users: list[int]) -> None:
        self.admins = set(admins)
        self.users = set(users)

    def is_admin(self, user_id: int) -> bool:
        return user_id in self.admins

    def is_allowed_user(self, user_id: int) -> bool:
        return user_id in self.admins or user_id in self.users
