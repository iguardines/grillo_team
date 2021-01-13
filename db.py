# !pip install PyMySQL
from sqlalchemy import create_engine

import yfinance as yf
import pandas as pd


def getDataM(listado, start='2000-01-01', interval='1d', end=None):
    data = yf.download(listado, start=start, end=end, interval=interval, auto_adjust=True)
    return data.swaplevel(i=1, j=0, axis=1)





#Seteo el USER : PASS @ HOST / BBDD_NAME
sql_engine = create_engine('mysql+pymysql://root:@35.193.28.44/screener_v1')
sql_conn = sql_engine.connect()


#sp500_wiki = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
#sp500_tickers = list(sp500_wiki.Symbol) 
sp500_tickers = ['AMZN' ,'BABA','TSLA' ,'KO' ]
sp500_tickers = [t for t in sp500_tickers if t not in ['BRK.B' ,'BF.B']]


pd.DataFrame(sp500_tickers).to_sql(con=sql_conn, name='sp500tickers', if_exists='replace')

df_sp500 = getDataM(sp500_tickers, start='2012-01-01')

def getDataByYfinance(sp500_tickers):
	tablas = []
	for ticker in sp500_tickers:
        	tabla = df_sp500[ticker].copy()
        	tabla['ticker'] = ticker
        	tabla['variacion'] = tabla.Close.pct_change() *100
        	tabla['volatilidad'] = tabla.variacion.rolling(250).std() * 250**0.5
        	tabla['vol_mln'] = tabla.Volume * tabla.Close / 1000000
        	tabla = tabla.dropna().round(2)
        	tablas.append(tabla)

	return  pd.concat(tablas)

tabla_full = getDataByYfinance(sp500_tickers)
print(tabla_full)

tabla_full.to_excel('df_sp500.xlsx')

tabla_full.to_sql(con=sql_conn, name='sp500', if_exists='replace',chunksize=990500)

print("bye")
