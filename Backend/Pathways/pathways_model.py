from tkinter import CHAR
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class NodeBase(BaseModel):
    name: str

class NodeCreate(NodeBase):
    pass

class Node(NodeBase):
    node_id: str

    class Config:
        from_attributes = True

class InteractionBase(BaseModel):
    link_type: str
    Description: Optional[str]
    validate_status: str
    Annotations: Optional[str]

class InteractionCreate(InteractionBase):
    interaction_id: str

class Interaction(InteractionCreate):
    node_source: str
    node_target: str
    interaction_type: str = str | None  
    reference: list[str] = []
    users: str = str | None  

    class Config:
        from_attributes = True

class InteractionTypeBase(BaseModel):
    name: str

class InteractionTypeCreate(InteractionTypeBase):
    interaction_type_id: str

class InteractionType(InteractionTypeBase):
    interactions: list[str] = []

    class Config:
        from_attributes = True

class ReferenceBase(BaseModel):
    reference: Optional[str]
    referenceType: Optional[str]

class ReferenceCreate(ReferenceBase):
    reference_id: str

class Reference(ReferenceBase):
    interactions: list[str] = []
    previous_interactions: list[str] = []

    class Config:
        from_attributes = True

class PreviousInteractionBase(BaseModel):
    interactions_id: str
    interaction_type_id: str
    node_id_source: str
    node_id_target: str
    linkType: str
    Description: str
    validate_status: str
    Annotations: str

class PreviousInteractionCreate(PreviousInteractionBase):
    pass

class PreviousInteraction(PreviousInteractionBase):
    previous_interaction_id: list[str] = []
    interaction: list[str] = []
    interaction_type: list[str] = []
    node: list[str] = []
    references: list[str] = []
    users: list[str] = []

    class Config:
        from_attributes = True
