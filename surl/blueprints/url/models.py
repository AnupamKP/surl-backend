from surl.utils.db import db


class Surl_ID(db.Model):
    __tablename__ = 'surl_id'

    url_id = db.Column(db.String(30), primary_key=True, nullable=False)
    url = db.Column(db.String(10000), nullable=False)

    def __init__(self, **kwargs):
        super(Surl_ID, self).__init__(**kwargs)

    def __repr__(self):
        return f"<Surl_ID(url_id='{self.url_id}',url='{self.url}')>"

    @classmethod
    def get_url_all(cls):
        return db.session.query(Surl_ID.url_id, Surl_ID.url).all()

    @classmethod
    def get_url_from_id(cls, url_id):
        try:
            return db.session.query(Surl_ID.url).filter(Surl_ID.url_id == url_id).one()
        except Exception:
            return None

    @classmethod
    def create_url(cls, url_id, url):
        db.session.add(Surl_ID(url=url, url_id=url_id))
        db.session.commit()
        return Surl_ID(url=url, url_id=url_id)

    @classmethod
    def delete_url_from_id(cls, url_id):
        response_from_db = db.session.query(Surl_ID).filter(Surl_ID.url_id == url_id).delete()
        db.session.commit()
        return response_from_db
