from uuid import uuid4
from sqlalchemy.orm import Session
from Database.SqlAlchemy import engine
from Pathways import pathways_model
from Database.DB_Models import DB_Pathways

class ReferenceRepository:
    @staticmethod
    def create_references(references: list):
        try:
            with Session(engine) as session:
                # Filter out references that already exist in the database
                existing_references = ReferenceRepository.get_existing_references(session, references)
                new_references = [ref for ref in references if ref not in existing_references]
                if new_references:
                # Create DB_Pathways.Reference instances for the new references
                    db_references = [
                        DB_Pathways.Reference(
                            reference_id = str(uuid4()),
                            reference=reference.reference,
                            referenceType=reference.referenceType,
                        ) for reference in new_references
                    ]

                    # Add all new references to the session
                    session.add_all(db_references)
                    session.commit()

                    # Return the newly created references
                    new_references = [
                        pathways_model.ReferenceCreate(
                            reference=db_reference.reference,
                            referenceType=db_reference.referenceType,
                            reference_id=db_reference.reference_id
                        ) for db_reference in db_references
                    ]

                    return new_references
        except Exception as error:
            raise Exception(f"Error while adding references to the database. {str(error)}")

    def get_existing_references(session, references):
        # Create a list of tuples representing the unique identifiers of the references
        unique_identifiers = [(ref.reference, ref.referenceType) for ref in references]

        # Query for existing references with the unique identifiers
        db_references = session.query(DB_Pathways.Reference).filter(
            DB_Pathways.Reference.reference == unique_identifiers[0][0],
            DB_Pathways.Reference.referenceType == unique_identifiers[0][1],
        ).all()

        # Return the existing references as a list
        return db_references
