import StockTwitsAPI as api

twit = api.Twits()

scraped = twit.scrape_ticker('SPY', lookback_volume = 10000)

print(scraped[0])
