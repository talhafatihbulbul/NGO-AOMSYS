from . import user
from . import aid_operation
from . import ship_items_operation
from . import collect_items_operation
from . import public_event_operation


class OperationCoordinator(user.User):
    def __init__(self):
        user.User.__init__(self)
        self.aid_operations: list = []

    def getAidOperations(self) -> list:
        return self.aid_operations

    def addAidOperation(self, input: aid_operation.AidOperation):
        self.aid_operations.append(input)

    def removeAidOperation(self, input: aid_operation.AidOperation):
        self.aid_operations.remove(input)
