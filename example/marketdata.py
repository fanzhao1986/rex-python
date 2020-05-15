# -*- coding: utf-8 -*-
# Copyright (C) 2020 Reactive Markets Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import asyncio
import random

from reactive.platform.feed.client import FeedClient
from reactive.platform.feed.handler import print_handler

MARKET_LIST = ["EURUSD-REX", "EURGBP-REX", "EURCHF-REX", "EURRON-REX", "USDCAD-REX",
               "USDCHF-REX", "USDJPY-REX", "USDCHF-REX", "EURJPY-REX", "AUDUSD-REX",
               "BTCUSD-BFN", "ETHUSD-BFN", "LTCUSD-BFN", "XRPUSD-BFN",
               "BCHUSDT-BIN", "BTCUSDT-BIN", "ETHUSDT-BIN", "LTCUSDT-BIN", "XRPUSDT-BIN",
               "BCHUSD-CNB", "BTCUSD-CNB", "ETHUSD-CNB", "LTCUSD-CNB", "XRPUSD-CNB"]
TOKEN = ""
ADDR = "wss://api.platform.reactivemarkets.com/feed"


def random_market():
    index = random.randint(0, len(MARKET_LIST) - 1)
    return MARKET_LIST[index]


async def client_handler(c: FeedClient):
    """
    implement an application client_handler coroutine to and subscribe or
    unsubscribe marketdata.
    """

    # unknown markets, expect an reject message
    await c.subscribe(["BTCUSD-CME"], depth=10, grouping=1)

    while True:
        market = random_market()
        print("sub", market)
        await c.subscribe([market], depth=0, grouping=0)
        await c.subscribe([market], depth=5)
        await asyncio.sleep(3)
        print("unsub", market)
        await c.unsubscribe([market], depth=0, grouping=0)
        await c.unsubscribe([market], depth=5)
        await asyncio.sleep(1)


def run():
    client = FeedClient(addr=ADDR, key=TOKEN, close_timeout=1.0)
    run = asyncio.ensure_future(client.run(client_handler=client_handler,
                                           data_handler=print_handler))
    asyncio.get_event_loop().run_until_complete(run)


if __name__ == "__main__":
    run()
