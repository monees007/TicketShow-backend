from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from application.config import LocalDevelopmentConfig

engine = create_engine(LocalDevelopmentConfig().SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)


def get_or_create(model, **kwargs):
    """
    Usage:
    class Employee(Base):
        __tablename__ = 'employee'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)

    get_or_create(Employee, name='bob')
    """
    instance = get_instance(model, **kwargs)
    if instance is None:
        instance = create_instance(model, **kwargs)
    return instance


def create_instance(model, **kwargs):
    """create instance"""
    try:
        instance = model(**kwargs)
        db_session.add(instance)
        db_session.flush()
    except Exception as msg:
        mtext = 'model:{}, args:{} => msg:{}'
        print(mtext.format(model, kwargs, msg))
        db_session.rollback()
        raise msg
    return instance


def get_instance(model, **kwargs):
    """Return first instance found."""
    try:
        return db_session.query(model).filter_by(**kwargs).first()
    except NoResultFound:
        return
