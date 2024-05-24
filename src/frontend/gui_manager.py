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


@ui.page("/")
def start_page():
    ui.navigate.to("/login")


@ui.page("/login")
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
    ui.button(text="Aid Registration")


@ui.page("/register")
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
                dbm.Volunteer(username.value,
                              password1.value,
                              name.value,
                              surname.value,
                              email.value)
            ui.navigate.to("/login")
        else:
            ui.notify("Passwords don't match.")

    ui.button(text="Sign up", on_click=lambda: register_button_on_click())


@ui.page("/manage-account")
def manage_account():
    current_user = dbm.getUserByID(app.storage.user["id"])
    if current_user is None:
        ui.notify("Identification failed.")
    elif current_user.isPasswordCorrect(app.storage.user["password"]):
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


@ui.page("/aid-registration-form")
def aid_registration_form():
    pass


# Donor Part
@ui.page("/donor-menu")
def donor_menu():
    ui.button(text="Log Out", on_click=lambda: logout())
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
        donation_table = ui.table(columns=donation_columns, rows=[])
        ui.button(text="Add Donation",
                  on_click=lambda: ui.navigate.to("/add-donation"))
        shipment_request_table = ui.table(columns=shipment_request_columns, rows=[])
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


@ui.page("/add-donation")
def add_donation():
    current_donor = dbm.getDonorByID(app.storage.user["id"])
    if current_donor is None:
        ui.notify("Identification failed.")
    elif current_donor.isPasswordCorrect(app.storage.user["password"]):
        type_of_donation = ui.input(label="Type of Donation")
        amount = ui.input(label="Amount")
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


@ui.page("/add-shipment-request")
def add_shipment_request():
    current_donor = dbm.getDonorByID(app.storage.user["id"])
    if current_donor is None:
        ui.notify("Identification failed.")
    elif current_donor.isPasswordCorrect(app.storage.user["password"]):
        address = ui.input(label="Address")
        selfShipped_or_shippedByNGO = ui.toggle(
                ["Self Shipped", "Shipped by NGO"],
                value="Self Shipped")
        donation_id = ui.input(label="Donation ID")

        def add_shipment_request_button_on_click():
            current_donation = current_donor.getDonationByID(donation_id.value)
            if current_donation is None:
                ui.notify("Donation ID isn't found.")
            else:
                if selfShipped_or_shippedByNGO == "Self Shipped":
                    dbm.addShipmentRequest(address.value,
                                           True,
                                           current_donation,
                                           current_donor)
                elif selfShipped_or_shippedByNGO == "Shipped by NGO":
                    dbm.addShipmentRequest(address.value,
                                           False,
                                           current_donation,
                                           current_donor)

        ui.button(text="Add Shipment Request",
                  on_click=lambda: add_shipment_request_button_on_click())
    else:
        ui.notify("Identification failed.")

# Volunteer Part


@ui.page("/volunteer-menu")
def volunteer_menu():
    ui.button(text="Log Out", on_click=lambda: logout())
    current_volunteer = dbm.getVolunteerByID(app.storage.user["id"])
    if current_volunteer is None:
        ui.notify("Identification failed.")
    elif current_volunteer.isPasswordCorrect(app.storage.user["password"]):
        ui.button(text="Set Personal Profile",
                  on_click=ui.navigate.to("/set-personal-profile"))
    else:
        ui.notify("Identification failed.")


@ui.page("/set-personal-profile")
def set_personal_profile():
    current_volunteer = dbm.getVolunteerByID(app.storage.user["id"])
    if current_volunteer is None:
        ui.notify("Identification failed.")
    elif current_volunteer.isPasswordCorrect(app.storage.user["password"]):
        current_personal_profile = current_volunteer.getPersonalProfile()
        profession = ui.input(label="Profession",
                              value=current_personal_profile.getProfession())
        average_annual_income = ui.input(label="Average Annual Income",
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
                                   current_personal_profile)
    else:
        ui.notify("Identification failed.")

# Operation Coordinator Part


@ui.page("/operation-coordinator-menu")
def operation_coordinator_menu():
    item_operations_columns=[
            {"name": "type_of_operation", "label": "Type Of Operation", "field": "type_of_operation"},
            {"name": "address", "label": "Address", "field": "address"},
            {"name": "destination_address", "label": "Destination Address", "field": "destination_address"},
            {"name": "id", "label": "ID", "field": "id"}
            ]
    event_operations_columns=[
            {"name": "event_name", "label":"Public Event Name", "field": "event_name"},
            {"name": "address", "label":"Event Address", "field": "address"},
            {"name": "id", "label": "ID", "field": "id"}
            ]
    ui.button(text="Log Out", on_click=lambda: logout())
    current_operation_coordinator = dbm.getOperationcoordinatorByID(app.storage.user["id"])
    if current_operation_coordinator is None:
        ui.notify("Identification failed")
    elif current_operation_coordinator.isPasswordCorrect(app.storage.user["password"]):
        item_operations_table = ui.table(columns=item_operations_columns, rows=[])
        event_operations_table = ui.table(columns=event_operations_columns, rows=[])
        for i in current_operation_coordinator.getAidOperations():
            if (
                isinstance(i, collect_items_operation.CollectItemsOperation)
                or
                isinstance(i, ship_items_operation.ShipItemsOperation)
            ):
                if isinstance(i, collect_items_operation.CollectItemsOperation):
                    item_operations_table.add_rows({
                        "type_of_operation": "Collect Items",
                        "address": i.getAddress(),
                        "destination_address": i.getDestinationAddress(),
                        "id": i.getID()
                        })
                elif isinstance(i, ship_items_operation.ShipItemsOperation):
                    item_operations_table.add_rows({
                            "type_of_operation": "Ship Items",
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
        ui.button(text="")
    else:
        ui.notify("Identification failed.")

# System Administrator Part


@ui.page("/system-administrator-menu")
def system_administrator_menu():
    ui.button(text="Log Out", on_click=lambda: logout())
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


@ui.page("/check-personal-profiles")
def check_personal_profiles():
    pass


@ui.page("/manage-users")
def manage_users():
    pass

# Start the Program


dbm.addDonor("test", "123", "abc", "def", "sjsj")
ui.run(storage_secret="Don't tell this storage secret to anyone plsplspls. No one can guess it.  ")
