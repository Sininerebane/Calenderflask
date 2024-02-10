import db
import model

TITLE_LIMIT = 30
TEXT_LIMIT = 200


class LogicException(Exception):
    pass


def check_logic_update(event: model.Event):
    if len(event.title) > TITLE_LIMIT:
        raise LogicException(f'Title length > max: {TITLE_LIMIT}')
    elif len(event.text) > TEXT_LIMIT:
        raise LogicException(f'Text length > max: {TEXT_LIMIT}')


class Eventlogic:
    def __init__(self):
        self.db = db.DB()

    def check_logic_create(self, event: model.Event):
        if len(event.title) > TITLE_LIMIT:
            raise LogicException(f'Title length > max: {TITLE_LIMIT}')
        elif len(event.text) > TEXT_LIMIT:
            raise LogicException(f'Text length > max: {TEXT_LIMIT}')
        elif event.event_id in self.db.storage.storage.keys():
            raise LogicException(f'You can add only one event for one day')

    def create(self, event: model.Event):
        self.check_logic_create(event)
        try:
            self.db.create(event)
        except Exception as ex:
            raise LogicException(f"failed CREATE operation with: {ex}")

    def list(self):
        try:
            return self.db.list()
        except Exception as ex:
            raise LogicException(f"failed LIST operation with: {ex}")

    def read(self, event_id: str):
        try:
            return self.db.read(event_id)
        except Exception as ex:
            raise LogicException(f"failed READ operation with: {ex}")

    def update(self, event_id: str, event: model.Event):
        check_logic_update(event)
        try:
            self.db.update(event_id, event)
        except Exception as ex:
            return LogicException(f"failed UPDATE operation with: {ex}")

    def delete(self, event_id: str):
        try:
            self.db.delete(event_id)
        except Exception as ex:
            return LogicException(f"failed DELETE operation with: {ex}")
