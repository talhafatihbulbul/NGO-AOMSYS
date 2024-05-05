class Donation:
    def __init__(self, type_of_donation, amount, area, id):
        self.type_of_donation = type_of_donation
        self.amount = amount
        self.area = area
        self.id = id

    def getTypeOfDonation(self):
        return self.type_of_donation

    def getAmount(self):
        return self.amount

    def getArea(self):
        return self.area

    def getID(self):
        return self.id

    def setTypeOfDonation(self, type_of_donation):
        self.type_of_donation = type_of_donation

    def setAmount(self, amount):
        self.amount = amount

    def setArea(self, area):
        self.area = area

class ShipmentRequest:
    def __init__(self, address, shipped, shipped_by_ngo, id, donation):
        self.address = address
        self.shipped = shipped
        self.shipped_by_ngo = shipped_by_ngo
        self.id = id
        self.donation = donation

    def getAddress(self):
        return self.address

    def isShipped(self):
        return self.shipped

    def isShippedByNGO(self):
        return self.shipped_by_ngo

    def getID(self):
        return self.id

    def getDonation(self):
        return self.donation

    def setAddress(self, address):
        self.address = address

    def setShipped(self, shipped):
        self.shipped = shipped

    def setShippedByNGO(self, shipped_by_ngo):
        self.shipped_by_ngo = shipped_by_ngo

class User:
    def __init__(self, username, password, name, surname, email, id):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.email = email
        self.id = id

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getName(self):
        return self.name

    def getSurname(self):
        return self.surname

    def getEmail(self):
        return self.email

    def getID(self):
        return self.id

    def setUsername(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password

    def setName(self, name):
        self.name = name

    def setSurname(self, surname):
        self.surname = surname

    def setEmail(self, email):
        self.email = email

class PersonalProfile:
    def __init__(self, profession, average_annual_income, selected_region, transportation_support, availability, accepted, pending):
        self.profession = profession
        self.average_annual_income = average_annual_income
        self.selected_region = selected_region
        self.transportation_support = transportation_support
        self.availability = availability
        self.accepted = accepted
        self.pending = pending

    
