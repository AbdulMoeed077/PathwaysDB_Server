from sqlalchemy.orm import Session
from fastapi import HTTPException
from Database.SqlAlchemy import engine
from Pathways import pathways_model
from Database.DB_Models import DB_Pathways

class InteractionTypeRepository:
    def create_interaction_type(interactionType: pathways_model.InteractionTypeBase):
        try:
            with Session(engine) as session:
                db_interactionType = DB_Pathways.InteractionType(
                    name=interactionType.name
                )
                session.add(db_interactionType)
                session.commit()
                new_interactionType = pathways_model.InteractionTypeCreate(name=db_interactionType.name, interaction_type_id=db_interactionType.interaction_type_id)
                return new_interactionType
        except Exception as error:
            raise Exception(f"Error while adding role in the database. {str(error)}")
        
    def get_interaction_type_by_name(interactionType: pathways_model.InteractionTypeBase):
        try:
            with Session(engine) as session:
                 db_interactionType = session.query(DB_Pathways.InteractionType).filter(DB_Pathways.InteractionType.name == interactionType.name).first()
                 if not db_interactionType:
                     db_interactionType = InteractionTypeRepository.create_interaction_type(interactionType)
                 return(db_interactionType)
        except Exception as error:            
            raise Exception(f"Node name '{interactionType.name}' already exists in the database. {error.args[0]}")
    