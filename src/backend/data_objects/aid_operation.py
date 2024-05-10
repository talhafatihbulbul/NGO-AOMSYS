class AidOperation:
    last_id: int = 0

    def __init__(self):
        self.address: str = ""
        self.operation_coordinator_id: int = 0
        AidOperation.last_id = AidOperation.last_id + 1
        self.id: int = AidOperation.last_id

    def getAddress(self) -> str:
        return self.address

    def setAddress(self, input: str):
        self.address = input

    def getID(self) -> int:
        return self.id

    def getOperationCoordinatorID(self) -> int:
        return self.operation_coordinator_id

    def setOperationCoordinatorID(self, input: int):
        self.operation_coordinator_id = input
