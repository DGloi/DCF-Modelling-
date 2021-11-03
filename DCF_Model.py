import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 400)

years=['2020A','2021B',"2022P","2023P","2024P","2025P"]
sales=pd.Series(index=years)

##
sales["2020A"]= 31.0


##assume growth rates 
growth_rate1=float(0.1)
growth_rate2=float(0.02)


for years in range (1,4):
	sales[years]= float(sales[years-1]*(1+growth_rate1))
for years in range (4,6):
	sales[years]=sales[years-1]*(1+growth_rate2)

#ebita= operating income + D&A
#ebitda_margin= Ebitda/sales
ebitda=pd.Series(years)

##
ebitda_margin1=0.15
ebitda_margin2=0.2
ebitda_margin3=0.3


for years in range(1,2):
	ebitda[years]= sales[years]*ebitda_margin1
for years in range(2,4):
	ebitda[years]=sales[years]*ebitda_margin2
for years in range(4,6):
	ebitda[years]=sales[years]*ebitda_margin3
##
depreciation_rate=0.032

depreciation=sales*depreciation_rate
ebit=ebitda-depreciation
capex_rate=depreciation_rate #add if you need to
capex=-(sales*capex_rate)
##
tax_rate=0.4

tax_payment=-ebit*tax_rate
tax_payment=tax_payment.apply(lambda x : min(x,0))
#NWC = Current Assets (less cash) - Current Liabilities (less debt)= Accounts Receivable + Inventory - Accounts Payable

##
nwc_rate1=0.15
nwc_rate2=0.2
nwc_rate3=0.25

nwc=pd.Series(years)

for years in range (1,2):
	nwc[years]=sales[years]*nwc_rate1
for years in range (1,2):
	nwc[years]=sales[years]*nwc_rate1
for years in range (1,2):
	nwc[years]=sales[years]*nwc_rate1

change_in_nwc=nwc.shift(1)-nwc

free_cash_flow=ebit+depreciation+tax_payment+capex+change_in_nwc

#Creation de la df pour sortie

output = pd.DataFrame([sales, ebitda,free_cash_flow],index=['Sales', 'EBITDA','Free cash flow'])

output.to_excel("/Users/gloinec/Desktop/Test_DCF.xlsx")
print(output) 