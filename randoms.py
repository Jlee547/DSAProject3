coins = [0.25,0.10,0.05,0.01]

coinsAmount = 0.32

def getChange(coins, coinsAmount):
    amountCoins = 0
    for i in coins:
        if coinsAmount//i >=1:
            amountCoins += coinsAmount//i
            coinsAmount = coinsAmount%i

    return amountCoins

print(getChange(coins, coinsAmount))