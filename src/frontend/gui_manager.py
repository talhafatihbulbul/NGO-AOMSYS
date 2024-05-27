import sys
sys.path.append(".")
from backend.data_objects import user
from backend.data_objects import donor
from backend.data_objects import volunteer
from backend.data_objects import operation_coordinator
from backend.data_objects import system_administrator
from backend.data_objects import collect_items_operation
from backend.data_objects import ship_items_operation
from backend.data_objects import public_event_operation
from backend import database_manager
from nicegui import ui, app


dbm = database_manager.DatabaseManager()
# General Part


def logout():
    app.storage.user["id"] = -1
    app.storage.user["username"] = ""
    app.storage.user["password"] = ""
    app.storage.user["type"] = ""
    ui.navigate.to("/login")


@ui.page("/", title="NGO-AOMSYS")
def start_page():
    ui.navigate.to("/login")


@ui.page("/login", title="Log In")
def login():
    username = ui.input(label="Username")
    password = ui.input(label="Password",
                        password=True, password_toggle_button=True)

    def log_in_button_on_click():
        for i in dbm.getUsers():
            if i.getUsername() == username.value:
                if i.isPasswordCorrect(password.value):
                    app.storage.user["id"] = i.getID()
                    app.storage.user["username"] = i.getUsername()
                    app.storage.user["password"] = password.value
                    if isinstance(
                            i,
                            donor.Donor):
                        app.storage.user["type"] = "donor"
                        ui.navigate.to("/donor-menu")
                    elif isinstance(
                            i,
                            volunteer.Volunteer):
                        app.storage.user["type"] = "volunteer"
                        ui.navigate.to("/volunteer-menu")
                    elif isinstance(
                            i,
                            operation_coordinator.OperationCoordinator):
                        app.storage.user["type"] = "operation_coordinator"
                        ui.navigate.to("/operation-coordinator-menu")
                    elif isinstance(
                            i,
                            system_administrator.SystemAdministrator):
                        app.storage.user["type"] = "system_administrator"
                        ui.navigate.to("/system-administrator-menu")
                else:
                    ui.notify("Info doesn't match")
                    return
        ui.notify("Info doesn't match")

    def register_button_on_click():
        ui.navigate.to("/register")

    def aid_register_button_on_click():
        ui.navigate.to("/aid-registration-form")

    ui.button(text="Log in", on_click=lambda: log_in_button_on_click())
    ui.button(text="Register", on_click=lambda: register_button_on_click())
    ui.button(text="Aid Registration", on_click=lambda: ui.navigate.to("/aid-registration-form"))


@ui.page("/register", title="Register")
def register():
    username = ui.input(label="Username")
    name = ui.input(label="Name")
    surname = ui.input(label="Surname")
    password1 = ui.input(label="Password", password=True,
                         password_toggle_button=True)
    password2 = ui.input(label="Password Again", password=True,
                         password_toggle_button=True)
    email = ui.input(label="Email")
    donor_or_volunteer = ui.toggle(["Donor", "Volunteer"], value="Donor")

    def register_button_on_click():
        if password1.value == password2.value:
            if donor_or_volunteer.value == "Donor":
                dbm.addDonor(username.value,
                             password1.value,
                             name.value,
                             surname.value,
                             email.value)
            elif donor_or_volunteer.value == "Volunteer":
                dbm.addVolunteer(username.value,
                              password1.value,
                              name.value,
                              surname.value,
                              email.value)
            ui.navigate.to("/login")
        else:
            ui.notify("Passwords don't match.")

    ui.button(text="Sign up", on_click=lambda: register_button_on_click())


@ui.page("/manage-account", title="Manage Account")
def manage_account():
    info_table_columns = [{"name": "username", "label": "Username", "field": "username"},
                          {"name": "name", "label": "Name", "field": "name"},
                          {"name": "surname", "label": "Surname", "field": "surname"},
                          {"name": "email", "label": "Email", "field": "email"}]
    current_user = dbm.getUserByID(app.storage.user["id"])
    if current_user is None:
        ui.notify("Identification failed.")
    elif current_user.isPasswordCorrect(app.storage.user["password"]):
        info_table = ui.table(columns=info_table_columns, rows=[{"username":current_user.getUsername(),
                                                                 "name": current_user.getName(),
                                                                 "surname": current_user.getSurname(),
                                                                 "email": current_user.getEmail()}])
        previous_password = ui.input(label="Previous Password", password=True, password_toggle_button=True)
        new_password = ui.input(label="New Password", password=True, password_toggle_button=True)
        new_password_again = ui.input(label="New Password Again", password=True, password_toggle_button=True)

        def change_password_button_on_click():
            if new_password.value == new_password_again.value:
                if current_user.isPasswordCorrect(previous_password.value):
                    app.storage.user["password"] = new_password.value
                    current_user.setPassword(new_password.value)
                    ui.notify("Password has been changed.")
                else:
                    ui.notify("Password is incorrect.")
            else:
                ui.notify("Passwords don't match.")

        ui.button(text="Change Password",
                  on_click=lambda: change_password_button_on_click())


    else:
        ui.notify("Identification failed.")


@ui.page("/aid-registration-form", title="Aid Registration Form")
def aid_registration_form():
    ui.label("The Aid Registration Form")
    household_members_columns = [
            {"name": "name", "label": "Name", "field": "name"},
            {"name": "surname", "label": "Surname", "field": "surname"},
            {"name": "employment_status", "label": "Employment Status", "field": "employment_status"},
            {"name": "educational_status", "label": "Educational Status", "field": "educational_status"},
            {"name": "age", "label": "Age", "field": "age"}
            ]
    household_members =[]
    number_of_children = ui.number(label="Number of Children", precision=0, value=0)
    monthly_income = ui.number(label="Monthly Income", precision=2, value=0.0)
    address = ui.textarea(label="Address")
    household_members_table = ui.table(columns=household_members_columns, rows=[])
    monthly_expenditures = ui.textarea(label="Monthly Expenditures")
    nature_of_support_needed = ui.input(label="Nature of Support Needed")

    def send_aid_registration_form_on_click():
        dbm.addAidRegistration(int(number_of_children.value),
                               float(monthly_income.value),
                               address.value,
                               household_members,
                               monthly_expenditures.value,
                               nature_of_support_needed.value)
        ui.notify("Aid Registration Form has been sent!")
        ui.navigate.to("/login")

    ui.button(text="Send Aid Registration Form", on_click=lambda: send_aid_registration_form_on_click())

    ui.label("New Household Member")
    name = ui.input(label="Name")
    surname = ui.input(label="Surname")
    employment_status = ui.input(label="Employment Status")
    educational_status = ui.input(label="Educational Status")
    age = ui.number(label="Age", precision=0, value=0)

    def add_household_member_on_click():
        current_indigent_person = dbm.makeIndigentPerson(name.value,
                               surname.value,
                               employment_status.value,
                               educational_status.value,
                               int(age.value))
        household_members.append(current_indigent_person)
        household_members_table.add_rows({
            "name": current_indigent_person.getName(),
            "surname": current_indigent_person.getSurname(),
            "employment_status": current_indigent_person.getEmploymentStatus(),
            "educational_status": current_indigent_person.getEducationalStatus(),
            "age": current_indigent_person.getAge()
            })
        name.value = ""
        surname.value = ""
        employment_status.value = ""
        educational_status.value = ""
        age.value = 0

    ui.button(text="Add Household Member", on_click=lambda: add_household_member_on_click())


# Donor Part


@ui.page("/donor-menu", title="Donor Menu")
def donor_menu():
    ui.button(text="Log Out", on_click=lambda: logout())
    ui.button(text="Manage Account", on_click=lambda: ui.navigate.to("/manage-account"))
    donation_columns = [
        {"name": "type_of_donation", "label": "Type of Donation", "field": "type_of_donation"},
        {"name": "amount", "label": "Amount", "field": "amount"},
        {"name": "area", "label": "Area", "field": "area"},
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "shipment_request_id", "label": "Shipment Request ID", "field": "shipment_request_id"}
    ]
    shipment_request_columns = [
        {"name": "address", "label": "Address", "field": "address"},
        {"name": "self_shipped", "label": "Self Shipped", "field": "self_shipped"},
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "donation_id", "label": "Donation ID", "field": "donation_id"}
    ]
    current_donor = dbm.getDonorByID(app.storage.user["id"])
    if current_donor is None:
        ui.notify("Identification failed.")
    elif current_donor.isPasswordCorrect(app.storage.user["password"]):
        donation_table = ui.table(columns=donation_columns, rows=[], pagination=10)
        ui.button(text="Add Donation",
                  on_click=lambda: ui.navigate.to("/add-donation"))
        shipment_request_table = ui.table(columns=shipment_request_columns, rows=[], pagination=10)
        ui.button(text="Add Shipment Request",
                  on_click=lambda: ui.navigate.to("/add-shipment-request"))
        for i in current_donor.getDonations():
            donation_table.add_rows({
                    "type_of_donation": i.getTypeOfDonation(),
                    "amount": i.getAmount(),
                    "area": i.getArea(),
                    "id": i.getID(),
                    "shipment_request_id": i.getShipmentRequestID()})
        for i in current_donor.getShipmentRequests():
            shipment_request_table.add_rows({
                "address": i.getAddress(),
                "self_shipped": i.isSelfShipped(),
                "id": i.getID(),
                "donation_id": i.getDonationID()
                })
    else:
        ui.notify("Identification failed.")


@ui.page("/add-donation", title="Add Donation")
def add_donation():
    ui.button(text="Go Back", on_click=lambda: ui.navigate.to("/donor-menu"))
    current_donor = dbm.getDonorByID(app.storage.user["id"])
    if current_donor is None:
        ui.notify("Identification failed.")
    elif current_donor.isPasswordCorrect(app.storage.user["password"]):
        type_of_donation = ui.input(label="Type of Donation")
        amount = ui.number(label="Amount", precision=2, value=0.0)
        area = ui.input(label="Area")

        def add_donation_button_on_click():
            dbm.addDonation(type_of_donation.value,
                            float(amount.value),
                            area.value,
                            current_donor)
            ui.navigate.to("/donor-menu")

        ui.button(text="Add Donation",
                  on_click=lambda: add_donation_button_on_click())
    else:
        ui.notify("Identification failed.")


@ui.page("/add-shipment-request", title="Add Shipment Request")
def add_shipment_request():
    ui.button(text="Go Back", on_click=lambda: ui.navigate.to("/donor-menu"))
    donation_columns = [
        {"name": "type_of_donation", "label": "Type of Donation", "field": "type_of_donation"},
        {"name": "amount", "label": "Amount", "field": "amount"},
        {"name": "area", "label": "Area", "field": "area"},
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "shipment_request_id", "label": "Shipment Request ID", "field": "shipment_request_id"}
    ]
    current_donor = dbm.getDonorByID(app.storage.user["id"])
    if current_donor is None:
        ui.notify("Identification failed.")
    elif current_donor.isPasswordCorrect(app.storage.user["password"]):
        address = ui.textarea(label="Address")
        selfShipped_or_shippedByNGO = ui.toggle(
                ["Self Shipped", "Shipped by NGO"],
                value="Self Shipped")
        donation_table = ui.table(columns=donation_columns, rows=[], pagination=10)
        for i in current_donor.getDonations():
            donation_table.add_rows({
                    "type_of_donation": i.getTypeOfDonation(),
                    "amount": i.getAmount(),
                    "area": i.getArea(),
                    "id": i.getID(),
                    "shipment_request_id": i.getShipmentRequestID()})

        def donation_table_on_row_click(e):
            selected_row = e.args[1]
            donation_id.value = selected_row["id"]

        donation_table.on("rowClick", lambda e: donation_table_on_row_click(e))
        donation_id = ui.number(label="Donation ID", precision=0, value=0)

        def add_shipment_request_button_on_click():
            current_donation = current_donor.getDonationByID(donation_id.value)
            if current_donation is None:
                ui.notify("Donation ID isn't found.")
            else:
                if selfShipped_or_shippedByNGO.value == "Self Shipped":
                    dbm.addShipmentRequest(address.value,
                                           True,
                                           current_donation,
                                           current_donor)
                elif selfShipped_or_shippedByNGO.value == "Shipped by NGO":
                    dbm.addShipmentRequest(address.value,
                                           False,
                                           current_donation,
                                           current_donor)
                ui.navigate.to("/donor-menu")

        ui.button(text="Add Shipment Request",
                  on_click=lambda: add_shipment_request_button_on_click())
    else:
        ui.notify("Identification failed.")


# Volunteer Part


@ui.page("/volunteer-menu", title="Volunteer Menu")
def volunteer_menu():
    ui.button(text="Log Out", on_click=lambda: logout())
    ui.button(text="Manage Account", on_click=lambda: ui.navigate.to("/manage-account"))
    current_volunteer = dbm.getVolunteerByID(app.storage.user["id"])
    if current_volunteer is None:
        ui.notify("Identification failed.")
    elif current_volunteer.isPasswordCorrect(app.storage.user["password"]):
        ui.button(text="Set Personal Profile",
                  on_click=lambda: ui.navigate.to("/set-personal-profile"))
        ui.button(text="View Aid Operations",
                  on_click=lambda: ui.navigate.to("/view-aid-operations"))
    else:
        ui.notify("Identification failed.")


@ui.page("/set-personal-profile", title="Set Personal Profile")
def set_personal_profile():
    ui.button(text="Go Back", on_click=lambda: ui.navigate.to("/volunteer-menu"))
    current_volunteer = dbm.getVolunteerByID(app.storage.user["id"])
    if current_volunteer is None:
        ui.notify("Identification failed.")
    elif current_volunteer.isPasswordCorrect(app.storage.user["password"]):
        current_personal_profile = current_volunteer.getPersonalProfile()
        profession = ui.input(label="Profession",
                              value=current_personal_profile.getProfession())
        average_annual_income = ui.number(label="Average Annual Income",
                                          precision=2,
                                          value=current_personal_profile.getAverageAnnualIncome())
        selected_region = ui.input(label="Selected Region",
                                   value=current_personal_profile.getSelectedRegion())
        transportation_support = ui.input(label="Transportation Support",
                                          value=current_personal_profile.getTransportationSupport())
        availability = ui.input(label="Availability",
                                value=current_personal_profile.getAvailability())

        def set_personal_profile_on_click():
            dbm.addPersonalProfile(profession.value,
                                   float(average_annual_income.value),
                                   selected_region.value,
                                   transportation_support.value,
                                   availability.value,
                                   False,
                                   current_volunteer)
            ui.navigate.to("/volunteer-menu")
        ui.button("Set Personal Profile", on_click=lambda: set_personal_profile_on_click())
    else:
        ui.notify("Identification failed.")


@ui.page("/view-aid-operations", title="View Aid Operations")
def view_aid_operations():
    ui.button(text="Go Back", on_click=lambda: ui.navigate.to("/volunteer-menu"))
    ship_items_operations_columns = [{"name": "id", "label": "ID", "field": "id"},
                                     {"name":"address", "label": "Address", "field": "address"},
                                     {"name": "destination_address", "label": "Destination Address", "field": "destination_address"}
                                     ]
    collect_items_operations_columns = [{"name": "id", "label": "ID", "field": "id"},
                                     {"name":"address", "label": "Address", "field": "address"},
                                     {"name": "destination_address", "label": "Destination Address", "field": "destination_address"}
                                     ] 
    public_event_operations_columns = [{"name": "id", "label": "ID", "field": "id"},
                                       {"name": "event_name", "label": "Event Name", "field": "event_name"},
                                       {"name": "address", "label": "Address", "field": "address"}]
    current_volunteer=dbm.getVolunteerByID(app.storage.user["id"])
    if current_volunteer is None:
        ui.notify("Identification failed.")
    elif current_volunteer.isPasswordCorrect(app.storage.user["password"]):
        if current_volunteer.getPersonalProfile() is None:
            ui.notify("Personal Profile not accepted.")
        elif current_volunteer.getPersonalProfile().getAccepted() == True:
            ui.label("Collect Items Operations")
            collect_items_operations = ui.table(columns=collect_items_operations_columns, rows=[], pagination=5)
            ui.label("Ship Items Operations")
            ship_items_operations = ui.table(columns=ship_items_operations_columns, rows=[], pagination=5)
            ui.label("Public Event Operations")
            public_event_operations = ui.table(columns=public_event_operations_columns, rows=[], pagination=5)
            for i in dbm.getAidOperations():
                if isinstance(i, ship_items_operation.ShipItemsOperation):
                    ship_items_operations.add_rows({"id": i.getID(),
                                                    "address": i.getAddress(),
                                                    "destination_address": i.getDestinationAddress()})
                elif isinstance(i, collect_items_operation.CollectItemsOperation):
                    collect_items_operations.add_rows({"id": i.getID(),
                                                    "address": i.getAddress(),
                                                    "destination_address": i.getDestinationAddress()})
                elif isinstance(i, public_event_operation.PublicEventOperation):
                    public_event_operations.add_rows({"id": i.getID(),
                                                    "event_name": i.getEventName(),
                                                    "address": i.getAddress()})
        else:
            ui.notify("Personal Profile not accepted.")

    else:
        ui.notify("Identification failed.")


# Operation Coordinator Part


@ui.page("/operation-coordinator-menu", title="Operation Coordinator Menu")
def operation_coordinator_menu():
    item_operations_columns = [
            {"name": "id", "label": "ID", "field": "id"},
            {"name": "address", "label": "Address", "field": "address"},
            {"name": "destination_address", "label": "Destination Address", "field": "destination_address"},
            ]
    event_operations_columns = [
            {"name": "id", "label": "ID", "field": "id"},
            {"name": "event_name", "label": "Public Event Name", "field": "event_name"},
            {"name": "address", "label": "Event Address", "field": "address"}
            ]
    ui.button(text="Log Out", on_click=lambda: logout())
    ui.button(text="Manage Account", on_click=lambda: ui.navigate.to("/manage-account"))
    current_operation_coordinator = dbm.getOperationCoordinatorByID(app.storage.user["id"])
    if current_operation_coordinator is None:
        ui.notify("Identification failed")
    elif current_operation_coordinator.isPasswordCorrect(app.storage.user["password"]):
        ui.label("Collect Items Operations")
        collect_items_operations_table = ui.table(columns=item_operations_columns, rows=[], pagination=5)
        ui.label("Ship Items Operations")
        ship_items_operations_table = ui.table(columns=item_operations_columns, rows=[], pagination=5)
        ui.label("Public Event Operations")
        event_operations_table = ui.table(columns=event_operations_columns, rows=[], pagination=5)
        for i in current_operation_coordinator.getAidOperations():
            if isinstance(i, collect_items_operation.CollectItemsOperation):
                collect_items_operations_table.add_rows({
                    "address": i.getAddress(),
                    "destination_address": i.getDestinationAddress(),
                    "id": i.getID()
                    })
            elif isinstance(i, ship_items_operation.ShipItemsOperation):
                ship_items_operations_table.add_rows({
                    "address": i.getAddress(),
                    "destination_address": i.getDestinationAddress(),
                    "id": i.getID()
                    })
            elif isinstance(i, public_event_operation.PublicEventOperation):
                event_operations_table.add_rows({
                    "event_name": i.getEventName(),
                    "address": i.getAddress(),
                    "id": i.getID()
                    })
        ui.button(text="Add Collect Items Operation", on_click=lambda: ui.navigate.to("/add-collect-items-operation"))
        ui.button(text="Add Ship Items Operation", on_click=lambda: ui.navigate.to("/add-ship-items-operation"))
        ui.button(text="Add Public Event Operation", on_click=lambda: ui.navigate.to("/add-public-event-operation"))
        ui.button(text="View Aid Registrations", on_click=lambda: ui.navigate.to("/view-aid-registrations"))
        ui.button(text="View Donations", on_click=lambda: ui.navigate.to("/view-donations"))
    else:
        ui.notify("Identification failed.")


@ui.page("/add-collect-items-operation", title="Add Collect Items Operation")
def add_collect_items_operation():
    ui.button(text="Go Back", on_click=lambda: ui.navigate.to("/operation-coordinator-menu"))
    current_operation_coordinator = dbm.getOperationCoordinatorByID(app.storage.user["id"])
    if current_operation_coordinator is None:
        ui.notify("Identification failed.")
    elif current_operation_coordinator.isPasswordCorrect(app.storage.user["password"]):
        address = ui.input(label="Address")
        destination_address = ui.input(label="Destination Address")

        def add_collect_items_operation_button_on_click():
            dbm.addCollectItemsOperation(address.value,
                                         destination_address.value,
                                         current_operation_coordinator)
            ui.navigate.to("/operation-coordinator-menu")

        ui.button(text="Add Collect Items Operation",
                  on_click=lambda: add_collect_items_operation_button_on_click())
    else:
        ui.notify("Identification failed.")


@ui.page("/add-ship-items-operation", title="Add Ship Items Operation")
def add_ship_items_operation():
    ui.button(text="Go Back", on_click=lambda: ui.navigate.to("/operation-coordinator-menu"))
    current_operation_coordinator = dbm.getOperationCoordinatorByID(app.storage.user["id"])
    if current_operation_coordinator is None:
        ui.notify("Identification failed.")
    elif current_operation_coordinator.isPasswordCorrect(app.storage.user["password"]):
        address = ui.input(label="Address")
        destination_address = ui.input(label="Destination Address")

        def add_ship_items_operation_button_on_click():
            dbm.addShipItemsOperation(address.value,
                                      destination_address.value,
                                      current_operation_coordinator)
            ui.navigate.to("/operation-coordinator-menu")

        ui.button(text="Add Ship Items Operation",
                  on_click=lambda: add_ship_items_operation_button_on_click())
    else:
        ui.notify("Identification failed.")


@ui.page("/add-public-event-operation", title="Add Public Event Operation")
def add_public_event_operation():
    ui.button(text="Go Back", on_click=lambda: ui.navigate.to("/operation-coordinator-menu"))
    current_operation_coordinator = dbm.getOperationCoordinatorByID(app.storage.user["id"])
    if current_operation_coordinator is None:
        ui.notify("Identification failed.")
    elif current_operation_coordinator.isPasswordCorrect(app.storage.user["password"]):
        event_name = ui.input(label="Event Name")
        address = ui.input(label="Address")

        def add_public_event_operation_button_on_click():
            dbm.addPublicEventOperation(address.value,
                                        event_name.value,
                                        current_operation_coordinator)
            ui.navigate.to("/operation-coordinator-menu")

        ui.button(text="Add Public Event Operation",
                  on_click=lambda: add_public_event_operation_button_on_click())
    else:
        ui.notify("Identification failed.")


@ui.page("/view-aid-registrations", title="View Aid Registrations")
def view_aid_registrations():
    ui.button(text="Go Back", on_click=lambda: ui.navigate.to("/operation-coordinator-menu"))
    aid_registrations_columns=[
            {"name": "id", "label": "ID", "field": "id"},
            {"name": "number_of_children","label": "Number Of Children","field": "number_of_children"},
            {"name": "monthly_income", "label": "Monthly Income", "field": "monthly_income"},
            {"name": "address", "label": "Address", "field": "address"},
            {"name": "monthly_expenditures", "label": "Monthly Expenditures", "field": "monthly_expenditures"},
            {"name": "nature_of_support_needed", "label": "Nature of Support Needed", "field": "nature_of_support_needed"}
            ]
    household_members_columns=[
            {"name": "name", "label": "Name", "field": "name"},
            {"name": "surname", "label": "Surname", "field": "surname"},
            {"name": "employment_status", "label": "Employment Status", "field": "employment_status"},
            {"name": "educational_status", "label": "Educational Status", "field": "educational_status"},
            {"name": "age", "label": "Age", "field": "age"}
            ]
    current_operation_coordinator = dbm.getOperationCoordinatorByID(app.storage.user["id"])
    if current_operation_coordinator is None:
        ui.notify("Identification failed.")
    elif current_operation_coordinator.isPasswordCorrect(app.storage.user["password"]):
        aid_registrations_table = ui.table(columns=aid_registrations_columns, rows=[], pagination=10)
        def selected_aid_registration_id_on_change():
            input = int(selected_aid_registration_id.value)
            household_members_table.clear()
            if dbm.getAidRegistrationByID(input) is None:
                return
            for i in dbm.getAidRegistrationByID(input).getHouseholdMembers():
                household_members_table.add_rows({"name": i.getName(),
                                                  "surname": i.getSurname(),
                                                  "employment_status": i.getEmploymentStatus(),
                                                  "educational_status": i.getEducationalStatus(),
                                                  "age": i.getAge()})

        selected_aid_registration_id = ui.number(label="Selected Aid Registration ID", precision=0, value=0, on_change=lambda: selected_aid_registration_id_on_change())
        household_members_table = ui.table(columns=household_members_columns, rows=[], pagination=10)
        for i in dbm.getAidRegistrations():
            aid_registrations_table.add_rows({"id": i.getID(),
                                              "number_of_children": i.getNumberOfChildren(),
                                              "monthly_income": i.getMonthlyIncome(),
                                              "address": i.getAddress(),
                                              "monthly_expenditures": i.getMonthlyExpenditures(),
                                              "nature_of_support_needed": i.getNatureOfSupportNeeded()})

        def aid_registrations_table_on_row_click(e):
            selected_row = e.args[1]
            selected_aid_registration_id.value = selected_row["id"]
 
        aid_registrations_table.on("rowClick",lambda e: aid_registrations_table_on_row_click(e))
    else:
        ui.notify("Identification failed.")


@ui.page("/view-donations", title="View Donations")
def view_donations():
    ui.button(text="Go Back", on_click=lambda: ui.navigate.to("/operation-coordinator-menu"))
    donation_columns = [
        {"name": "type_of_donation", "label": "Type of Donation", "field": "type_of_donation"},
        {"name": "amount", "label": "Amount", "field": "amount"},
        {"name": "area", "label": "Area", "field": "area"},
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "shipment_request_id", "label": "Shipment Request ID", "field": "shipment_request_id"}
    ]
    shipment_request_columns = [
        {"name": "address", "label": "Address", "field": "address"},
        {"name": "self_shipped", "label": "Self Shipped", "field": "self_shipped"},
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "donation_id", "label": "Donation ID", "field": "donation_id"}
    ]

    current_operation_coordinator = dbm.getOperationCoordinatorByID(app.storage.user["id"])
    if current_operation_coordinator is None:
        ui.notify("Identification failed.")
    elif current_operation_coordinator.isPasswordCorrect(app.storage.user["password"]):
        donations_table = ui.table(columns = donation_columns, rows=[], pagination=10)
        shipment_requests_table = ui.table(columns = shipment_request_columns, rows=[], pagination=10)
        for i in dbm.getDonations():
            donations_table.add_rows({
                    "type_of_donation": i.getTypeOfDonation(),
                    "amount": i.getAmount(),
                    "area": i.getArea(),
                    "id": i.getID(),
                    "shipment_request_id": i.getShipmentRequestID()})
        for i in dbm.getShipmentRequests():
            shipment_requests_table.add_rows({
                "address": i.getAddress(),
                "self_shipped": i.isSelfShipped(),
                "id": i.getID(),
                "donation_id": i.getDonationID()
                })
    else:
        ui.notify("Identification failed.")


# System Administrator Part


@ui.page("/system-administrator-menu", title="System Administrator Menu")
def system_administrator_menu():
    ui.button(text="Log Out", on_click=lambda: logout())
    ui.button(text="Manage Account", on_click=lambda: ui.navigate.to("/manage-account"))
    current_system_administrator = dbm.getSystemAdministratorByID(app.storage.user["id"])
    if current_system_administrator is None:
        ui.notify("Identification failed.")
    elif current_system_administrator.isPasswordCorrect(app.storage.user["password"]):
        ui.button(text="Check Personal Profiles",
                  on_click=lambda: ui.navigate.to("/check-personal-profiles"))
        ui.button(text="Manage Users",
                  on_click=lambda: ui.navigate.to("/manage-users"))
    else:
        ui.notify("Identification failed.")


@ui.page("/check-personal-profiles", title="Check Personal Profiles")
def check_personal_profiles():
    ui.button(text="Go Back", on_click=lambda: ui.navigate.to("/system-administrator-menu"))
    accepted_personal_profile_columns = [
            {"name": "username", "label": "Name", "field": "username"},
            {"name": "user_id", "label": "User ID", "field": "user_id"},
            {"name": "profession", "label": "Profession", "field": "profession"},
            {"name": "average_annual_income", "label": "Average Annual Income", "field": "average_annual_income"},
            {"name": "selected_region", "label": "Selected Region", "field": "selected_region"},
            {"name": "transportation_support", "label": "Transportation Support", "field": "transportation_support"},
            {"name": "availability", "label": "Availability", "field": "availability"}
            ]
    current_system_administrator = dbm.getSystemAdministratorByID(app.storage.user["id"])

    if current_system_administrator is None:
        ui.notify("Identification failed.")
    elif current_system_administrator.isPasswordCorrect(app.storage.user["password"]):
        ui.label(text="Accepted Personal Profiles")
        accepted_personal_profiles = ui.table(columns=accepted_personal_profile_columns, rows=[], pagination=10)
        ui.label(text="Unaccepted Personal Profiles")
        unaccepted_personal_profiles = ui.table(columns=accepted_personal_profile_columns, rows=[], pagination=10)
        for i in dbm.getPersonalProfiles():
            current_volunteer = dbm.getVolunteerByID(i.getVolunteerID())
            if i.getAccepted():
                accepted_personal_profiles.add_rows({
                    "username": current_volunteer.getUsername(),
                    "user_id": i.getVolunteerID(),
                    "profession": i.getProfession(),
                    "average_annual_income": i.getAverageAnnualIncome(),
                    "selected_region": i.getSelectedRegion(),
                    "transportation_support": i.getTransportationSupport(),
                    "availability": i.getAvailability()
                    })
            elif not i.getAccepted():
                unaccepted_personal_profiles.add_rows({
                    "username": current_volunteer.getUsername(),
                    "user_id": i.getVolunteerID(),
                    "profession": i.getProfession(),
                    "average_annual_income": i.getAverageAnnualIncome(),
                    "selected_region": i.getSelectedRegion(),
                    "transportation_support": i.getTransportationSupport(),
                    "availability": i.getAvailability()
                    })

        def unaccepted_personal_profiles_on_row_click(e):
            selected_row = e.args[1]
            accept_id.value = selected_row["user_id"]

        unaccepted_personal_profiles.on("rowClick", lambda e: unaccepted_personal_profiles_on_row_click(e))

        accept_id = ui.number(label="ID to be accepted", precision=0, value=0)

        def accept_button_on_click():
            current_personal_profile = dbm.getVolunteerByID(int(accept_id.value))
            if current_personal_profile is None:
                ui.notify("The specified profile couldn't be found.")
            else:
                current_personal_profile.getPersonalProfile().setAccepted(True)
                ui.navigate.to("/check-personal-profiles")

        ui.button(text="Accept", on_click=lambda: accept_button_on_click())
    else:
        ui.notify("Identification failed.")


@ui.page("/manage-users", title="Manage Users")
def manage_users():
    ui.button(text="Go Back", on_click=lambda: ui.navigate.to("/system-administrator-menu"))
    user_table_columns = [
            {"name": "type", "label": "Type", "field": "type"},
            {"name": "username", "label": "Username", "field": "username"},
            {"name": "name", "label": "Name", "field": "name"},
            {"name": "surname", "label": "Surname", "field": "surname"},
            {"name": "email", "label": "Email", "field": "email"},
            {"name": "id", "label": "ID", "field": "id"}
            ]
    current_system_administrator = dbm.getSystemAdministratorByID(app.storage.user["id"])
    if current_system_administrator is None:
        ui.notify("Identification failed.")
    elif current_system_administrator.isPasswordCorrect(app.storage.user["password"]):
        users = ui.table(columns=user_table_columns, rows=[], pagination=10)
        for i in dbm.getUsers():
            output_type = ""
            if isinstance(i, donor.Donor):
                output_type = "Donor"
            elif isinstance(i, volunteer.Volunteer):
                output_type = "Volunteer"
            elif isinstance(i, operation_coordinator.OperationCoordinator):
                output_type = "Operation Coordinator"
            elif isinstance(i, system_administrator.SystemAdministrator):
                output_type = "System Administrator"
            users.add_rows({"type": output_type,
                            "username": i.getUsername(),
                            "name": i.getName(),
                            "surname": i.getSurname(),
                            "email": i.getEmail(),
                            "id": i.getID()})

        def users_on_row_click(e):
            selected_row = e.args[1]
            to_remove_input.value = selected_row["id"]

        users.on("rowClick", lambda e: users_on_row_click(e))
        to_remove_input = ui.number(label="ID to be removed", precision=0, value=0)

        def remove_user_button_on_click():
            dbm.removeUser(dbm.getUserByID(int(to_remove_input.value)))
            ui.navigate.to("/manage-users")

        ui.button(text="Remove User", on_click=lambda: remove_user_button_on_click())
        ui.button(text="Add User", on_click=lambda: ui.navigate.to("/add-user"))
    else:
        ui.notify("Identification failed.")


@ui.page("/add-user", title="Add User")
def add_user():
    current_system_administrator = dbm.getSystemAdministratorByID(app.storage.user["id"])
    if current_system_administrator is None:
        ui.notify("Identification failed.")
    elif current_system_administrator.isPasswordCorrect(app.storage.user["password"]):
        username = ui.input(label="Username")
        name = ui.input(label="Name")
        surname = ui.input(label="Surname")
        password = ui.input(label="Password",
                            password=True,
                            password_toggle_button=True)
        password_again = ui.input(label="Password Again",
                                  password=True,
                                  password_toggle_button=True)
        email = ui.input(label="Email")
        user_type = ui.toggle(["Donor", "Volunteer", "Operation Coordinator", "System Administrator"], value="Donor")

        def add_user_on_click():
            ui.notify("clicked")
            if password.value == password_again.value:
                if user_type.value == "Donor":
                    dbm.addDonor(username.value,
                                 password.value,
                                 name.value,
                                 surname.value,
                                 email.value)
                elif user_type.value == "Volunteer":
                    dbm.addVolunteer(username.value,
                                     password.value,
                                     name.value,
                                     surname.value,
                                     email.value)
                elif user_type.value == "Operation Coordinator":
                    dbm.addOperationCoordinator(username.value,
                                                password.value,
                                                name.value,
                                                surname.value,
                                                email.value)
                elif user_type.value == "System Administrator":
                    dbm.addSystemAdministrator(username.value,
                                               password.value,
                                               name.value,
                                               surname.value,
                                               email.value)
                ui.notify("User added")
                ui.navigate.to("/manage-users")
            else:
                ui.notify("Passwords don't match")

        ui.button(text="Add User", on_click=lambda: add_user_on_click())
    else:
        ui.notify("Identification failed.")


# Start the Program


dbm.addDonor("stingy", "ilikemoney", "Stingy", "Donor", "bestemail@email.com")
dbm.addOperationCoordinator("worker", "hatemyjob", "Donus", "Lifus", "donus.lifus@email.com")
dbm.addSystemAdministrator("admin", "password", "Adminus", "Surnamus", "admin@email.com")
dbm.addVolunteer("helper", "ilikehelping", "Helpy", "Helpinus", "helper@email.com")
ui.run(storage_secret="Don't tell this storage secret to anyone plsplspls. No one can guess it.  ")
