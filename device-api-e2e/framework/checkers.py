from datetime import datetime
from typing import List

import allure

from config import HOST_GRPC, HOST_REST, TOKEN
from hamcrest import assert_that, equal_to, none, less_than, is_in, not_

from framework.constants import TOL
from framework.rest.api import DeviceAPI
from framework.grpc.api import DeviceAPIGRPC
from framework.sql.act_device_api_models import DevicesEvent


def get_data_and_check_expect_platform_and_user_id_rest(
    device_id, expected_platform: str, expected_user: str
):
    """
    Function for REST update_device testing.
    """
    with allure.step("Create Device API REST"):
        _, device_data = DeviceAPI(host=HOST_REST, token=TOKEN).get_device(device_id)
    with allure.step("Get device platform"):
        actual_platform = device_data.platform
    with allure.step("Get device user id"):
        actual_user_id = device_data.userId
    with allure.step("Check the device platform is the same as at initialization"):
        assert_that(
            actual_platform,
            equal_to(expected_platform),
            f"Platform is {actual_platform}, not {expected_platform}",
        )
    with allure.step("Check the device user id is the same as at initialization"):
        assert_that(
            str(actual_user_id),
            equal_to(expected_user),
            f"UserID is {actual_user_id}, not {expected_user}",
        )


def get_data_and_check_expect_platform_and_user_id_grpc(
    device_id, expected_platform: str, expected_user: str
):
    """
    Function for gRPC update_device testing.
    """
    with allure.step("Create Device API gRPC"):
        device_data = DeviceAPIGRPC(host=HOST_GRPC).get_device(device_id)
    with allure.step("Get device platform"):
        actual_platform = device_data.value.platform
    with allure.step("Get device user id"):
        actual_user_id = device_data.value.user_id
    with allure.step("Check the device platform is the same as at initialization"):
        assert_that(
            actual_platform,
            equal_to(expected_platform),
            f"Platform is {actual_platform}, not {expected_platform}",
        )
    with allure.step("Check the device user id is the same as at initialization"):
        assert_that(
            str(actual_user_id),
            equal_to(expected_user),
            f"UserID is {actual_user_id}, not {expected_user}",
        )


def check_status(status_code, expected_status_code):
    """
    Function to check status code.
    """
    assert_that(
        str(status_code),
        equal_to(str(expected_status_code)),
        f"Status code is {status_code}, not {expected_status_code}",
    )


def check_sql_log(
    device_api_orm,
    expected_device_id: int,
    previous_entities: List[DevicesEvent] = [],
    len_diff: int = 1,
    expected_type: int or None = None,
    entered_at: bool = False,
    expected_user_id: int or None = None,
    expected_platform: str or None = None,
    empty_payload: bool = False,
):
    with allure.step("Get logs from database by device id"):
        current_entities = device_api_orm.entries_by_device_id(expected_device_id)
    length_before = len(previous_entities)
    length_after = len(current_entities)
    with allure.step("Check the number of logs added"):
        assert_that(
            length_after - length_before,
            equal_to(len_diff),
            f"{length_after - length_before} logs were added, not {len_diff}",
        )

    if entered_at:
        with allure.step("Get the date from payload"):
            fdate = "%Y-%m-%dT%H:%M:%S.%f"
            actual_date = datetime.strptime(
                current_entities[-1].payload.get("entered_at")[:26], fdate
            )
        with allure.step("Get the date at created_at field"):
            expected_date = current_entities[-1].created_at
        with allure.step(
            "Check the date from payload is the same as the date at created_at field"
        ):
            assert_that(
                abs(actual_date - expected_date),
                less_than(TOL),
                f"Dates in 'payload' field and in 'created_at' field don't match",
            )
    if len_diff:
        with allure.step("Get device id"):
            actual_device_id = current_entities[-1].device_id
        with allure.step("Check that the log was added for the right device id"):
            assert_that(
                actual_device_id,
                equal_to(expected_device_id),
                f"Device id is {actual_device_id}, not {expected_device_id}",
            )
    if expected_type:
        with allure.step("Get operation type number"):
            actual_type = current_entities[-1].type
        with allure.step("Check that the type of operation is correct"):
            assert_that(
                actual_type,
                equal_to(expected_type),
                f"Operation type is {actual_type}, not {expected_type}",
            )
    if expected_user_id:
        with allure.step("Get the user id in payload"):
            actual_user_id = current_entities[-1].payload.get("user_id")
        with allure.step("Check that the user id in payload is correct"):
            assert_that(
                actual_user_id,
                equal_to(int(expected_user_id)),
                f"User id is {actual_user_id}, not {expected_user_id}",
            )
    if expected_platform:
        with allure.step("Get the platform in payload"):
            actual_platform = current_entities[-1].payload.get("platform")
        with allure.step("Check that the platform in payload is correct"):
            assert_that(
                actual_platform,
                equal_to(expected_platform),
                f"Platform is {actual_platform}, not {expected_platform}",
            )
    if empty_payload:
        with allure.step("Get payload field"):
            actual_payload = current_entities[-1].payload
        with allure.step("Check that the payload field is empty "):
            assert_that(
                actual_payload,
                none(),
                f"Payload is {actual_payload}, not None",
            )


def check_create_device_sql_log(all_device_ids, new_device_id):
    assert_that(
        new_device_id,
        not_(is_in(all_device_ids)),
        f"Device id already exists",
    )
