def max_profit(max_trades, daily_prices):
    if not daily_prices or max_trades == 0:
        return 0

    n = len(daily_prices)

    if max_trades >= n // 2:
        profit = 0
        for i in range(1, n):
            if daily_prices[i] > daily_prices[i - 1]:
                profit += daily_prices[i] - daily_prices[i - 1]
        return profit

    dp = [[0] * n for _ in range(max_trades + 1)]

    for t in range(1, max_trades + 1):
        max_diff = -daily_prices[0]
        for d in range(1, n):
            dp[t][d] = max(
                dp[t][d - 1],               
                daily_prices[d] + max_diff 
            )
            max_diff = max(
                max_diff,
                dp[t - 1][d] - daily_prices[d]
            )

    return dp[max_trades][n - 1]

prices = [2000, 4000, 1000]
max_trades = 2

result = max_profit(max_trades, prices)
print("Maximum Profit:", result)
