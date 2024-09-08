import strategy

store_strategy_map = {
    "walmart" : {
        'strategy': strategy.WalmartStrategy(),
        'id_adapter': 'f781b57d74d0'},
    "oxxo" : {strategy.OxxoStrategy()},
    "liverpool": {strategy.LiverpoolStrategy()}
}