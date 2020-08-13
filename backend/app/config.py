class ProductionConfig():
    JOBS = [{
        'id': 'update_password',
        'func': 'app.jobs:update_password',
        'trigger': 'cron',
        'hour': 0,
        'minute': 30,
        'day': 1,
    }]
    SCHEDULER_API_ENABLED = True
