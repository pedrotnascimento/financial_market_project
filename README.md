# Financial market project 

- building a financial market business rule for a future backtest aplication and live market operations


- features:
 - sell_finish and buy_finish methods on strategy
 - strategies:
    - [V] volume rate -> go with the flow
        - (the problem its not the small fish, but the big ones, and the big ones only attack when there is no small fish)
    - [V] consequents bars
        - map stocks that are actually trending real consequent bars
    - trade heatmaps on prices by bar and by absolute time window.
 - filters of trading
 - alert on entering, finishing and on signal
 - build graphic to plot indicators
 - backtest
 - expose interface(api) to commands actions to trade
 
 - modules to be constructed:
    - filtering module [V]
    - filters [V]
    - alerts module [V]
    - statistical module[V]
    - plot module
    - backtest
