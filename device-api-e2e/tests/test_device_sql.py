import allure
import pytest

from framework.checkers import check_sql_log, check_create_device_sql_log
from framework.constants import PLATFORMS, USER_IDS, NONEXISTENT_DEVICE_ID, BAD_USER_ID


@allure.suite("Logs")
@allure.title("Basic get_device logs test")
def test_get_device_sql_alchemy(device_api_orm, device_sql):
    device_id = device_sql
    with allure.step("Check the log with the right parameters was added"):
        check_sql_log(
            device_api_orm,
            expected_device_id=device_id,
            len_diff=1,
            expected_type=1,
            entered_at=True,
        )


@allure.suite("Logs")
@allure.title("get_device logs test with non-existent device id")
def test_get_nonexistent_device_sql_alchemy(device_api_orm, device_sql):
    device_id = NONEXISTENT_DEVICE_ID
    with allure.step("Check the log wasn't added"):
        check_sql_log(device_api_orm, expected_device_id=device_id, len_diff=0)


@allure.suite("Logs")
@allure.title("Basic update_device logs test with different input parameters")
@pytest.mark.parametrize(
    "platform, user_id",
    [
        (PLATFORMS[1], USER_IDS[1]),
        (PLATFORMS[1], USER_IDS[2]),
        (PLATFORMS[2], USER_IDS[2]),
    ],
)
def test_update_device_sql_alchemy(
    device_api, device_api_orm, device_sql, platform, user_id
):
    device_id = device_sql
    with allure.step("Get all logs with provided device id"):
        entities = device_api_orm.entries_by_device_id(device_id)

    with allure.step(""):
        device_api.update_device(
            platform=platform, user_id=user_id, device_id=device_id
        )

    with allure.step("Check the log with the right parameters was added"):
        check_sql_log(
            device_api_orm,
            expected_device_id=device_id,
            previous_entities=entities,
            len_diff=1,
            expected_type=2,
            expected_user_id=int(user_id),
            expected_platform=platform,
        )


@allure.suite("Logs")
@allure.title("Basic update_device logs test with platform updates")
def test_update_platform_device_sql_alchemy(device_api, device_api_orm, device_sql):
    device_id = device_sql
    with allure.step("Get all logs with provided device id"):
        entities = device_api_orm.entries_by_device_id(device_id)

    with allure.step("Update device by its id with provided parameters"):
        device_api.update_device(
            platform=PLATFORMS[2],
            user_id=USER_IDS[0],
            device_id=device_id,
        )
    with allure.step("Check the log with the right parameters was added"):
        check_sql_log(
            device_api_orm,
            expected_device_id=device_id,
            previous_entities=entities,
            len_diff=1,
            expected_type=2,
            expected_user_id=USER_IDS[0],
            expected_platform=PLATFORMS[2],
        )


@allure.suite("Logs")
@allure.title("update_device logs test with non-existent device id")
def test_update_nonexistent_device_sql_alchemy(device_api, device_api_orm, device_sql):
    device_id = NONEXISTENT_DEVICE_ID
    with allure.step("Get all logs with provided device id"):
        entities = device_api_orm.entries_by_device_id(device_id)

    with allure.step("Try to update non-existent device"):
        device_api.update_device(
            platform=PLATFORMS[1], user_id=USER_IDS[1], device_id=device_id
        )

    with allure.step("Check the log wasn't added"):
        check_sql_log(
            device_api_orm,
            previous_entities=entities,
            expected_device_id=device_id,
            len_diff=0,
        )


@allure.suite("Logs")
@allure.title("Basic delete_device logs test")
def test_delete_device_sql_alchemy(device_api, device_api_orm, device_sql):
    device_id = device_sql
    with allure.step("Get all logs with provided device id"):
        entities = device_api_orm.entries_by_device_id(device_id)

    with allure.step("Delete device by id"):
        device_api.delete_device(device_id=device_id)

    with allure.step("Check the log with the right parameters was added"):
        check_sql_log(
            device_api_orm,
            expected_device_id=device_id,
            previous_entities=entities,
            len_diff=1,
            expected_type=3,
            empty_payload=True,
        )


@allure.suite("Logs")
@allure.title("delete_device logs test with non-existent device id")
def test_delete_nonexistent_device_sql_alchemy(device_api, device_api_orm):
    device_id = NONEXISTENT_DEVICE_ID
    with allure.step("Get all logs with provided device id"):
        entities = device_api_orm.entries_by_device_id(device_id)

    with allure.step("Try to delete non-existent device"):
        device_api.delete_device(device_id=device_id)

    with allure.step("Check the log wasn't added"):
        check_sql_log(
            device_api_orm,
            previous_entities=entities,
            expected_device_id=device_id,
            len_diff=0,
        )


@allure.suite("Logs")
@allure.title("Basic create_device logs test")
def test_create_device_sql_alchemy(device_api, device_api_orm):
    all_device_ids = device_api_orm.all_device_ids()
    _, device_id = device_api.create_device(platform=PLATFORMS[1], user_id=USER_IDS[2])

    check_create_device_sql_log(all_device_ids=all_device_ids, new_device_id=device_id)
    check_sql_log(
        device_api_orm, expected_device_id=int(device_id), len_diff=1, expected_type=1
    )

    device_api.delete_device(device_id=device_id)


@allure.suite("Logs")
@allure.title("create_device logs test with non-existent device id")
def test_create_bad_device_sql_alchemy(device_api, device_api_orm):
    device_id = NONEXISTENT_DEVICE_ID
    entities = device_api_orm.entries_by_device_id(device_id)

    device_api.create_device(platform=PLATFORMS[1], user_id=BAD_USER_ID)

    check_sql_log(
        device_api_orm,
        previous_entities=entities,
        expected_device_id=device_id,
        len_diff=0,
    )
