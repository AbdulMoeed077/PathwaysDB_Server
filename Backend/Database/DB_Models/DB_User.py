import uuid
from Database.SqlAlchemy import Base
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship, Mapped
from Database.DB_Models import Pathways_associations

class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    fname = Column(String(35), index=True)
    lname = Column(String(35), index=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)
    interaction: Mapped[list] = relationship('Interaction', secondary=Pathways_associations.interaction_users_association_table, back_populates='users')
    previous_interaction: Mapped[list] = relationship('PreviousInteraction', secondary=Pathways_associations.previous_interaction_user_association_table, back_populates='users')
    
    roles: Mapped[list] = relationship("Role_DB", secondary=Pathways_associations.user_role_association_table, back_populates="users")
# Other parts of your DB_User.py module...
