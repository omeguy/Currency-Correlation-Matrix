import MetaTrader5 as mt5

# MetaTrader 5 credentials
details = dict(
    account = 5020598211,
    password = 'Vf!o5eYc',
    server = 'MetaQuotes-Demo', 
    webhook_url = 'https://discordapp.com/api/webhooks/1186814711031922778/iVImTjDYvHkNpLLM__uSZQ3P9mZKd4R9Pmy6lt8mgAWWDMIaGibPjsEj5tw8_wW_ipgZ'
)

# User-defined variables
symbols = ['EURUSD', 'EURJPY']
timeframe = mt5.TIMEFRAME_M15
lot = 0.01
from_data = 1
to_data = 16
deviation = 10
magic1 = 360
magic2 = 361
magic3 = 362
pip_range = 10
tp_pips = 50
atr_sl_multiplier = 0.1
atr_period = 14
max_dist_atr_multiplier = 0.4
trail_atr_multiplier = 0.2
