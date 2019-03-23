'''
    Variable Interest Rate Loan Calculator

'''

import random
import pandas as pd

# Formats price float dollar string

dollar = lambda x: '${0:.2f}'.format(x)
pct = lambda x: '{0:.2f}%'.format(x*100)

# Generates a random number between 0 and 1 for 5 decimal places
rd = lambda c: (random.randint(1,100000) / 100000) / c

# Calculates your current loan value after payment and interest

loan_val = lambda amt, intpmt, pymt: amt + intpmt - pymt

# Calculates the loan payment derived off a variable interest rate
def pmt(amt, apr, t, T):
    n = amt * (apr / (T - t))
    d = 1 - pow(1 + (apr / (T - t)), -(T - t))
    return n / d

# Calculates the interest payment derived off a variable interest rate
def ipmt(amt, apr, t, T):
    return amt * (apr / (T - t))


if __name__ == '__main__':
    # Define parameters
    beg_amount = 500000
    
    maturity = 75
    compound = 12

    # Computed params
    end_amount = beg_amount
    interest = payment = 0
    periods = maturity * compound
    R = rd(compound)

    # Temporary data storage array
    
    data = []
    
    #print('StartBal\tIPMT\tPMT\tEndBal\n')

    for i in range(1,periods+1,1):
        # Interest and payment start after first deposit period
        if i > 1:
            interest = ipmt(beg_amount, R, i-1, periods)
            payment = pmt(beg_amount, R, i-1, periods)

        # The current balance of your loan
        end_amount = loan_val(beg_amount, interest, payment)

        # Append to data
        data.append([dollar(m) if ii < 4 else pct(m) for ii, m in enumerate([beg_amount, interest, payment, end_amount, R])])
        
        # Random interest rate
        R = rd(compound)

        # Making sure your values don't return non zero value ending balance payments
        beg_amount = end_amount

    # Create a pandas dataframe for presentable format 
    loan_table = pd.DataFrame(data=data, columns=["Start Balance", "Interest Payment", "Loan Payment", "Ending Balance", "Interest Rate"])

    # Prints loan table
    print(loan_table)
