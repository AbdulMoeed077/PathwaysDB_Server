from fastapi import HTTPException, APIRouter
from Admin import role_services
from Admin import role_models

router = APIRouter()

@router.post("/add_role", response_model=role_models.Role)
def create_role(role: role_models.RoleBase):
    try:
        db_role = role_services.adding_role(name=role.name)
        return db_role
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating role: {str(e)}")

@router.delete("/delete_role", response_model=role_models.Role)
def delete_role(role: role_models.RoleBase):
    try:
        db_role = role_services.remove_role(name=role.name)
        return db_role
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting role: {str(e)}")