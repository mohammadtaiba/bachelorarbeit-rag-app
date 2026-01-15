# tests/integration/conftest.py
import os

# ******************************************************************
# Hard-Crash (Access Violation) – komplett “wegkonfigurieren”
os.environ["ANONYMIZED_TELEMETRY"] = "FALSE"
# ******************************************************************

