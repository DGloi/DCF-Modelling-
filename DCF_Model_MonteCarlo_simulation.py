import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 400)

years=["2020A","2021B","2022P","2023P","2024P","2025P"]
sales = pd.Series(index=years)
sales['2020A'] = 31.0  
growth_rate1 = 0.1
growth_rate2 = 0.1
growth_rate3 = 0.1
for year in range(1, 2):
    sales[year] = sales[year - 1] * (1 + growth_rate1)
for year in range(2,4):
    sales[year] = sales[year - 1] * (1 + growth_rate2)
for year in range(4,6):
    sales[year] = sales[year - 1] * (1 + growth_rate3)


ebitda=pd.Series(index=years)
ebitda_margin1 = 0.14
ebitda_margin2 = 0.14
ebitda_margin3 = 0.14
for years in range(0,2):
	ebitda[years]= sales[years]*ebitda_margin1
for years in range(2,4):
	ebitda[years]=sales[years]*ebitda_margin2
for years in range(4,6):
	ebitda[years]=sales[years]*ebitda_margin3

depreciation=pd.Series(index=["2020A","2021B","2022P","2023P","2024P","2025P"])
depr_percent1 = 0.032
depr_percent2 = 0.032
depr_percent3 = 0.032
for years in range(0,2):
	depreciation[years]= sales[years]*depr_percent1
for years in range(2,4):
	depreciation[years]=sales[years]*depr_percent2
for years in range(4,6):
	depreciation[years]=sales[years]*depr_percent3


ebit = ebitda - depreciation

nwc=pd.Series(index=["2020A","2021B","2022P","2023P","2024P","2025P"])
nwc_percent1 = 0.24
nwc_percent2 = 0.24
nwc_percent3 = 0.24
for years in range(0,2):
	nwc[years]= sales[years]*nwc_percent1
for years in range(2,4):
	nwc[years]=sales[years]*nwc_percent2
for years in range(4,6):
	nwc[years]=sales[years]*nwc_percent3

change_in_nwc = nwc.shift(1) - nwc 

tax_rate = 0.25
tax_payment = -ebit * tax_rate
tax_payment = tax_payment.apply(lambda x: min(x, 0))

capex=pd.Series(index=["2020A","2021B","2022P","2023P","2024P","2025P"])
capex_percent1 = depr_percent1#+ 0,2
capex_percent2 = depr_percent2#+0,15
capex_percent3 = depr_percent3#+0,1

for years in range(0,2):
	capex[years]= -(sales[years]*capex_percent1)
for years in range(2,4):
	capex[years]=-(sales[years]*capex_percent2)
for years in range(4,6):
	capex[years]=-(sales[years]*capex_percent3)

free_cash_flow = ebit + depreciation + tax_payment + capex + change_in_nwc
#CostE =(dividends/share n+1/current market/share) + growth rate of dividends
#Using CAPM model : CostE= Riskfreerate + B¨(expected return- Riskfree rate)
#WACC = %E * costE +%debt * cost of debt * (1 – corporate tax rate)

cost_of_equity=0.12
cost_of_debt=0.17
share_of_equity=0.6 
WACC=cost_of_equity*share_of_equity+cost_of_debt*(1-share_of_equity)
terminal_growth=0.02
terminal_value = ((free_cash_flow[-1]*(1+terminal_growth))/(WACC-terminal_growth))


output = pd.DataFrame([sales,ebitda,depreciation,ebit,nwc,change_in_nwc,capex,tax_payment,free_cash_flow],index=['Sales', 'EBITDA', 'depreciation','EBIT',"Net Working Capital","Change in NWC","CAPEX","Tax","Free Cash Flow"]).round(2)
print(output)
print(terminal_value)
output.to_excel("/Users/gloinec/Documents/GitHub/DCF-Modelling-/test_DCF.xlsx")




