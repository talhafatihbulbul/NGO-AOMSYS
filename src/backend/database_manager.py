from . data_objects import user
from . data_objects import donor
from . data_objects import system_administrator
from . data_objects import volunteer
from . data_objects import operation_coordinator
from . data_objects import donation
from . data_objects import shipment_request
from . data_objects import personal_profile
from . data_objects import aid_operation
from . data_objects import ship_items_operation
from . data_objects import collect_items_operation
from . data_objects import public_event_operation
from . data_objects import indigent_person
from . data_objects import aid_registration


class DatabaseManager:
    def __init__(self):
        self.volunteers: list = []
        self.operation_coordinators: list = []
        self.system_administrators: list = []
        self.donors: list = []

        self.donations: list = []
        self.shipment_requests: list = []
        self.aid_registrations: list = []
        self.personal_profiles: list = []

        self.ship_items_operations: list = []
        self.collect_items_operations: list = []
        self.public_event_operations: list = []

    def getDonorByID(self, input: int):
        for i in self.donors:
            if i.getID() == input:
                return i

    def getVolunteerByID(self, input: int):
        for i in self.volunteers:
            if i.getID() == input:
                return i

    def getOperationCoordinatorByID(self, input: int):
        for i in self.operation_coordinators:
            if i.getID() == input:
                return i

    def getSystemAdministratorByID(self, input: int):
        for i in self.system_administrators:
            if i.getID() == input:
                return i

    def getUserByID(self, input: int):
        for i in (self.donors+self.volunteers+self.operation_coordinators+self.system_administrators):
            if i.getID() == input:
                return i

    def getDonationByID(self, input: int):
        for i in self.donations:
            if i.getID() == input:
                return i

    def getShipmentRequestByID(self, input: int):
        for i in self.shipment_requests:
            if i.getID() == input:
                return i

    def getAidRegistrationByID(self, input: int):
        for i in self.aid_registrations:
            if i.getID() == input:
                return i

    def getPersonalProfileByID(self, input: int):
        for i in self.personal_profiles:
            if i.getID() == input:
                return i

    def getAidOperationByID(self, input: int):
        for i in self.ship_items_operations:
            if i.getID() == input:
                return i
        for i in self.collect_items_operations:
            if i.getID() == input:
                return i
        for i in self.public_event_operations:
            if i.getID() == input:
                return i

    def getDonations(self) -> list:
        return self.donations

    def getShipmentRequests(self) -> list:
        return self.shipment_requests

    def getAidRegistrations(self) -> list:
        return self.aid_registrations

    def getAidOperations(self) -> list:
        return self.ship_items_operations + self.collect_items_operations + self.public_event_operations

    def getPersonalProfiles(self) -> list:
        return self.personal_profiles

    def getUsers(self) -> list:
        return self.volunteers + self.operation_coordinators + self.system_administrators + self.donors

    def getVolunteers(self) -> list:
        return self.volunteers

    def getOperationCoordinators(self) -> list:
        return self.operation_coordinators

    def getSystemsAdministrators(self) -> list:
        return self.system_administrators

    def getDonors(self) -> list:
        return self.donors

    def addDonor(self, username: str, password: str, name: str, surname: str, email: str):
        new_donor = donor.Donor()
        new_donor.setUsername(username)
        new_donor.setPassword(password)
        new_donor.setName(name)
        new_donor.setSurname(surname)
        new_donor.setEmail(email)
        self.donors.append(new_donor)

    def addOperationCoordinator(self, username: str, password: str, name: str, surname: str, email: str):
        new_operation_coordinator = operation_coordinator.OperationCoordinator()
        new_operation_coordinator.setUsername(username)
        new_operation_coordinator.setPassword(password)
        new_operation_coordinator.setName(name)
        new_operation_coordinator.setSurname(surname)
        new_operation_coordinator.setEmail(email)
        self.operation_coordinators.append(new_operation_coordinator)

    def addSystemAdministrator(self, username: str, password: str, name: str, surname: str, email: str):
        new_system_administrator = system_administrator.SystemAdministrator()
        new_system_administrator.setUsername(username)
        new_system_administrator.setPassword(password)
        new_system_administrator.setName(name)
        new_system_administrator.setSurname(surname)
        new_system_administrator.setEmail(email)
        self.system_administrators.append(new_system_administrator)

    def addVolunteer(self, username: str, password: str, name: str, surname: str, email: str):
        new_volunteer = volunteer.Volunteer()
        new_volunteer.setUsername(username)
        new_volunteer.setPassword(password)
        new_volunteer.setName(name)
        new_volunteer.setSurname(surname)
        new_volunteer.setEmail(email)
        self.volunteers.append(new_volunteer)

    def addDonation(self, type_of_donation: str, amount: float, area: str, donor_input: donor.Donor):
        new_donation = donation.Donation()
        new_donation.setTypeOfDonation(type_of_donation)
        new_donation.setAmount(amount)
        new_donation.setArea(area)

        new_donation.setDonorID(donor_input.getID())

        donor_input.addDonation(new_donation)
        self.donations.append(new_donation)

    def addShipmentRequest(self, address: str, self_shipped: bool, donation_input: donation.Donation, donor_input: donor.Donor):
        new_shipment_request = shipment_request.ShipmentRequest()
        new_shipment_request.setAddress(address)
        new_shipment_request.setSelfShipped(self_shipped)
        new_shipment_request.setDonationID(donation_input.getID())

        new_shipment_request.setDonorID(donor_input.getID())
        donation_input.setShipmentRequestID(new_shipment_request.getID())

        donor_input.addShipmentRequest(new_shipment_request)
        self.shipment_requests.append(new_shipment_request)

    def addAidRegistration(self, number_of_children: int, monthly_income: float, address: str, household_members: list, monthly_expenditures: str, nature_of_support_needed: str):
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

    def addPersonalProfile(self, profession: str, average_annual_income: float, selected_region: str, transportation_support: str, availability: str, accepted: bool, volunteer_input: volunteer.Volunteer):
        new_personal_profile = personal_profile.PersonalProfile()
        new_personal_profile.setProfession(profession)
        new_personal_profile.setAverageAnnualIncome(average_annual_income)
        new_personal_profile.setSelectedRegion(selected_region)
        new_personal_profile.setTransportationSupport(transportation_support)
        new_personal_profile.setAvailability(availability)
        new_personal_profile.setAccepted(accepted)

        new_personal_profile.setVolunteerID(volunteer_input.getID())

        volunteer_input.setPersonalProfile(new_personal_profile)
        self.personal_profiles.append(new_personal_profile)

    def addShipItemsOperation(self, address: str, destination_address: str, operation_coordinator_input: operation_coordinator.OperationCoordinator):
        new_ship_items_operation = ship_items_operation.ShipItemsOperation()
        new_ship_items_operation.setAddress(address)
        new_ship_items_operation.setDestinationAddress(destination_address)

        new_ship_items_operation.setOperationCoordinatorID(operation_coordinator_input.getID())

        operation_coordinator_input.addAidOperation(new_ship_items_operation)
        self.ship_items_operations.append(new_ship_items_operation)

    def addCollectItemsOperation(self, address: str, destination_address: str, operation_coordinator_input: operation_coordinator.OperationCoordinator):
        new_collect_items_operation = collect_items_operation.CollectItemsOperation()
        new_collect_items_operation.setAddress(address)
        new_collect_items_operation.setDestinationAddress(destination_address)

        new_collect_items_operation.setOperationCoordinatorID(operation_coordinator_input.getID())

        operation_coordinator_input.addAidOperation(new_collect_items_operation)
        self.collect_items_operations.append(new_collect_items_operation)

    def addPublicEventOperation(self, address: str, event_name: str, operation_coordinator_input: operation_coordinator.OperationCoordinator):
        new_public_event_operation = public_event_operation.PublicEventOperation()
        new_public_event_operation.setAddress(address)
        new_public_event_operation.setEventName(event_name)

        new_public_event_operation.setOperationCoordinatorID(operation_coordinator_input.getID())

        operation_coordinator_input.addAidOperation(new_public_event_operation)
        self.public_event_operations.append(new_public_event_operation)

    def removeDonor(self, donor: donor.Donor):
        self.donors.remove(donor)

    def removeOperationCoordinator(self, operation_coordinator_input: operation_coordinator.OperationCoordinator):
        self.operation_coordinators.remove(operation_coordinator_input)

    def removeSystemAdministrator(self, system_administrator: system_administrator.SystemAdministrator):
        self.system_administrators.remove(system_administrator)

    def removeVolunteer(self, volunteer_input: volunteer.Volunteer):
        self.personal_profiles.remove(volunteer_input.getPersonalProfile())
        self.volunteers.remove(volunteer_input)

    def removeDonation(self, donation_input: donation.Donation):
            (self.getDonorByID(donation_input.getDonorID())).removeDonation(donation_input)
            self.donations.remove(donation_input)

    def removeShipmentRequest(self, shipment_request_input: shipment_request.ShipmentRequest):
        self.getDonorByID(shipment_request_input.getDonorID()).removeShipmentRequest(shipment_request_input)
        self.shipment_requests.remove(shipment_request_input)

    def removeAidRegistration(self, aid_registration_input: aid_registration.AidRegistration):
        self.aid_registrations.remove(aid_registration_input)

    def removePersonalProfile(self, personal_profile_input: personal_profile.PersonalProfile):
        self.personal_profiles.remove(personal_profile_input)

    def removeAidOperation(self, aid_operation_input: aid_operation.AidOperation):
        self.getOperationCoordinatorByID(aid_operation_input.getOperationCoordinatorID()).removeAidOperation(aid_operation_input)

        if isinstance(aid_operation_input, ship_items_operation.ShipItemsOperation):
            self.ship_items_operations.remove(aid_operation_input)
        elif isinstance(aid_operation_input, collect_items_operation.CollectItemsOperation):
            self.collect_items_operations.remove(aid_operation_input)
        elif isinstance(aid_operation_input, public_event_operation.PublicEventOperation):
            self.public_event_operations.remove(aid_operation_input)

    def removeUser(self, user_input: user.User):
        if isinstance(user_input, donor.Donor):
            self.removeDonor(user_input)
        elif isinstance(user_input, volunteer.Volunteer):
            self.removeVolunteer(user_input)
        elif isinstance(user_input, operation_coordinator.OperationCoordinator):
            self.removeOperationCoordinator(user_input)
        elif isinstance(user_input, system_administrator.SystemAdministrator):
            self.removeSystemAdministrator(user_input)
