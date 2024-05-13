from ..backend import database_manager
from nicegui import ui


class GUIManager:
    def __init__(self, database_manager_input: database_manager.DatabaseManager):
        self.dbm: database_manager.DatabaseManager = database_manager_input

    @ui.page("/login")
    def login(self):
        username=ui.input(label = "Username")
        password=ui.input(label = "Password", password = True, password_toggle_button = True)
        ui.button(text="Log in")
        ui.button(text="Sign up")
        ui.button(text="Aid Registration")
    
    @ui.page("/aid-registration-form")
    def aid_registration_form(self):

        pass

    @ui.page("/register")
    def register(self):
        username=ui.input(label="Username")
        name=ui.input(label="Name")
        surname=ui.input(label="Surname")
        password1=ui.input(label="Password", password = True, password_toggle_button = True)
        password2=ui.input(label="Password Again", password = True, password_toggle_button = True)
        email=ui.input(label="Email")
        donor_or_volunteer=ui.toggle(["Donor","Volunteer"], value = "Donor")
        ui.button(text="Sign up",
                  on_click=lambda:
                  if password1.value==password2.value:
                    
                  else:
                    ui.notify("Passwords don't match.")
                                                        
                  
                  )

