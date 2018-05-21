from datetime import datetime


class ViewBase:
    @staticmethod
    def serialized_attributes(entity):
        serialized_entity = {}
        if not entity:
            return {}
        for column in entity.__table__.columns:
            value = getattr(entity, column.name)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M')
            serialized_entity[column.name] = value
        return serialized_entity

    @staticmethod
    def serialized_relationships(entity):
        serialized_relationships = {}
        for rel in entity._field_relationships():
            rel_entity = getattr(entity, rel)
            serialized_relationships[rel] = ViewBase.serialized_attributes(rel_entity)

        return serialized_relationships

    @staticmethod
    def serialize(entities_or_entity):
        serialized = []
        if isinstance(entities_or_entity, list):
            for entity in entities_or_entity:
                serialized_entity = ViewBase.serialized_attributes(entity)
                serialized_entity.update(ViewBase.serialized_relationships(entity))

                serialized.append(serialized_entity.copy())
            return serialized
        else:
            serialized_entity = ViewBase.serialized_attributes(entities_or_entity)
            serialized_entity.update(ViewBase.serialized_relationships(entities_or_entity))
            return serialized_entity
