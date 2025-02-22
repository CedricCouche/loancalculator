import numpy as np

# For table formatting
import locale 
from tabulate import tabulate


class Loan:
    def __init__(self, capital: int, annual_rate: float, years: int, periods_per_year: int):
        """
        Initialize the Loan object with the necessary parameters.

        Args:
            capital (int): The principal amount of the loan.
            annual_rate (float): The annual interest rate in decimal format (e.g., 0.03 for 3%).
            years (int): The number of years for the loan.
            periods_per_year (int): The number of payment periods per year.
        """
        self.capital = capital
        self.annual_rate = annual_rate
        self.years = years
        self.periods_per_year = periods_per_year
        self.nper = years * periods_per_year  # Total number of payments
        self.periodic_rate = annual_rate / periods_per_year  # Periodic interest rate
        self.pmt = -1 * ( (self.capital * self.periodic_rate) / (1 - (1 + self.periodic_rate) ** (-self.nper)) )
        

    def get_ipmt(self, period: int) -> float:
        """
        Calculate the interest payment for a specific period.

        Args:
            period (int): The payment period number.

        Returns:
            float: The interest payment for the given period.
        """
        
        ipmt = -(self.pmt * ((1 + self.periodic_rate) ** (period - 1) - 1) / self.periodic_rate +
                 self.capital * (1 + self.periodic_rate) ** (period - 1)) * self.periodic_rate
        
        return ipmt
    

    def get_ppmt(self, period: int) -> float:
        """
        Calculate the principal payment for a specific period.

        Args:
            period (int): The payment period number.

        Returns:
            float: The principal payment for the given period.
        """
        
        ppmt_a =  (self.pmt * ( (1 + self.periodic_rate)**(period-1) - 1 ) / self.periodic_rate + self.capital * (1 + self.periodic_rate)**(period-1))
        ppmt = self.pmt + ppmt_a  * self.periodic_rate
        
        return ppmt

    

    def get_loan_schedule(self) -> tuple[list[int], list[float], list[float], list[float]]:
        """
        Generate the loan amortization schedule.

        Returns:
            tuple: A tuple containing lists of periods, interest payments, principal payments, and total payments.
        """
        list_per = []
        list_ipmt = []
        list_ppmt = []
        list_pmt = []

        for i in range(1, self.nper + 1):
            ipmt = self.get_ipmt(i)
            ppmt = self.get_ppmt(i)
            pmt = self.pmt

            list_per.append(i)
            list_ipmt.append(-ipmt)
            list_ppmt.append(-ppmt)
            list_pmt.append(-pmt)

        return list_per, list_ipmt, list_ppmt, list_pmt


    def get_basic_info(self):
        """ Return the basic parameters of the loan
        
        """
        
        print('Capital : ', self.capital)
        print('Annual rate : ', self.annual_rate)
        print('Number of years : ',self.years)
        print('Number of periods per year : ',self.periods_per_year)
        print('Total number of payments : ',self.nper)
        print('Periodic rate : ',self.periodic_rate)
        print('Periodic payment : ',self.pmt)
        print('Total interest paid : ')
        
        
    def get_period_for_targeted_cumulated_interest(self, threshold:float=0.5):
        """ Return the period number corresponding a cumulated target value

        Args:
            - per (list): list of period
            - ipmt (list): list of periodic interest
            - threshold (float, optional): share of interests already paid (cumulative). Defaults to 0.5.

        Returns:
            int: period when cumulated interest goes beyond the threshold
        """
        
        list_period, list_ipmt, _, _ = self.get_loan_schedule()
        
        ipmt_target = np.sum(list_ipmt) * threshold
        ipmt_cum = np.cumsum(list_ipmt)
        
        for p, i in zip(list_period, ipmt_cum):
            
            if i > ipmt_target:
                result = p
                break
        
        print('Period : ', result)
            
            
    def get_situation_at_period(self, period:int=1):
        """ Return the main charateristics of the loan at a given period number

        Args:
            - per (list): list of period

        Returns:
            str: 
        """
        
        list_period, list_ipmt, list_ppmt, list_pmt = self.get_loan_schedule()
        
        try : 
            
            # Find the index corresponding to the period entered
            for i, per in enumerate(list_period):
                if list_period[i] == period:
                    period_idx = i  
            
            
            # Situation at period
            period_at_period = list_period[period_idx]
            ipmt_sum_at_period = np.sum(list_ipmt[:period_idx+1]) 
            ppmt_sum_at_period = np.sum(list_ppmt[:period_idx+1]) 
            pmt_sum_at_period = np.sum(list_pmt[:period_idx+1]) 
            
            # Total of series
            period_max = max(list_period)
            ipmt_sum_total = np.sum(list_ipmt) 
            ppmt_sum_total = np.sum(list_ppmt) 
            pmt_sum_total = np.sum(list_pmt) 
            
            # Display results
            print('Situation of loan at period : ', period_at_period)
            print('Paid capital : ',np.round(ppmt_sum_at_period,2))
            print('Paid interest : ', np.round(ipmt_sum_at_period, 2))
            print('cumulated Payment at period : ', np.round(pmt_sum_at_period,2) )
            print('Remaining Period : ', period_max - period_at_period)
            print('Remaining capital :', np.round( ppmt_sum_total - ppmt_sum_at_period,2))
            print('Remaining interest :', np.round(ipmt_sum_total - ipmt_sum_at_period,2))
            print('Remaining payment :', np.round(pmt_sum_total - pmt_sum_at_period,2) )
            print('total capital :', np.round( ppmt_sum_total,2))
        
        except UnboundLocalError as e1:
            return print('Uncorrect period, available periods are : [', min(list_period),',', max(list_period), ']')


    def formated_depreciation_table(self, table_size:int=12):
        """ Return a formated depreciation schedule

        Args:
            - per (list): list of periods
            - ipmt (list): list of periodic interests
            - ppmt (list): list of periodic capital
            - pmt (list): list of periodic payments
            - table_size (int, optional): number of periods used to split the table. Defaults to 12.

        Returns:
            table: formated depreciation table
        """
        
        # To use default Operating Système regional settings
        locale.setlocale(locale.LC_ALL, '')
        
        
        # temp
        per, ipmt, ppmt, pmt = self.get_loan_schedule()
        
        # Headers
        headers_FR = ["Echéance", "Mensualité\néchéance", "Capital\néchéance", "Intérêts\néchéance", "Capital\ncumulé", "Intérêts\ncumulé", "Capital\nrestant", "Intérêts\nrestants"]
        headers_ENG = ["Period", "Payment\nPeriodic", "Principal\nPeriodic", "Interest\nPeriodic", "Principal\nCumulated", "Interest\nCumulated", "Principal\nremaining", "Interest\nremaining"]

        
        # First Initialization of the list
        loan_table = []

        # Table size definition
        list_per_cut = np.arange(0, np.max(per), table_size)
        period_start = 0
        period_end = 0
        
        # Loop
        for i in range(min(per), max(per) ):
            
            period_start = period_end
            
            periodic_payment = pmt[i]
            principal_periodic = ppmt[i]
            interest_periodic = ipmt[i]
            principal_cumulated = np.sum(ppmt[:i+1])
            interest_cumulated = np.sum(ipmt[:i+1])
            principal_remaining = np.sum(ppmt) - principal_cumulated
            interest_remaining = np.sum(ipmt) - interest_cumulated

            # Built of the periodic line
            periodic_line = [
                i, 
                locale._format('%.2f', periodic_payment ),
                locale._format('%.2f', principal_periodic ),
                locale._format('%.2f', interest_periodic ),
                locale._format('%.2f', principal_cumulated ),
                locale._format('%.2f', interest_cumulated ),
                locale._format('%.2f', principal_remaining ),
                locale._format('%.2f', interest_remaining )
                ]
            
            if not i in list_per_cut:

                # Add of the periodic line inside the table
                loan_table.append(periodic_line)
                
                
            if i in list_per_cut:
                
                period_end = i
                
                # Add of the periodic line inside the table
                loan_table.append(periodic_line)

                print(tabulate(loan_table, headers = headers_FR, tablefmt="fancy_grid"))
                print("Total périodes : ",period_start, " - ", period_end, '-' * 78)
                print("Capital cumulé : ", locale._format('%.2f', principal_cumulated ))
                print("Intérêts cumulés : ", locale._format('%.2f', interest_cumulated ))
                print('-' * 105)
                print(" ")
                
                loan_table = []

        return "End"