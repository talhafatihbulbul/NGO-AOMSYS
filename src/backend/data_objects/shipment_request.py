class ShipmentRequest:
    last_id: int = 0

    def __init__(self):
        self.address: str = ""
        self.self_shipped: bool = False
        self.shipped_by_NGO: bool = False
        ShipmentRequest.last_id = ShipmentRequest.last_id + 1
        self.id: int = ShipmentRequest.last_id
        self.donation_id: int = 0
        self.donor_id: int = 0

    def getAddress(self):
        return self.address

    def setAddress(self, input: str):
        self.address = input

    def isSelfShipped(self) -> bool:
        return self.self_shipped

    def isShippedByNGO(self) -> bool:
        return self.shipped_by_NGO

    def setSelfShipped(self, input: bool):
        self.self_shipped = input
        self.shipped_by_NGO = not input

    def setShippedByNGO(self, input: bool):
        self.shipped_by_NGO = input
        self.self_shipped = not input

    def getID(self):
        return self.id

    def getDonationID(self) -> int:
        return self.donation_id

    def setDonationID(self, input: int):
        self.donation_id = input

    def getDonorID(self) -> int:
        return self.donor_id

    def setDonorID(self, input: int):
        self.donor_id = input
