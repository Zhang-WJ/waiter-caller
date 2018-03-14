import os

class Config:
    base_url = 'http://127.0.0.1:5000/'
    SECRET_KEY = 'This is a APP by Flask'
    MONGODB_SETTINGS = {
        'db':'library'
    }
    DEBUG_TB_PANELS = (
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        # 'flask_mongoengine.panels.MongoDebugPanel'
    )

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    MAIL_SERVER = 'smtp.sina.cn'
    MAIL_POSRT = 25
    MAIL_USERNAME = 'ahnqihyun@sina.cn'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


    FLASKY_MAIL_SUBJECT_PREFIX ='[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <ahnqihyun@sina.cn>'
    FLASKY_ADMIN = 'ahnqihyun@sina.cn'


    @staticmethod
    def init_app(app):
        pass

