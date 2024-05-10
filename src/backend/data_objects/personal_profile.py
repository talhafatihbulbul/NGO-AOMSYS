class PersonalProfile:
    def __init__(self):
        self.profession: str = ""
        self.average_annual_income: float = 0.0
        self.selected_region: str = ""
        self.transportation_support: str = ""
        self.availability: str = ""
        self.accepted: bool = False
        self.is_pending: bool = True
        self.volunteer_id: int = 0

    def getProfession(self) -> str:
        return self.profession

    def getAverageAnnualIncome(self) -> float:
        return self.average_annual_income

    def getSelectedRegion(self) -> str:
        return self.selected_region

    def getTransportationSupport(self) -> str:
        return self.transportation_support

    def getAvailability(self) -> str:
        return self.availability

    def setProfession(self, input: str):
        self.profession = input

    def setAverageAnnualIncome(self, input: float):
        self.average_annual_income = input

    def setSelectedRegion(self, input: str):
        self.selected_region = input

    def setTransportationSupport(self, input: str):
        self.transportation_support = input

    def setAvailability(self, input: str):
        self.availability = input

    def getAccepted(self) -> bool:
        return self.accepted

    def setAccepted(self, input: bool):
        self.accepted = input
        if self.accepted == True:
            self.is_pending = False

    def getIsPending(self) -> bool:
        return self.is_pending

    def getVolunteerID(self) -> int:
        return self.volunteer_id

    def setVolunteerID(self, input: int):
        self.volunteer_id = input
