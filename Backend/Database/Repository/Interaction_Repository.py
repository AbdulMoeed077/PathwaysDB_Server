# Import necessary modules and classes
from sqlalchemy.orm import Session
from Pathways import pathways_model
from Database.DB_Models import DB_Pathways
from Database.SqlAlchemy import engine
from Database.DB_Models.DB_User import User
from Auth import auth_models

class InteractionRepository:
    def create_interaction(interaction: pathways_model.InteractionBase, references: str, interactiontype: str, node_source: str, node_target: str, user: auth_models.User):
        try:
            with Session(engine) as session:
                # Fetch the database objects for reference, node_source, node_target, and interaction_type for reference in references:
                db_node_source = session.query(DB_Pathways.Node).filter(DB_Pathways.Node.name == node_source).first()
                db_node_target = session.query(DB_Pathways.Node).filter(DB_Pathways.Node.name == node_target).first()
                db_interactiontype = session.query(DB_Pathways.InteractionType).filter(DB_Pathways.InteractionType.name == interactiontype).first()

                # Create a new user object
                db_interaction = DB_Pathways.Interaction(
                    link_type=interaction.link_type,
                    description=interaction.Description,
                    validate_status=interaction.validate_status,
                    annotations=interaction.Annotations,
                    interaction_type=db_interactiontype
                )
                db_interaction.interaction_type=db_interactiontype
                db_interaction.node_source=db_node_source
                db_interaction.node_target=db_node_target
                # Fetch the "user" role from the database
                db_user = session.query(User).filter(User.id == user.id).first()

                # Append the retrieved objects to the relationship
                for reference in references:
                    db_reference = session.query(DB_Pathways.Reference).filter(DB_Pathways.Reference.reference_id == reference.reference_id).first()
                    db_interaction.reference.append(db_reference)
                db_interaction.node.append(db_node_source)
                db_interaction.node.append(db_node_target)
                db_interaction.users.append(db_user)

                # Add the interaction to the database
                session.add(db_interaction)
                session.commit()

                # Refresh the interaction object to get its updated state
                session.refresh(db_interaction)

                return db_interaction
        except Exception as error:
            # Handle any exceptions that occur during the process
            raise Exception(f"Error while creating interaction in the database. {error.args[0]}")
        
    def get_all_interaction():
        try:
            with Session(engine) as session:
                db_interactions = session.query(DB_Pathways.Interaction).all()
                interactions = []

                for interact in db_interactions:
                    interaction = pathways_model.Interaction(
                        interaction_id=interact.interaction_id,
                        link_type=interact.link_type,
                        interaction_type=interact.interaction_type.name,
                        node_source=interact.node_source.name,
                        node_target=interact.node_target.name,
                        Description=interact.description,
                        Annotations=interact.annotations,
                        users=interact.users[0].email,
                        validate_status=interact.validate_status,
                            
                    )
                    for reference in interact.reference:
                        new_reference = pathways_model.ReferenceCreate(
                            reference=reference.reference,
                            referenceType=reference.referenceType,
                            reference_id=reference.reference_id
                        )
                        interaction.reference.append(new_reference)
                    interactions.append(interaction)

                return interactions
        except Exception as error:
            raise Exception(f"Error while getting interactions from the database. {error.args[0]}")
