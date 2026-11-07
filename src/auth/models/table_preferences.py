import datetime

from sqlalchemy.dialects.postgresql import JSONB

from src import db


class TablePreferences(db.Model):
    """Preferencias de visualizacion de la tabla de vuelos, una fila por usuario."""

    __tablename__ = 'table_preferences'
    __table_args__ = (
        db.CheckConstraint(
            'hour_start BETWEEN 0 AND 23 AND hour_end BETWEEN 0 AND 23 '
            'AND hour_start <= hour_end',
            name='ck_table_preferences_hour_range'),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        unique=True,
    )
    hour_start: int = db.Column(db.SmallInteger, nullable=False, default=8,
                                server_default='8')
    hour_end: int = db.Column(db.SmallInteger, nullable=False, default=20,
                              server_default='20')
    # matriculas ocultas: una avioneta nueva se muestra por defecto
    hidden_planes: list = db.Column(
        JSONB, nullable=False, default=list, server_default='[]')
    updated_at = db.Column(
        db.DateTime, nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)
