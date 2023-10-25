import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped
from Database.DB_Models import Pathways_associations
from Database.SqlAlchemy import Base
from uuid import uuid4

class Node(Base):
    __tablename__ = 'node'
    node_id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, index=True)
    name = Column(String)
    
    
    node_source = relationship('Interaction', back_populates='node_source', foreign_keys='Interaction.node_id_source')
    node_target = relationship('Interaction', back_populates='node_target', foreign_keys='Interaction.node_id_target')

    interaction = relationship('Interaction', secondary=Pathways_associations.node_interaction_association_table, back_populates='node')
    previous_interaction = relationship('PreviousInteraction', secondary=Pathways_associations.previous_interaction_node_association_table, back_populates='node')

class Interaction(Base):
    __tablename__ = 'interaction'
    interaction_id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, index=True)
    
    interaction_type_id = Column(String(36), ForeignKey('interaction_type.interaction_type_id'))
    interaction_type = relationship('InteractionType', back_populates='interaction')

    node_id_source = Column(String(36), ForeignKey('node.node_id'))
    node_id_target = Column(String(36), ForeignKey('node.node_id'))
    node_source = relationship('Node', back_populates='node_source', foreign_keys='Interaction.node_id_source')
    node_target = relationship('Node', back_populates='node_target', foreign_keys='Interaction.node_id_target')

    link_type = Column(String(255))  # Adjusted the data type and length
    description = Column(String)  # Adjusted the data type
    validate_status = Column(String)
    annotations = Column(String)
    
    
    node: Mapped[list] = relationship('Node', secondary=Pathways_associations.node_interaction_association_table, back_populates='interaction')
    previous_interaction: Mapped[list] = relationship('PreviousInteraction', back_populates='interaction')
    users: Mapped[list] = relationship('User', secondary=Pathways_associations.interaction_users_association_table, back_populates='interaction')
    reference: Mapped[list] = relationship('Reference', secondary=Pathways_associations.interaction_reference_association_table, back_populates='interaction')

class InteractionType(Base):
    __tablename__ = 'interaction_type'
    interaction_type_id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, index=True)
    name = Column(String)
    
    interaction: Mapped[list] = relationship('Interaction', back_populates='interaction_type')
    previous_interaction = relationship('PreviousInteraction', back_populates='interaction_type')

class Reference(Base):
    __tablename__ = 'reference'
    reference_id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, index=True)
    reference = Column(String(2083))  # Adjusted the data type and length
    referenceType = Column(String(255))

    interaction: Mapped[list] = relationship('Interaction', secondary=Pathways_associations.interaction_reference_association_table, back_populates='reference')
    previous_interaction: Mapped[list] = relationship('PreviousInteraction', secondary=Pathways_associations.previous_interaction_reference_association_table, back_populates='reference')

class PreviousInteraction(Base):
    __tablename__ = 'previous_interaction'
    previous_interaction_id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, index=True)
    interaction_type_id = Column(String(36), ForeignKey('interaction_type.interaction_type_id'))
    interaction_id = Column(String(36), ForeignKey('interaction.interaction_id'))
    node_id_source = Column(String(36), ForeignKey('node.node_id'))
    node_id_target = Column(String(36), ForeignKey('node.node_id'))
    link_type = Column(String(255))  # Adjusted the data type and length
    description = Column(String)  # Adjusted the data type
    validate_status = Column(String)
    annotations = Column(String)
    
    interaction: Mapped[list] = relationship('Interaction', back_populates='previous_interaction')
    interaction_type = relationship('InteractionType', back_populates='previous_interaction')
    node: Mapped[list] = relationship('Node', secondary=Pathways_associations.previous_interaction_node_association_table, back_populates='previous_interaction')
    reference: Mapped[list] = relationship('Reference', secondary=Pathways_associations.previous_interaction_reference_association_table, back_populates='previous_interaction')
    users: Mapped[list] = relationship('User', secondary=Pathways_associations.previous_interaction_user_association_table, back_populates='previous_interaction')
