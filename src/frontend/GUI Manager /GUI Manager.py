# frontend-gui_manager.py

class GUIManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def showLogin(self):
        print("Displaying Login Screen")

    def showRegister(self):
        print("Displaying Register Screen")

    def showMainMenu(self):
        print("Displaying Main Menu")

    def showUsers(self):
        users = self.database_manager.getUsers()
        print("Displaying Users:", users)

    def showPersonalProfiles(self):
        profiles = self.database_manager.getPersonalProfiles()
        print("Displaying Personal Profiles:", profiles)

    def showOperations(self):
        operations = self.database_manager.getOperations()
        print("Displaying Operations:", operations)

    def showDonations(self):
        donations = self.database_manager.getDonations()
        print("Displaying Donations:", donations)

    def showShipmentRequests(self):
        shipments = self.database_manager.getShipmentRequests()
        print("Displaying Shipment Requests:", shipments)

