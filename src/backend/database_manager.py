from data_objects import user
from data_objects import donor
from data_objects import system_administrator
from data_objects import volunteer
from data_objects import operation_coordinator
from data_objects import donation
from data_objects import shipment_request
from data_objects import personal_profile
from data_objects import aid_operation
from data_objects import ship_items_operation
from data_objects import collect_items_operation
from data_objects import public_event_operation
from data_objects import indigent_person
from data_objects import aid_registration


class DatabaseManager:
    def __init__(self):
        self.volunteers: list = []
        self.operation_coordinators: list = []
        self.system_administrators: list = []
        self.donors: list = []

        self.donations: list = []
        self.shipment_requests: list = []
        self.aid_registrations: list = []
        self.aid_operations: list = []
        self.personal_profiles: list = []

    def getDonations(self) -> list:
        return self.donations

    def getShipmentRequests(self) -> list:
        return self.shipment_requests

    def getAidRegistrations(self) -> list:
        return self.aid_registrations

    def getAidOperations(self) -> list:
        return self.aid_operations

    def getPersonalProfiles(self) -> list:
        return self.personal_profiles

    def getUsers(self) -> list:
        return self.volunteers + self.operation_coordinators + self.system_administrators + self.donors

    def addDonor(self, username: str, password: str, name: str, surname: str, email: str):
        new_donor = donor.Donor()
        new_donor.setUsername(username)
        new_donor.setPassword(password)
        new_donor.setName(name)
        new_donor.setEmail(email)
        self.donors.append(new_donor)

    def addOperationCoordinator(self, username: str, password: str, name: str, surname: str, email: str):
        new_operation_coordinator = operation_coordinator.OperationCoordinator()
        new_operation_coordinator.setUsername(username)
        new_operation_coordinator.setPassword(password)
        new_operation_coordinator.setName(name)
        new_operation_coordinator.setEmail(email)
        self.operation_coordinators.append(new_operation_coordinator)

    def addSystemAdministrator(self, username: str, password: str, name: str, surname: str, email: str):
        new_system_administrator = system_administrator.SystemAdministrator()
        new_system_administrator.setUsername(username)
        new_system_administrator.setPassword(password)
        new_system_administrator.setName(name)
        new_system_administrator.setEmail(email)
        self.system_administrators.append(new_system_administrator)

    def addVolunteer(self, username: str, password: str, name: str, surname: str, email: str):
        new_volunteer = volunteer.Volunteer()
        new_volunteer.setUsername(username)
        new_volunteer.setPassword(password)
        new_volunteer.setName(name)
        new_volunteer.setEmail(email)
        self.volunteers.append(new_volunteer)

    def addDonation(self, type_of_donation: str, amount: float, area: str, donor) -> donation.Donation:
        new_donation = donation.Donation()
        new_donation.setTypeOfDonation(type_of_donation)
        new_donation.setAmount(amount)
        new_donation.setArea(area)
        self.donations.append(new_donation)
        return new_donation

    def addShipmentRequest(self, address: str, self_shipped: bool, donation: donation.Donation) -> shipment_request.ShipmentRequest:
        new_shipment_request = shipment_request.ShipmentRequest()
        new_shipment_request.setAddress(address)
        new_shipment_request.setSelfShipped(self_shipped)
        new_shipment_request.setDonation(donation)
        self.shipment_requests.append(new_shipment_request)
        return new_shipment_request

    def addAidRegistration(self, number_of_children: int, monthly_income: float, address: string, household_members: list, monthly_expenditures: str, nature_of_support_needed: str):
        new_aid_registration = aid_registration.AidRegistration()
        new_aid_registration.setNumberOfChildren(number_of_children)
        new_aid_registration.setMonthlyIncome(monthly_income)
        new_aid_registration.setAddress(address)
        for i in household_members:
            new_aid_registration.addHouseholdMember(i)
        new_aid_registration.setMonthlyExpenditures(monthly_expenditures)
        new_aid_registration.setNatureOfSupportNeeded(nature_of_support_needed)
        self.aid_registrations.append(new_aid_registration)

    def makeIndigentPerson(self, name: str, surname: str, employment_status: str, educational_status: str, age: int) -> indigent_person.IndigentPerson:
        new_indigent_person = indigent_person.IndigentPerson()
        new_indigent_person.setName(name)
        new_indigent_person.setSurname(surname)
        new_indigent_person.setEmploymentStatus(employment_status)
        new_indigent_person.setEducationalStatus(educational_status)
        new_indigent_person.setAge(age)
        return new_indigent_person

        
