from sqlalchemy.orm import Session

from ..models.mark_image import MarkImage


class MarkImageService:
    @staticmethod
    def get_mark_image(db: Session, mark_image_id: int):
        return db.query(MarkImage).filter(MarkImage.id == mark_image_id).first()

    @staticmethod
    def get_mark_images(db: Session, mark_id: int):
        return db.query(MarkImage).filter(MarkImage.mark_id == mark_id,MarkImage.is_deleted == False).all()
