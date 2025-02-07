from pypresence import Presence
from time import localtime, mktime
from asyncio import get_event_loop

class DiscordRPC(object):
    def __init__(self, client_id: str, auto_connect: bool = True) -> None:
        self.client_id = client_id
        self.running = False

        try:
            if (self.client_id):
                self.rpc_client = Presence(client_id)
                if (auto_connect):
                    self.rpc_client.connect()
                    self.running = True
            else:
                self.rpc_client = None
        except Exception as e:
            self.rpc_client = None

        self.activity = None

        self.start_time = mktime(localtime())

    def __del__(self):
        self.stop()

    def is_connected(self):
        return (self.rpc_client is not None)

    def retry_connection(self):
        self.running = False

        if (not self.client_id):
            return

        try:
            self.rpc_client = Presence(self.client_id)
            self.rpc_client.connect()
            self.running = True
        except Exception:
            self.rpc_client = None

    def set_status(self, state: str, details: str, small_text: str, large_text: str, small_image: str, large_image: str):
        if (not self.rpc_client or not self.running):
            return

        self.activity = {
            "state": state,
            "details": details,
            "timestamps": {
                "start": self.start_time
            },
            "assets": {
                "small_text": small_text,
                "small_image": small_image,
                "large_text": large_text,
                "large_image": large_image
            }
        }

        self.rpc_client.update(
            state=self.activity["state"],
            details=self.activity["details"],
            start=self.activity["timestamps"]["start"],
            small_text=self.activity["assets"]["small_text"],
            small_image=self.activity["assets"]["small_image"],
            large_text=self.activity["assets"]["large_text"],
            large_image=self.activity["assets"]["large_image"],
        )

    def stop(self):
        if (self.rpc_client):
            self.rpc_client = None
            self.running = False
