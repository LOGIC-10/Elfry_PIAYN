from sqlalchemy.orm import Session
from ..db.database import ModelsAPI

def get_model_config(db: Session, model_name: str):
    model = db.query(ModelsAPI).filter(
        ModelsAPI.model_name == model_name,
        ModelsAPI.is_active == True
    ).first()
    return model
