import markets

suggested = []

def check_odds(array, markets, stat):
    for market in markets:
        print("Market: " + str(market) + "+ " + stat)
        winning_odds = check_market_hit(array, market)
        print("Minimum Winning Odds: " + str(winning_odds) + "\n")
        if (int(winning_odds) >= 1 and int(winning_odds) <= 2):
            suggested.append(str(market) + "+ " + stat + " min odds: " + str(winning_odds))
    

            
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
        return 0
