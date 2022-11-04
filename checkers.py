from datetime import datetime
from typing import List

from config import HOST_GRPC, HOST_REST, TOKEN
from hamcrest import assert_that, equal_to, is_, none, less_than

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
    _, device_data = DeviceAPI(host=HOST_REST, token=TOKEN).get_device(device_id)

    actual_platform = device_data.platform
    actual_user_id = device_data.userId

    assert_that(
        actual_platform,
        equal_to(expected_platform),
        f"Platform is {actual_platform}",
    )
    assert_that(
        str(actual_user_id),
        equal_to(expected_user),
        f"UserID is {actual_user_id}",
    )


def get_data_and_check_expect_platform_and_user_id_grpc(
    device_id, expected_platform: str, expected_user: str
):
    """
    Function for gRPC update_device testing.
    """
    device_data = DeviceAPIGRPC(host=HOST_GRPC).get_device(device_id)

    actual_platform = device_data.value.platform
    actual_user_id = device_data.value.user_id

    assert_that(
        actual_platform,
        equal_to(expected_platform),
        f"Platform is {actual_platform}, not {expected_platform}",
    )
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
    device_id: int,
    previous_entities: List[DevicesEvent] = [],
    len_diff: int = 1,
    type_: int or None = None,
    entered_at: bool = False,
    user_id: int or None = None,
    platform: str or None = None,
    empty_payload: bool = False,
):
    length_before = len(previous_entities)
    current_entities = device_api_orm.entries_by_device_id(device_id)
    length_after = len(current_entities)

    assert_that(length_after - length_before, equal_to(len_diff))

    if entered_at:
        fdate = "%Y-%m-%dT%H:%M:%S.%f"
        assert_that(
            abs(
                datetime.strptime(
                    current_entities[-1].payload["entered_at"][:26], fdate
                )
                - current_entities[-1].created_at
            ),
            less_than(TOL),
        )
    if len_diff:
        assert_that(current_entities[-1].device_id, equal_to(device_id))
    if type_:
        assert_that(current_entities[-1].type, equal_to(type_))
    if user_id:
        assert_that(current_entities[-1].payload["user_id"], equal_to(int(user_id)))
    if platform:
        assert_that(current_entities[-1].payload["platform"], equal_to(platform))
    if empty_payload:
        assert_that(current_entities[-1].payload, is_(none()))
