import allure
import pytest
from framework.constants import (
    PLATFORMS,
    USER_IDS,
    BAD_USER_ID,
    NONEXISTENT_DEVICE_ID,
    EXPECTED_STATUS,
    CODE_OK,
)
from framework.checkers import (
    get_data_and_check_expect_platform_and_user_id_rest,
    check_status,
)


@allure.suite("REST")
@allure.title("Basic get_device test with different input parameters")
@pytest.mark.parametrize(
    "platform, user_id",
    [
        (PLATFORMS[1], USER_IDS[2]),
        (PLATFORMS[1], USER_IDS[1]),
        (PLATFORMS[2], USER_IDS[2]),
    ],
)
def test_get_device(device_api, platform, user_id):
    with allure.step("Basic create device"):
        status_code, device_id = device_api.create_device(platform, user_id)

    with allure.step("Check the expected status code"):
        check_status(status_code, CODE_OK)
    with allure.step("Check expected parameters after get_device"):
        get_data_and_check_expect_platform_and_user_id_rest(
            device_id, platform, user_id
        )


@allure.suite("REST")
@allure.title("Basic update_device test with different input parameters")
@pytest.mark.parametrize(
    "platform, user_id",
    [
        (PLATFORMS[1], USER_IDS[1]),
        (PLATFORMS[1], USER_IDS[2]),
        (PLATFORMS[2], USER_IDS[2]),
    ],
)
def test_update_device(device_api, device, platform, user_id):
    with allure.step("Basic update_device with provided parameters"):
        status_code, _ = device_api.update_device(
            platform=platform, user_id=user_id, device_id=device
        )
    with allure.step("Check the expected status code"):
        check_status(status_code, CODE_OK)
    with allure.step("Check expected parameters after update_device"):
        get_data_and_check_expect_platform_and_user_id_rest(device, platform, user_id)


@allure.suite("REST")
@allure.title("update_device test with bad user id")
def test_update_device_bad_input(device_api, device):
    with allure.step("Try to update device with bad input parameters"):
        status_code, update_status = device_api.update_device(
            platform=PLATFORMS[1], user_id=BAD_USER_ID, device_id=device
        )
    with allure.step("Check the expected status code"):
        check_status(status_code, EXPECTED_STATUS["BAD_INPUT"]["REST"])


@allure.suite("REST")
@allure.title("update_device test with non-existent device id")
def test_update_nonexistent_device(device_api):
    with allure.step("Try to update non-existent device"):
        status_code, update_status = device_api.update_device(
            platform=PLATFORMS[1],
            user_id=USER_IDS[1],
            device_id=NONEXISTENT_DEVICE_ID,
        )
    with allure.step("Check the expected status code"):
        check_status(status_code, CODE_OK)
    with allure.step("Check the expected 'success' variable value"):
        check_status(update_status, EXPECTED_STATUS["NONEXISTENT_DEVICE"]["REST"])
