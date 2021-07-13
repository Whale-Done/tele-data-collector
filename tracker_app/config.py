# config database uri here
# it is ignored during commits, change gitignore to enable commits

class DeployConfig:
    USER_APP_NAME = "Tracker"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False  # Disable email authentication
    USER_ENABLE_USERNAME = True  # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False
    # for deploy
    REDIS_URL = "redis://:p22272393a04e83e3c4b7cbe21faa98ac3d93cf57e55203ffa43eef0f3a2d5113@ec2-54-205-43-29.compute-1.amazonaws.com:11780"
    SQLALCHEMY_DATABASE_URI = 'postgres://rqadiwolwnxpvg:544cfa8b90aa0ab5ad9d5f48b73c986ad67ac4d67183d9900cfe6dcb022f8a1c@ec2-52-6-77-239.compute-1.amazonaws.com:5432/d2h2q50nlgqs5l'
    # for debug
    # REDIS_URL = "redis://leipetushood:1234567890@localhost:6379"
    # SQLALCHEMY_DATABASE_URI = 'postgresql://leipetushood:1234567890@localhost:5432/whalemoney'


class DebugConfig:
    USER_APP_NAME = "Tracker"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False  # Disable email authentication
    USER_ENABLE_USERNAME = True  # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False
    REDIS_URL = "redis://leipetushood:1234567890@localhost:6379"
    SQLALCHEMY_DATABASE_URI = 'postgresql://cairong:chonkyboilaptop@localhost:5432/whalemoney'
