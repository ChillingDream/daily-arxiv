import datetime
from download import update
import schedule
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s', datefmt='[%Y-%m-%d %H:%M:%S]')

from exts import db

def fetch_new():
    raw = db.raw_arxiv_data
    max_result = 500
    if datetime.datetime.now().hour <= 2:
        theday = datetime.date.today() - datetime.timedelta(1)
    else:
        theday = datetime.date.today()
    max_id_record = raw.find_one(
        {"arxiv_id": {"$regex": '^{:02}{:02}.*'.format(theday.year % 100, theday.month)}},
        sort=[('arxiv_id', -1)]
    )
    if max_id_record is None:
        max_id = '{:02}{:02}.{:05}'.format(theday.year % 100, theday.month, 0)
    else:
        max_id = max_id_record["arxiv_id"]

    try:
        n_update = update(theday, max_id, max_result)
        logging.info('sucess get %d papers from %s' % (n_update, max_id))
    except Exception as e:
        logging.info('Update failed')
        print(e)

for i in range(1, 24, 2):
    schedule.every().day.at('{:02}:00'.format(i)).do(fetch_new)

logging.info('Start!')
while True:
    schedule.run_pending()
    time.sleep(60)