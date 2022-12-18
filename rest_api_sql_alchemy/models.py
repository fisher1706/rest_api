from rest_api_sql_alchemy.app import db, Base


class Video(Base):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)
