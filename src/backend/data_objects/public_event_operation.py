from . import aid_operation


class PublicEventOperation(aid_operation.AidOperation):
    def __init__(self):
        aid_operation.AidOperation.__init__(self)
        self.event_name: str = ""

    def getEventName(self) -> str:
        return self.event_name

    def setEventName(self, input: str):
        self.event_name = input
