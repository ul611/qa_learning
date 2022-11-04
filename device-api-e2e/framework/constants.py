from datetime import timedelta

from requests import codes


PLATFORMS = ["IOS", "Windows", "Linux"]
USER_IDS = ["13", "14", "15"]

EXPECTED_STATUS = {
    "BAD_INPUT": {"GRPC": "5", "REST": codes.bad_request},
    "NONEXISTENT_DEVICE": {"GRPC": "", "REST": "False"},
}

CODE_OK = codes.ok

NONEXISTENT_DEVICE_ID = 10000
BAD_USER_ID = "OLOLO"
BAD_USER_ID_GRPC = 0

PLATFORM_IOS = "IOS"
TOL = timedelta(microseconds=100000)
