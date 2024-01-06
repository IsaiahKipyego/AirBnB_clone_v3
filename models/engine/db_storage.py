#!/usr/bin/python3
'''
    Defines class DatabaseStorage
'''
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.state import State
from models.city import City
from models.base_model import Base


class DBStorage:
    '''
        Creates SQLalchemy database
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
            Creates engine and link to MySQL database (hbnb_dev, hbnb_dev_db)
        '''
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        envv = getenv("HBNB_ENV", "none")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if envv == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
            Querys current db session
        '''
        db_dict = {}

        if cls != "":
            objs = self.__session.query(models.classes[cls]).all()
            for obj in objs:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                db_dict[key] = obj
            return db_dict
        else:
            for k, v in models.classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(v).all()
                    if len(objs) > 0:
                        for obj in objs:
                            key = "{}.{}".format(obj.__class__.__name__,
                                                 obj.id)
                            db_dict[key] = obj
            return db_dict

    def new(self, obj):
        '''
            Adds object to current db session
        '''
        self.__session.add(obj)

    def save(self):
        '''
            Commits all changes of current db session
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''
            Deletes from current db session
        '''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''
            Commits all changes of current databse session
        '''
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        '''
            Removes private sessions attribute
        '''
        self.__session.close()

    def get(self, cls, id):
        '''
            Retrieves an object with class name and id
        '''
        result = None
        try:
            objs = self.__session.query(models.classes[cls]).all()
            for obj in objs:
                if obj.id == id:
                    result = obj
        except BaseException:
            pass
        return result

    def count(self, cls=None):
        '''
            Count num objects in DBstorage
        '''
        cls_counter = 0

        if cls is not None:
            objs = self.__session.query(models.classes[cls]).all()
            cls_counter = len(objs)
        else:
            for k, v in models.classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(models.classes[k]).all()
                    cls_counter += len(objs)
        return cls_counter

