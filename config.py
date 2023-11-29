import os
basedir = os.path.abspath(os.path.dirname(__file__))

# yaml är en textfil som ligger utanför "exefilen" 
# interpreterande
class Config:
    DEBUG = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Hejsan123@mysql/pythoncrud'
    #SQLALCHEMY_DATABASE_URI = os.getenv('CONNECTIONSTRING')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
    DEBUG = True