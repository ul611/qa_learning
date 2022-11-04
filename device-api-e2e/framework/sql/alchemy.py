from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from framework.sql.act_device_api_models import DevicesEvent


class Alchemy:
    def __init__(self, dsn: str):
        engine = create_engine(dsn)
        self.session_factory = sessionmaker(bind=engine)
        self.session = self.session_factory()

    def entries_by_device_id(self, device_id: int) -> List[DevicesEvent]:
        all_entries = (
            self.session.query(DevicesEvent).filter_by(device_id=device_id).all()
        )
        return sorted(all_entries, key=lambda x: x.updated_at)

    def existent_entry_by_device_id(self, device_id: int) -> DevicesEvent:
        return self.session.query(DevicesEvent).filter_by(device_id=device_id).first()

    def all_device_ids(self) -> List[int]:
        return self.session.query(DevicesEvent.device_id).distinct()
