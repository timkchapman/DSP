class SerializerMixin:
    def serialize(self):
        return {column.name: getattr(self,column.name) for column in self.__table__.columns}