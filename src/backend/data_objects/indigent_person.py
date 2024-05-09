class IndigentPerson:
    def __init__(self):
        self.name: str = ""
        self.surname: str = ""
        self.employment_status: str = ""
        self.educational_status: str = ""
        self.age: int = 0

    def getName(self) -> str:
        return self.name

    def getSurname(self) -> str:
        return self.surname

    def getEmploymentStatus(self) -> str:
        return self.employment_status

    def getEducationalStatus(self) -> str:
        return self.educational_status

    def getAge(self) -> int:
        return self.age

    def setName(self, input: str):
        self.name = input

    def setSurname(self, input: str):
        self.surname = input

    def setEmploymentStatus(self, input: str):
        self.employment_status: str = input

    def setEducationalStatus(self, input: str):
        self.educational_status = input

    def setAge(self, input: int):
        self.age = input
