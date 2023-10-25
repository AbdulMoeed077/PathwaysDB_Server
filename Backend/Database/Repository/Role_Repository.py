from sqlalchemy.orm import Session
from Admin import role_models
from Admin.role_models import Role
from Database.DB_Models import DB_Role
from Database.SqlAlchemy import engine

class RoleRepository:
    def create_role(role: role_models.RoleBase):
        try:
            with Session(engine) as session:
                db_role = session.query(DB_Role.Role_DB).filter(DB_Role.Role_DB.name == role.name).first()
                if not db_role:
                    db_role = DB_Role.Role_DB(name=role.name)
                    session.add(db_role)
                    session.commit()
                    new_role = Role(name=db_role.name, id=db_role.id, is_active=db_role.is_active)
                    return new_role
                else:
                    raise Exception(f"Role with name '{role.name}' already exists in the database.")
        except Exception as error:
            raise Exception(f"Error while adding role in the database. {str(error)}")

    def delete_role(role: role_models.RoleBase):
        try:
            with Session(engine) as session:
                db_role = session.query(DB_Role.Role_DB).filter(DB_Role.Role_DB.name == role.name).first()
                if db_role:
                    session.delete(db_role)
                    session.commit()
                    new_role = Role(name=db_role.name, id=db_role.id, is_active=db_role.is_active)
                    return new_role
                else:
                    raise Exception(f"Role with name '{role.name}' not found in the database.")
        except Exception as error:
            raise Exception(f"Error while deleting role in the database. {str(error)}")


