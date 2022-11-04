import allure
import pytest
from grpc import RpcError
from framework.constants import (
    PLATFORMS,
    USER_IDS,
    NONEXISTENT_DEVICE_ID,
    BAD_USER_ID_GRPC,
    EXPECTED_STATUS,
)
from framework.checkers import (
    get_data_and_check_expect_platform_and_user_id_grpc,
    check_status,
)


@allure.suite("gRPC")
@allure.title("Basic get_device test with different input parameters")
@pytest.mark.parametrize(
    "platform, user_id",
    [
        (PLATFORMS[1], int(USER_IDS[2])),
        (PLATFORMS[1], int(USER_IDS[1])),
        (PLATFORMS[2], int(USER_IDS[2])),
    ],
)
def test_get_device_grpc(device_api_grpc, platform, user_id):
    with allure.step("Basic create device"):
        device_data = device_api_grpc.create_device(platform, user_id)
    with allure.step("Check expected parameters after get_device"):
        get_data_and_check_expect_platform_and_user_id_grpc(
            device_data.device_id, platform, str(user_id)
        )


@allure.suite("gRPC")
@allure.title("get_device test with non-existent device id")
def test_get_nonexistent_device_grpc(device_api_grpc):
    with pytest.raises(RpcError) as exc_info:
        with allure.step("Try get_device with non-existent device id"):
            device_api_grpc.get_device(NONEXISTENT_DEVICE_ID)
        with allure.step("Check the expected status code"):
            check_status(exc_info.code(), EXPECTED_STATUS["BAD_INPUT"]["GRPC"])


@allure.suite("gRPC")
@allure.title("Basic update_device test with different input parameters")
@pytest.mark.parametrize(
    "platform, user_id",
    [
        (PLATFORMS[1], USER_IDS[2]),
        (PLATFORMS[1], USER_IDS[1]),
        (PLATFORMS[2], USER_IDS[2]),
    ],
)
def test_update_device_grpc(device_api_grpc, device, platform, user_id):
    with allure.step("Basic update_device with provided parameters"):
        _ = device_api_grpc.update_device(
            platform=platform, user_id=int(user_id), device_id=device
        )
    with allure.step("Check expected parameters after update_device"):
        get_data_and_check_expect_platform_and_user_id_grpc(device, platform, user_id)


@allure.suite("gRPC")
@allure.title("update_device test with bad user id")
def test_update_device_bad_input(device_api_grpc, device):
    with pytest.raises(RpcError) as exc_info:
        with allure.step("Try to update device with bad input parameters"):
            device_api_grpc.update_device(
                platform=PLATFORMS[1],
                user_id=BAD_USER_ID_GRPC,
                device_id=device,
            )
        with allure.step("Check the expected status code"):
            check_status(exc_info.code(), EXPECTED_STATUS["BAD_INPUT"]["GRPC"])


@allure.suite("gRPC")
@allure.title("update_device test with non-existent device id")
def test_update_nonexistent_device(device_api_grpc):
    with allure.step("Try to update non-existent device"):
        update_status = device_api_grpc.update_device(
            platform=PLATFORMS[1],
            user_id=int(USER_IDS[1]),
            device_id=NONEXISTENT_DEVICE_ID,
        )
    with allure.step("Check the expected answer after non-existent device id update"):
        check_status(update_status, EXPECTED_STATUS["NONEXISTENT_DEVICE"]["GRPC"])
