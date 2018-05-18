import json
from .models import *
from server import db
from .views import ViewBase


def get_dict_table_name_to_class():
    all_classes = set()
    work = [db.Model]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in all_classes:
                all_classes.add(child)
                work.append(child)

    return {klass.__tablename__: klass for klass in all_classes if getattr(klass, '__tablename__')}


table_name_class = get_dict_table_name_to_class()


class BaseController:
    @staticmethod
    def create_entity(entity_class, fields: dict):
        entity = entity_class()
        for field in fields:
            setattr(entity, field, fields[field])
        print(1)
        return entity

    @staticmethod
    def update_entity(entity, fields: dict):
        for field in fields:
            setattr(entity, field, fields[field])
        print(1)
        return entity

    @staticmethod
    def base_get(entity: str, entity_id: int = None):
        entity_class = table_name_class.get(entity)
        #
        if not entity_class:
            return None
        if entity_id:
            result = entity_class.query.filter(entity_class.id == entity_id).one_or_none()
            if result:
                view = ViewBase.serialize([result])
            else:
                return {}
        else:
            result = entity_class.query.all()
            if result:
                view = ViewBase.serialize(result)
            else:
                return {}
        return view

    @staticmethod
    def base_post(entity: str, data):
        entity_class = table_name_class.get(entity)

        if not entity_class:
            return None
        data = json.loads(data.decode('utf-8'))
        result = BaseController.create_entity(entity_class, data)
        db.session.add(result)
        db.session.commit()
        view = ViewBase.serialize(result)
        return view

    @staticmethod
    def base_update(entity: str, entity_id: int, data):
        entity_class = table_name_class.get(entity)
        if not entity_class:
            return None
        entity = entity_class.query.filter(entity_class.id == entity_id).one_or_none()
        if not entity:
            return None
        data = json.loads(data.decode('utf-8'))
        result = BaseController.update_entity(entity, data)
        db.session.add(result)
        db.session.commit()
        view = ViewBase.serialize(result)
        return view

    @staticmethod
    def base_delete(entity: str, entity_id: int):
        entity_class = table_name_class.get(entity)

        if not entity_class:
            return None
        entity = entity_class.query.filter(entity_class.id == entity_id).one_or_none()
        db.session.delete(entity)
        db.session.commit()
        return {"status": "done"}
