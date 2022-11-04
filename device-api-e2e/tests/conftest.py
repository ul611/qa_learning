import allure
import pytest

from framework.rest.api import DeviceAPI
from framework.grpc.api import DeviceAPIGRPC
from config import HOST_REST, HOST_GRPC, TOKEN, DSN
from framework.constants import PLATFORMS, USER_IDS
from framework.sql.alchemy import Alchemy
from framework.sql.client import SQLDeviceApi


@pytest.fixture(scope="session")
def device_api():
    return DeviceAPI(HOST_REST, TOKEN)


@pytest.fixture(scope="session")
def device_api_grpc():
    return DeviceAPIGRPC(HOST_GRPC)


@pytest.fixture(scope="function")
def device(device_api):
    with allure.step("Create device in fixture"):
        _, device_id = device_api.create_device(
            platform=PLATFORMS[0], user_id=USER_IDS[0]
        )

    yield int(device_id)

    with allure.step("Delete device by id in fixture"):
        device_api.delete_device(device_id)


@pytest.fixture(scope="session")
def device_api_sql():
    return SQLDeviceApi(dsn=DSN)


@pytest.fixture(scope="session")
def device_api_orm():
    return Alchemy(dsn=DSN)


@pytest.fixture(scope="session")
def device_sql(device_api):
    with allure.step("Create device in fixture"):
        _, device_id = device_api.create_device(
            platform=PLATFORMS[0], user_id=USER_IDS[0]
        )

    yield int(device_id)

    with allure.step("Delete device by id in fixture"):
        device_api.delete_device(device_id)
