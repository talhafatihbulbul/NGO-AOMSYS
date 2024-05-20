from . import user
from . import donation
from . import shipment_request


class Donor(user.User):
    def __init__(self):
        user.User.__init__(self)
        self.donations: list = []
        self.shipment_requests: list = []

    def getDonations(self) -> list:
        return self.donations

    def getShipmentRequests(self) -> list:
        return self.shipment_requests

    def addDonation(self, input: donation.Donation):
        print("called")
        self.donations.append(input)

    def removeDonation(self, input: donation.Donation):
        return self.donations.remove(input)

    def addShipmentRequest(self, input: shipment_request.ShipmentRequest):
        self.shipment_requests.append(input)

    def removeShipmentRequest(self, input: shipment_request.ShipmentRequest):
        self.shipment_requests.remove(input)
