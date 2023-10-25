from sqlalchemy import Column, Table, ForeignKey
from Database.SqlAlchemy import Base

node_interaction_association_table = Table(
    'node_interaction',
    Base.metadata,
    Column('node_id', ForeignKey('node.node_id'), primary_key=True),
    Column('interaction_id', ForeignKey('interaction.interaction_id'), primary_key=True)
)

# Define the many-to-many relationship table for Interactions and Reference
interaction_reference_association_table = Table(
    'interaction_reference',
    Base.metadata,
    Column('interaction_id', ForeignKey('interaction.interaction_id'), primary_key=True),
    Column('reference_id', ForeignKey('reference.reference_id'), primary_key=True)
)

# Define the many-to-many relationship table for Interactions and Users
interaction_users_association_table = Table(
    'interaction_users',
    Base.metadata,
    Column('interaction_id', ForeignKey('interaction.interaction_id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True)
)

# Define the many-to-many relationship table for PreviousInteraction and Node
previous_interaction_node_association_table = Table(
    'previous_interaction_node',
    Base.metadata,
    Column('previous_interaction_id', ForeignKey('previous_interaction.previous_interaction_id'), primary_key=True),
    Column('node_id', ForeignKey('node.node_id'), primary_key=True)
)

# Define the many-to-many relationship table for PreviousInteraction and Reference
previous_interaction_reference_association_table = Table(
    'previous_interaction_reference',
    Base.metadata,
    Column('previous_interaction_id', ForeignKey('previous_interaction.previous_interaction_id'), primary_key=True),
    Column('reference_id', ForeignKey('reference.reference_id'), primary_key=True)
)

# Define the many-to-many relationship table for PreviousInteraction and Users
previous_interaction_user_association_table = Table(
    'previous_interaction_user',
    Base.metadata,
    Column('previous_interaction_id', ForeignKey('previous_interaction.previous_interaction_id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True)
)


user_role_association_table = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)