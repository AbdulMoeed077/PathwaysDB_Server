from fastapi import APIRouter, Depends, HTTPException, Path, Query
from Pathways import pathways_model 
from Pathways import pathways_services
from Auth import auth_models, auth_services
router = APIRouter()

@router.post("/add_interaction")
def create_interaction(interaction: pathways_model.InteractionBase, reference: str, interactiontype: str, node_source: str, node_target: str):
    try:
        # Call the register_user function from auth_services
        db_interaction = pathways_services.register_interaction(interaction, reference, interactiontype, node_source, node_target)
        return db_interaction
    except Exception as e:
        # Handle exceptions and return an HTTP error response
        raise HTTPException(status_code=400, detail=f"{str(e.detail)}")

@router.get("/add_node", response_model=pathways_model.Node)
def create_node(node: pathways_model.NodeBase):
    try:
        # Call the register_user function from auth_services
        db_node = pathways_services.register_node(node)
        return db_node
    except Exception as e:
        # Handle exceptions and return an HTTP error response
        raise HTTPException(status_code=400, detail=f"{str(e.detail)}")
    

@router.get("/add_interaction_type", response_model=pathways_model.InteractionTypeCreate)
def create_interaction(interactionType: pathways_model.InteractionTypeBase):
    try:
        # Call the register_user function from auth_services
        db_interactionType = pathways_services.register_interaction_type(interactionType)
        return db_interactionType
    except Exception as e:
        # Handle exceptions and return an HTTP error response
        raise HTTPException(status_code=400, detail=f"{str(e.detail)}")
    
@router.post("/add_reference")
def create_reference(reference: pathways_model.ReferenceBase):
    try:
        # Call the register_user function from auth_services
        db_reference = pathways_services.register_reference(reference)
        return db_reference
    except Exception as e:
        # Handle exceptions and return an HTTP error response
        raise HTTPException(status_code=400, detail=f"{str(e.detail)}")
    
@router.post("/")
def add_new_interaction(interaction: pathways_model.InteractionBase, reference: list[pathways_model.ReferenceBase], interactionType: pathways_model.InteractionTypeBase, nodeSource: pathways_model.NodeBase, nodeTarget: pathways_model.NodeBase, current_user: auth_models.User = Depends(auth_services.authenticate_user)):
    try:
        # Call the register_user function from auth_services
        db_interaction = pathways_services.add_new_interaction(interaction, reference, interactionType, nodeSource, nodeTarget, current_user)
        return db_interaction
    except Exception as e:
        # Handle exceptions and return an HTTP error response
        raise HTTPException(status_code=400, detail=f"{str(e.detail)}")

@router.get("/display_interaction")
def display_interaction(current_user: auth_models.User = Depends(auth_services.authenticate_user)):
    try:
        # Call the register_user function from auth_services
        db_interaction = pathways_services.get_interaction_from_db()
        return db_interaction
    except Exception as e:
        # Handle exceptions and return an HTTP error response
        raise HTTPException(status_code=400, detail=f"{str(e.detail)}")