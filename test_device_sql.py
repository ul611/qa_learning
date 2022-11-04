import pytest

from framework.checkers import check_sql_log
from framework.constants import PLATFORMS, USER_IDS, NONEXISTENT_DEVICE_ID


def test_get_device_sql_alchemy(device_api_orm, device_sql):
    device_id = device_sql
    check_sql_log(
        device_api_orm, device_id=device_id, len_diff=1, type_=1, entered_at=True
    )


def test_get_nonexistent_device_sql_alchemy(device_api_orm, device_sql):
    device_id = NONEXISTENT_DEVICE_ID
    check_sql_log(device_api_orm, device_id=device_id, len_diff=0)


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
    entities = device_api_orm.entries_by_device_id(device_id)

    device_api.update_device(platform=platform, user_id=user_id, device_id=device_id)

    check_sql_log(
        device_api_orm,
        device_id=device_id,
        previous_entities=entities,
        len_diff=1,
        type_=2,
        user_id=int(user_id),
        platform=platform,
    )


def test_update_platform_device_sql_alchemy(device_api, device_api_orm, device_sql):
    device_id = device_sql
    previous_entry = device_api_orm.existent_entry_by_device_id(device_id)
    entities = device_api_orm.entries_by_device_id(device_id)

    device_api.update_device(
        platform=PLATFORMS[2],
        user_id=previous_entry.payload["user_id"],
        device_id=device_id,
    )

    check_sql_log(
        device_api_orm,
        device_id=device_id,
        previous_entities=entities,
        len_diff=1,
        type_=2,
        user_id=previous_entry.payload["user_id"],
        platform=PLATFORMS[2],
    )


def test_update_nonexistent_device_sql_alchemy(device_api, device_api_orm, device_sql):
    device_id = NONEXISTENT_DEVICE_ID
    entities = device_api_orm.entries_by_device_id(device_id)

    device_api.update_device(
        platform=PLATFORMS[1], user_id=USER_IDS[1], device_id=device_id
    )

    check_sql_log(
        device_api_orm, previous_entities=entities, device_id=device_id, len_diff=0
    )


def test_delete_device_sql_alchemy(device_api, device_api_orm, device_sql):
    device_id = device_sql
    entities = device_api_orm.entries_by_device_id(device_id)

    device_api.delete_device(device_id=device_id)

    check_sql_log(
        device_api_orm,
        device_id=device_id,
        previous_entities=entities,
        len_diff=1,
        type_=3,
        empty_payload=True,
    )


def test_delete_nonexistent_device_sql_alchemy(device_api, device_api_orm):
    device_id = NONEXISTENT_DEVICE_ID
    entities = device_api_orm.entries_by_device_id(device_id)

    device_api.delete_device(device_id=device_id)

    check_sql_log(
        device_api_orm, previous_entities=entities, device_id=device_id, len_diff=0
    )
