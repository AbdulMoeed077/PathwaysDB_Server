from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import HTTPException
from Database.SqlAlchemy import engine
from Pathways import pathways_model
from Database.DB_Models import DB_Pathways

class NodeRepository:
    def create_node(node: pathways_model.NodeBase):
        try:
            with Session(engine) as session:
                db_node = DB_Pathways.Node(
                    node_id = str(uuid4()),
                    name=node.name
                )
                session.add(db_node)
                session.commit()
                new_node = pathways_model.Node(name=db_node.name, node_id=db_node.node_id)
                return new_node
        except Exception as error:
            raise Exception(f"Error while adding role in the database. {str(error)}")
        
    def get_node_by_name(node: pathways_model.NodeBase):
        try:
            with Session(engine) as session:
                 db_node = session.query(DB_Pathways.Node).filter(DB_Pathways.Node.name == node.name).first()
                 if not db_node:
                     db_node = NodeRepository.create_node(node)
                 return(db_node)
        except Exception as error:            
            raise Exception(f"Node name '{node.name}' already exists in the database. {error.args[0]}")
    