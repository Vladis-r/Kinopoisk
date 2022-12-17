from project.models import User



class AuthDAO:
    def __init__(self, session):
        self.session = session

    def create_user(self, data):
        user = User(**data)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user_by_email(self, email):
        return self.session.query(User).filter(User.email == email).one()
