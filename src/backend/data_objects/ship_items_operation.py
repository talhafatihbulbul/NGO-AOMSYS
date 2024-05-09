import aid_operation


class ShipItemsOperation(aid_operation.AidOperation):
    def __init__(self):
        aid_operation.AidOperation.__init__(self)
        self.destination_address: str = ""

    def getDestinationAddress(self) -> str:
        return self.destination_address

    def setDestinationAddress(self, input: str):
        self.destination_address = input
