from fastapi import HTTPException
from Database.Repository.Role_Repository import RoleRepository
from Admin import role_models

def adding_role(name: str):
    try:
        role_base = role_models.RoleBase(name=name)
        db_role = RoleRepository.create_role(role_base)
        return db_role
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def remove_role(name: str):
    try:
        role_base = role_models.RoleBase(name=name)
        db_role = RoleRepository.delete_role(role_base)
        return db_role
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))