import mt5utilities as util
import logging
import keyboard
import config as cfg
import time
import threading
import bot as Bot

logger = util.AppLogger('main-logger', 'main-logger.log').get_logger()


def key_capture_thread(kill_threads):
    logger.info("Waiting for ESC key...")
    keyboard.wait('esc')
    logger.info("ESC key detected!")
    kill_threads[0] = True


def update_market_status_thread(market_status, messenger, market_open_message_printed, market_closed_message_printed, connector, kill_threads):
    while not kill_threads[0]:
        market_status.update_market_status()
        if market_status.is_market_open:
            if not market_open_message_printed[0]:
                messenger.send('Market is open.. 🎉')
                logger.info("--------------------")
                logger.info('Market is open')
                market_open_message_printed[0] = True
                market_closed_message_printed[0] = False
                connector.connect()
                if connector.is_connected:
                    logger.info("----------------------------------")
                    logger.info("Successfully initialized to MT5.")
                else:
                    logger.info("----------------------------")
                    logger.info("Failed to initialize to MT5. Retrying in 10 seconds.")
        else:
            if not market_closed_message_printed[0]:
                logger.info("--------------------")
                logger.info('Market is closed.')
                messenger.send('Market is closed 😴')
                market_closed_message_printed[0] = True
                market_open_message_printed[0] = False
        time.sleep(10)
        
def create_bots(connector, market_status):
    while not connector:
        logger.info("Waiting for connection to MT5...")
        time.sleep(5)

    logger.info("Successfully connected to MT5.")

    bots = ['bot', 'jut']
    logger.info('bots created')
    logger.info("----------------------------------")
    logger.info('Strategy: Curency Coalition Matrix')

    threads = []
    for bot in bots:
        try:
            bot_thread = threading.Thread(target=bot.run)
            bot_thread.start()
            threads.append(bot_thread)
        except Exception as e:
            logger.error(f"Error creating or starting thread for: {e}")

    return threads, bots

def stop_bots(bots):
    for bot in bots:
        bot.stop()

def main():
    try:      
        # Variable to keep track if threads should be killed
        kill_threads = [False]

        messenger = util.Messenger(cfg.details['webhook_url'])

        # Variable to check if the "Market is closed or opened" message was already printed
        market_closed_message_printed = [False]
        market_open_message_printed = [False]

        # Create an instance of MT5Connector and MarketStatus
        connector = util.MT5Connector(account=cfg.details['account'], password=cfg.details['password'], server=cfg.details['server'])
        market_status = util.MarketStatus(connector)

        

        key_thread = threading.Thread(target=key_capture_thread, args=(kill_threads,))
        key_thread.start()
        logger.info('Press ESC to Terminate Tracy..')

        logger.info("----------------------------------")
        logger.info('Status Thread started...... ')

        update_thread = threading.Thread(target=update_market_status_thread, args=(market_status, messenger, market_open_message_printed, market_closed_message_printed, connector, kill_threads))
        update_thread.start()

        threads, bots = create_bots(connector, market_status)



        # Wait until all threads finish or the key capture thread sets kill_threads to True
        while threads and not kill_threads[0]:
            for thread in threads:
                thread.join(timeout=0.1)
                if not thread.is_alive():
                    threads.remove(thread)

        if kill_threads[0]:
            stop_bots(bots)

        # Stop the market status update thread
        update_thread.join()


        logger.info("All bots have stopped. Exiting...")

    except Exception as e:
        logger.error("An error occurred", exc_info=True)
        # Optionally, you could re-raise the exception if you want the bot to stop
        # raise e

if __name__ == "__main__":
    main()
