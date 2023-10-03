# Financial market project 

- building a financial market business rule for a future backtest aplication and live market operations


- features:
    - [&#10004;]sell_finish and buy_finish methods on strategy
    - strategies:
        - [ ] volume integral -> sum of the volume rate watching for buy and sells
        - [&#10004;] volume rate -> go with the flow
            - (the problem its not the small fish, but the big ones, and the big ones only attack when there is no small fish)
        - [&#10004;] consequents bars
            - map stocks that are actually trending real consequent bars
        - trade heatmaps on prices by bar and by absolute time window.
    - [&#10004;] filters of trading
    - [&#10004;] alert on entering, finishing and on signal
    - backtest
    - build graphic to plot indicators
    - expose interface(api) to commands actions to trade
    
    - modules to be constructed:
        - filtering module [&#10004;]
        - filters [&#10004;]
        - alerts module [&#10004;]
        - statistical module[&#10004;]
        - plot module
        - backtest
