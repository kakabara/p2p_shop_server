from datetime import datetime


class ViewComment:
    @staticmethod
    def serialize(entity):
        comment_serialized = ViewBase.serialized_attributes(entity)
        comment_serialized['answer'] = {}
        comment_serialized['user'] = {}
        comment_serialized['product'] = {}
        if getattr(entity, 'answer'):
            comment_serialized['answer'] = entity.answer.serializer()
        comment_serialized['user'] = entity.user.serializer()
        comment_serialized['product'] = entity.product.serializer()
        return comment_serialized


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
    def serialize(entity):
        serialized_entity = ViewBase.serialized_attributes(entity)
        serialized_entity.update(ViewBase.serialized_relationships(entity))
        return serialized_entity

    @staticmethod
    def append_relationships(serialized_entity, serialized_relationship):
        for k in serialized_relationship:
            serialized_entity[k] = serialized_relationship[k]
        return serialized_entity


class ResponseView:
    @staticmethod
    def get_view(entity_or_entities):
        serialized = []
        if isinstance(entity_or_entities, list):
            for entity in entity_or_entities:
                serialized_entity = entity.serializer()
                serialized.append(serialized_entity.copy())
            return serialized
        else:
            return entity_or_entities.serializer()

