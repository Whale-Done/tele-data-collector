# config database uri here
# it is ignored during commits, change gitignore to enable commits

class Config:
    USER_APP_NAME = "Tracker"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False  # Disable email authentication
    USER_ENABLE_USERNAME = True  # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False