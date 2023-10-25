from fastapi import HTTPException
from Database.Repository import Node_Repository
from Database.Repository import Interaction_Type_Repository
from Database.Repository import Reference_Repository
from Database.Repository import Interaction_Repository
from Pathways import pathways_model
from Auth import auth_models

def get_interaction_from_db():
    try:
        db_interaction = Interaction_Repository.InteractionRepository.get_all_interaction()
        return db_interaction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
def add_new_interaction(interaction: pathways_model.InteractionBase, reference: pathways_model.ReferenceBase, interactionType: pathways_model.InteractionTypeBase, node_source: pathways_model.NodeBase, node_target: pathways_model.NodeBase, user: auth_models.User):
    try:
        db_node_souce= Node_Repository.NodeRepository.get_node_by_name(node_source)
        db_node_target= Node_Repository.NodeRepository.get_node_by_name(node_target)
        db_interactionType= Interaction_Type_Repository.InteractionTypeRepository.get_interaction_type_by_name(interactionType)
        db_reference = Reference_Repository.ReferenceRepository.create_references(reference)
        db_interaction = Interaction_Repository.InteractionRepository.create_interaction(interaction, db_reference, db_interactionType.name, db_node_souce.name, db_node_target.name, user)
        return db_interaction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def register_interaction(interaction: pathways_model.InteractionBase, reference: str, interactiontype: str, node_source: str, node_target: str):
    try: 
        db_interaction = Interaction_Repository.InteractionRepository.create_interaction(interaction, reference, interactiontype, node_source, node_target)
        return db_interaction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def register_node(node: pathways_model.NodeCreate):
    try: 
        db_node = Node_Repository.NodeRepository.get_node_by_name(node)
        return db_node
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def register_interaction_type(interactionType: pathways_model.InteractionBase):
    try: 
        db_interactionType = Interaction_Type_Repository.InteractionTypeRepository.get_interaction_type_by_name(interactionType)
        return db_interactionType
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def register_reference(reference: pathways_model.ReferenceCreate):
    try: 
        db_reference = Reference_Repository.ReferenceRepository.create_reference(reference)
        return db_reference
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

