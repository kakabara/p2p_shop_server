
class ViewBase:
    @staticmethod
    def serialize(entities_or_entity):
        serialized = []
        serialized_entity = {}
        if isinstance(entities_or_entity, list):
            for entity in entities_or_entity:
                for column in entity.__table__.columns:
                    serialized_entity[column.name] = str(getattr(entity, column.name))
                serialized.append(serialized_entity.copy())
            return serialized
        else:
            for column in entities_or_entity.__table__.columns:
                serialized_entity[column.name] = str(getattr(entities_or_entity, column.name))
            return serialized_entity
