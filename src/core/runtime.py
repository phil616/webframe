from core.background import generate_background_scheduler
from core.logcontroller import Logger

runtime_info = {}
syslog = Logger("system").getLogger
scheduler = generate_background_scheduler()

