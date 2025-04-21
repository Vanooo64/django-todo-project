from datetime import datetime


def global_variables(request):
    return {
        'timestamp': datetime.now().timestamp()
    }
