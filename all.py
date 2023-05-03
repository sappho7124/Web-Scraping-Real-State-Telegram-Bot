from threading import Thread
from scraper_madrid import call_all_madrid
from scraper_barcelona import call_all_barcelona
from scraper_valencia import call_all_valencia

Thread(target = call_all_madrid).start()
Thread(target = call_all_barcelona).start()
Thread(target = call_all_valencia).start()