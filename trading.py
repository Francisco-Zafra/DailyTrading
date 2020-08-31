#MyKey I0WIR0PK41696HQM

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from pprint import pprint
import json

API_KEY = 'I0WIR0PK41696HQM'

ts = TimeSeries(key=API_KEY)
# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')

output = open('data.json','w')
readable_data = json.dumps(data, indent=4, sort_keys=True)
output.write(readable_data)

output = open('meta_data.json','w')
readable_meta_data = json.dumps(data, indent=4, sort_keys=True)
output.write(readable_meta_data)

# ts = TimeSeries(key=API_KEY, output_format='pandas')
# data, meta_data = ts.get_intraday(symbol='GOOGL',interval='1min', outputsize='full')
# data['4. close'].plot()
# plt.title('Intraday Times Series for the MSFT stock (1 min)')
# plt.show()
