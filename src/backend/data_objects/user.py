class User:
    last_id: int = 0

    def __init__(self):
        self.username: str = ""
        self.password: str = ""
        self.name: str = ""
        self.surname: str = ""
        self.email: str = ""
        User.last_id = User.last_id+1
        self.id: int = User.last_id

    def getUsername(self) -> str:
        return self.username

    def isPasswordCorrect(self, input: str) -> bool:
        return input == self.password

    def getName(self) -> str:
        return self.name

    def getSurname(self) -> str:
        return self.surname

    def setUsername(self, input: str):
        self.username = input

    def setPassword(self, input: str):
        self.password = input

    def setName(self, input: str):
        self.name = input

    def setSurname(self, input: str):
        self.surname = input

    def setEmail(self, input: str):
        self.email = input

    def getID(self) -> int:
        return self.id
