from . import user
from . import personal_profile


class Volunteer(user.User):
    def __init__(self):
        user.User.__init__(self)
        self.personal_profile = personal_profile.PersonalProfile()

    def getPersonalProfile(self) -> personal_profile.PersonalProfile:
        return self.personal_profile

    def setPersonalProfile(self, input: personal_profile.PersonalProfile):
        self.personal_profile = input
