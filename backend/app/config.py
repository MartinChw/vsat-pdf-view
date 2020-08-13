class ProductionConfig():
    JOBS = [{
        'id': 'task_monitor',
        'func': 'app.jobs:task_monitor',
        'trigger': 'interval',
        'seconds': 10
    }]
    SCHEDULER_API_ENABLED = True



