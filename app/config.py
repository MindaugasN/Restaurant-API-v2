class Config(object):
    '''Parent configuration class.'''
    HOST = '127.0.0.1'
    PORT = 5000 
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'

class DevelopmentConfig(Config):
    '''Configurations for Development.'''
    DEBUG = True

class TestingConfig(Config):
    '''Configurations for Testing, with a separate test database.'''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_data.db'
    DEBUG = True


class ProductionConfig(Config):
    '''Configurations for Production.'''
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}