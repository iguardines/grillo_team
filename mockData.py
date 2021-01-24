from datetime import datetime as dt
import csv

def get_mock_data_market():
  while True:
    with open('Evolucion_index_20201217.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
          try:
            eachRow = {'IndiceBTCMtR': row[0], 'LiquidezMedida': row[1], 'CostofTrade': row[2], 'time': str(dt.now())}
            yield eachRow
          except StopIteration:
            pass