import uuid
from sqlalchemy import  Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from Database.SqlAlchemy import Base
from Database.DB_Models.Pathways_associations import user_role_association_table

class Role_DB(Base):
    __tablename__ = 'roles'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, index=True)
    name = Column(String(35), unique=True, index=True)
    is_active = Column(Boolean, default=True)

    users: Mapped[list] = relationship("User", secondary=user_role_association_table, back_populates="roles")
    