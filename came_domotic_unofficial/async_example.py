import asyncio


class MyServer:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self._elements_list = None
        self._httpclient = None
        self._keep_alive_task = None
        self._command_sequence = 0
        self._command_sequence_lock = asyncio.Lock()

    @property
    async def elements_list(self):
        if self._elements_list is None:
            self._elements_list = await self._fetch_elements_list()
        return self._elements_list

    async def _fetch_elements_list(self):
        # Replace with the actual URL and parameters
        url = f"http://{self.host}/api/elements"
        params = {"username": self.username, "password": self.password}

        async with self._httpclient.get(url, params=params) as response:
            return await response.json()

    async def _increment_command_sequence(self):
        """
        Uses the "with" statement to acquire the lock, increment
        the _command_sequence attribute, and then release the lock.
        This ensures that the _command_sequence attribute is incremented
        safely, even if multiple tasks are trying to increment it
        at the same time.
        """
        async with self._command_sequence_lock:
            self._command_sequence += 1
            return self._command_sequence

    async def _keep_alive(self):
        while True:
            # Replace with the actual URL and parameters
            url = f"http://{self.host}/api/keep_alive"
            params = {"username": self.username, "password": self.password}

            async with self._httpclient.post(url, params=params):
                pass

            await asyncio.sleep(60)  # Sleep for 60 seconds

    async def close(self):
        self._keep_alive_task.cancel()
        await self._httpclient.close()


# Usage
async def main():
    server = MyServer("localhost", "username", "password")
    elements_list = await server.elements_list
    print(elements_list)
    await server.close()


# Run the example
asyncio.run(main())
