import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 400)

years = ["2020A", "2021B", "2022P", "2023P", "2024P", "2025P"]
sales = pd.Series(dtype='float64', index=years)
sales['2020A'] = 80.0

Repetition = 10000


def MonteCarloSim():
    # Let's create the distributions
    sales_growth1 = np.random.normal(loc=0.1, scale=0.01, size=Repetition)
    sales_growth2 = np.random.normal(loc=0.1, scale=0.04, size=Repetition)
    sales_growth3 = np.random.normal(loc=0.1, scale=0.08, size=Repetition)

    ebitda_margin1 = np.random.normal(loc=0.14, scale=0.01, size=Repetition)
    ebitda_margin2 = np.random.normal(loc=0.19, scale=0.08, size=Repetition)
    ebitda_margin3 = np.random.normal(loc=0.25, scale=0.1, size=Repetition)

    depr_percent1 = np.random.normal(loc=0.032, scale=0.01, size=Repetition)
    depr_percent2 = np.random.normal(loc=0.04, scale=0.05, size=Repetition)
    depr_percent3 = np.random.normal(loc=0.08, scale=0.1, size=Repetition)

    nwc_percent1 = np.random.normal(loc=0.024, scale=0.01, size=Repetition)
    nwc_percent2 = np.random.normal(loc=0.028, scale=0.04, size=Repetition)
    nwc_percent3 = np.random.normal(loc=0.030, scale=0.05, size=Repetition)

    capex_percent1 = np.random.normal(loc=0.024, scale=0.01, size=Repetition)
    capex_percent2 = np.random.normal(loc=0.018, scale=0.05, size=Repetition)
    capex_percent3 = np.random.normal(loc=0.010, scale=0.15, size=Repetition)

    # Calculation of the DCF values and Terminal value of the firm

    output_distribution = []
    for i in range(Repetition):
        for year in range(1, 2):
            sales[year] = sales[year - 1] * (1 + sales_growth1[i])
        for year in range(2, 4):
            sales[year] = sales[year - 1] * (1 + sales_growth2[i])
        for year in range(4, 6):
            sales[year] = sales[year - 1] * (1 + sales_growth3[i])

        ebitda = pd.Series(dtype='float64', index=["2020A", "2021B", "2022P", "2023P", "2024P", "2025P"])

        for years in range(0, 2):
            ebitda[years] = sales[years] * ebitda_margin1[i]
        for years in range(2, 4):
            ebitda[years] = sales[years] * ebitda_margin2[i]
        for years in range(4, 6):
            ebitda[years] = sales[years] * ebitda_margin3[i]

        depreciation = pd.Series(dtype='float64',
                                 index=["2020A", "2021B", "2022P", "2023P", "2024P", "2025P"])

        for years in range(0, 2):
            depreciation[years] = sales[years] * depr_percent1[i]
        for years in range(2, 4):
            depreciation[years] = sales[years] * depr_percent2[i]
        for years in range(4, 6):
            depreciation[years] = sales[years] * depr_percent3[i]

        ebit = ebitda - depreciation

        nwc = pd.Series(dtype='float64', index=["2020A", "2021B", "2022P",
                                                "2023P", "2024P", "2025P"])

        for years in range(0, 2):
            nwc[years] = sales[years] * nwc_percent1[i]
        for years in range(2, 4):
            nwc[years] = sales[years] * nwc_percent2[i]
        for years in range(4, 6):
            nwc[years] = sales[years] * nwc_percent3[i]

        change_in_nwc = nwc.shift(1) - nwc

        tax_rate = 0.25
        tax_payment = -ebit * tax_rate
        tax_payment = tax_payment.apply(lambda x: min(x, 0))

        capex = pd.Series(dtype='float64',
                          index=["2020A", "2021B", "2022P", "2023P", "2024P", "2025P"])

        for years in range(0, 2):
            capex[years] = -(sales[years] * capex_percent1[i])
        for years in range(2, 4):
            capex[years] = -(sales[years] * capex_percent2[i])
        for years in range(4, 6):
            capex[years] = -(sales[years] * capex_percent3[i])

        free_cash_flow = ebit + depreciation + tax_payment + capex + change_in_nwc
        # CostE =(dividends/share n+1/current market/share) + growth rate of dividends
        # Using CAPM model : CostE= Riskfreerate + B¨(expected return- Riskfree rate)
        # WACC = %E * costE +%debt * cost of debt * (1 – corporate tax rate)
        cost_of_equity = 0.12
        cost_of_debt = 0.17
        share_of_equity = 0.6
        WACC = cost_of_equity * share_of_equity + cost_of_debt * (1 - share_of_equity)
        terminal_growth = 0.02
        terminal_value = (free_cash_flow[-1] * (1 + terminal_growth) / (WACC - terminal_growth))
        free_cash_flow[-1] = terminal_value
        discount_factors = [(1 / (1 + WACC)) ** i for i in range(1, 6)]
        dcf_value = sum(free_cash_flow[1:6] * discount_factors)
        output_distribution.append(dcf_value)
        output = pd.DataFrame(
            [sales, ebitda, depreciation, ebit, nwc, change_in_nwc, capex, tax_payment, free_cash_flow], index=[
                'Sales', 'EBITDA', 'depreciation', 'EBIT', "Net Working Capital", "Change in NWC", "CAPEX", "Tax",
                "Free Cash Flow"]).round(2)
    return output_distribution


plt.hist(MonteCarloSim(), bins=30, density=True, alpha=0.9, color="g")
plt.xlabel('Enterprise Value in millions of USD')
plt.ylabel('Probability')
plt.title("Histogram of Company's most probable valuation ")
plt.savefig("monte-carlo-DCF-simulation.svg")
