import markets

def point_odds(point_array):
    for market in markets.POINT_MARKETS:
        print("Market: " + str(market) + "+ Points")
        winning_odds = check_market_hit(point_array, market)
        print("Minimum Winning Odds: " + str(winning_odds) + "\n")
    
        
            
def check_market_hit(stat_array, market):
    count = 0;
    for stat in stat_array:
        if (int(stat) >= market):
            count += 1
    if count > 0:
        hit_rate = (count / 5)
        odds = 1 / hit_rate
        return odds
    else:
        return "N/A - no last 5 hits"
