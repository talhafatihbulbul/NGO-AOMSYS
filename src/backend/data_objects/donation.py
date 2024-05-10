class Donation:
    last_id: int = 0

    def __init__(self):
        self.type_of_donation: str = ""
        self.amount: float = 0.0
        self.area: str = ""
        self.donor_id: int=0
        self.shipment_request_id: int=0
        Donation.last_id = Donation.last_id+1
        self.id: int = Donation.last_id

    def getTypeOfDonation(self) -> str:
        return self.type_of_donation

    def setTypeOfDonation(self, input: str):
        self.type_of_donation = input

    def getAmount(self) -> float:
        return self.amount

    def setAmount(self, input: float):
        self.amount = input

    def getArea(self) -> str:
        return self.area

    def setArea(self, input: str):
        self.area = input

    def getID(self) -> int:
        return self.id

    def getDonorID(self) -> int:
        return self.donor_id

    def setDonorID(self, input: int):
        self.donor_id = input

    def getShipmentRequestID(self) -> int:
        return self.shipment_request_id

    def setShipmentRequestID(self, input: int):
        self.shipment_request_id = input
