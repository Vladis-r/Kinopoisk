from project.models import User
from project.tools.security import generate_password_hash


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all_users(self):
        return self.session.query(User).all()

    def get_user_by_id(self, uid):
        return self.session.query(User).get(uid)

    def get_user_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def update_user(self, data):
        self.session.query(User).filter(User.id == data.get("id")).update(*data)
        self.session.commit()

    def patch_user(self, patch_user, user):
        if "email" in patch_user:
            user.email = patch_user.get("email")
        if "name" in patch_user:
            user.name = patch_user.get("name")
        if "surname" in patch_user:
            user.surname = patch_user.get("surname")
        if "favourite_genre" in patch_user:
            user.favourite_genre = patch_user.get("favourite_genre")
        self.session.add(user)
        self.session.commit()
        return user, 204

    def change_password(self, user, new_password):
        user.password = generate_password_hash(new_password)
        self.session.add(user)
        self.session.commit()
        return user

    def delete_user(self, uid):
        user = self.get_user_by_id(uid)
        self.session.delete(user)
        self.session.commit()
