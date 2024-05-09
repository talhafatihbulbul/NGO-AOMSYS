import indigent_person


class AidRegistration:
    last_id: int = 0

    def __init__(self):
        self.number_of_children: int = 0
        self.monthly_income: float = 0.0
        self.address: str = ""
        self.household_members: list = []
        self.monthly_expenditures: str = ""
        self.nature_of_support_needed: str = ""
        AidRegistration.last_id = AidRegistration.last_id + 1
        self.id: int = AidRegistration.last_id

    def getNumberOfChildren(self) -> int:
        return self.number_of_children

    def getMonthlyIncome(self) -> float:
        return self.monthly_income

    def getAddress(self) -> str:
        return self.address

    def getHouseholdMembers(self) -> list:
        return self.household_members

    def getMonthlyExpenditures(self) -> str:
        return self.monthly_expenditures

    def getNatureOfSupportNeeded(self) -> str:
        return self.nature_of_support_needed

    def setNumberOfChildren(self, input: int):
        self.number_of_children = input

    def setMonthlyIncome(self, input: float):
        self.monthly_income = input

    def setAddress(self, input: str):
        self.adress = input

    def addHouseholdMember(self, input: indigent_person.IndigentPerson):
        self.household_members.append(input)

    def removeHouseholdMember(self, input: indigent_person.IndigentPerson):
        self.household_members.remove(input)

    def setMonthlyExpenditures(self, input: str):
        self.monthly_expenditures = input

    def setNatureOfSupportNeeded(self, input: str):
        self.nature_of_support_needed = input

    def getID(self) -> int:
        return self.id
