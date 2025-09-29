import time

def run():
    print('ingestion worker started')
    while True:
        # TODO: pull events from API/event bus and store to DB
        time.sleep(5)

if __name__ == '__main__':
    run()