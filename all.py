import threading
from scraper_madrid import call_all_madrid

thread = threading.Thread(target=call_all_madrid)
thread.start()
thread = threading.Thread(target=call_all_barcelona)
thread.start()
thread = threading.Thread(target=call_all_valencia)
thread.start()