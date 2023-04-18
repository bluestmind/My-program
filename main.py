import threading
import time
from first_script import my_function
from second_script import BotzHubUser, events, FROM_CHANNEL, TO_CHANNEL, write_to_log

def main():
    # Call my_function() from the first script
    my_function()

    # Define the function to handle new messages from the Telegram client
    @BotzHubUser.on(events.NewMessage(incoming=True, chats=list(FROM_CHANNEL.keys())))
    async def sender_bH(event):
        # The code for handling incoming messages goes here
        pass

    # Start the Telegram client in a separate thread
    tele_thread = threading.Thread(target=BotzHubUser.run_until_disconnected)
    tele_thread.start()

    # Do something else while the Telegram client is running
    while True:
        print("Working on other stuff...")
        time.sleep(10)

if __name__ == "__main__":
    main()
