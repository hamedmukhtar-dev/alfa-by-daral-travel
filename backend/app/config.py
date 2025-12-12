import os


class Settings:
    # --------------------
    # Core
    # --------------------
    APP_ENV = os.getenv("APP_ENV", "pilot")  # pilot | production
    PILOT_MODE = APP_ENV == "pilot"

    # --------------------
    # Pilot Controls
    # --------------------
    ENABLE_FREE_SERVICES = os.getenv("ENABLE_FREE_SERVICES", "true").lower() == "true"
    ENABLE_OFFLINE_PAYMENTS = os.getenv("ENABLE_OFFLINE_PAYMENTS", "true").lower() == "true"

    # --------------------
    # Safety
    # --------------------
    MAX_OFFLINE_PAYMENT_AMOUNT = float(os.getenv("MAX_OFFLINE_PAYMENT_AMOUNT", "1000"))
    REQUIRE_ADMIN_APPROVAL = True

    # --------------------
    # Info
    # --------------------
    PLATFORM_NAME = "ALFA by Daral Travel"


settings = Settings()
