# coingeckoAPI
some functions and calls to make coing gecko data retreival easier


---
## Gets market data for all coins with MCap above specified value
``` /coins/markets: ```     
**URI**: ``` https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=2&page=1&sparkline=false&price_change_percentage=24h ```
``` python
[
  {
    "id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin",
    "image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png?1547033579",
    "current_price": 32823,
    "market_cap": 615470220154,
    "market_cap_rank": 1,
    "fully_diluted_valuation": 689559037163,
    "total_volume": 30706913939,
    "high_24h": 33599,
    "low_24h": 31071,
    "price_change_24h": 1751.74,
    "price_change_percentage_24h": 5.63777,
    "market_cap_change_24h": 33644018114,
    "market_cap_change_percentage_24h": 5.78249,
    "circulating_supply": 18743681,
    "total_supply": 21000000,
    "max_supply": 21000000,
    "ath": 64805,
    "ath_change_percentage": -49.33063,
    "ath_date": "2021-04-14T11:54:46.763Z",
    "atl": 67.81,
    "atl_change_percentage": 48324.46375,
    "atl_date": "2013-07-06T00:00:00.000Z",
    "roi": null,
    "last_updated": "2021-06-27T21:20:28.855Z",
    "price_change_percentage_24h_in_currency": 5.637773796603842
  }
]
```


---
## Gets market data for solana ecosystem tokens
``` /coins/markets: ```   
**URI:** ``` https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=solana-ecosystem&order=market_cap_desc&per_page=250&page=1&sparkline=false ```

---
## Gets all information for the specified coin
``` /coins/{id}: ```
**URI:** ``` https://api.coingecko.com/api/v3/coins/solana?tickers=true&market_data=true&community_data=true&developer_data=true&sparkline=true ```

**This includes twitter handle and description:**       
Twitter handle: ```['links']['twitter_screen_name'] ```     
Description: ``` ['description']['en'] ```

---
## Gets historical information for the specified coin
```
Intervals: 
  ~last 24 hours   = 5 min  intervals
  ~last 90 days    = 1 hour intervals
  ~before 90 days  = 1 day  intervals
```
**URI:** ``` https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1 ```

