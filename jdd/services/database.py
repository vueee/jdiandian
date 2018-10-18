from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('mysql://root:yourpassword@localhost/yourdb?charset=utf8', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Model = declarative_base(name='Model')
Model.query = db_session.query_property()

def init_db():
    import user
    import post
    Model.metadata.create_all(bind=engine) 




