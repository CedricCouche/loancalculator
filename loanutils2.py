import numpy as np
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

    def PMT(self) -> float:
        """
        Calculate the periodic payment for the loan.

        Returns:
            float: The periodic payment amount.
        """
        pmt = (self.capital * self.periodic_rate) / (1 - (1 + self.periodic_rate) ** (-self.nper))
        return -pmt

    def IPMT(self, period: int) -> float:
        """
        Calculate the interest payment for a specific period.

        Args:
            period (int): The payment period number.

        Returns:
            float: The interest payment for the given period.
        """
        pmt = self.PMT()
        ipmt = -(pmt * ((1 + self.periodic_rate) ** (period - 1) - 1) / self.periodic_rate +
                 self.capital * (1 + self.periodic_rate) ** (period - 1)) * self.periodic_rate
        return ipmt

    def PPMT(self, period: int) -> float:
        """
        Calculate the principal payment for a specific period.

        Args:
            period (int): The payment period number.

        Returns:
            float: The principal payment for the given period.
        """
        pmt = self.PMT()
        ipmt = self.IPMT(period)
        ppmt = pmt - ipmt
        return ppmt

    def loan_schedule(self) -> tuple[list[int], list[float], list[float], list[float]]:
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
            ipmt = self.IPMT(i)
            ppmt = self.PPMT(i)
            pmt = self.PMT()

            list_per.append(i)
            list_ipmt.append(-ipmt)
            list_ppmt.append(-ppmt)
            list_pmt.append(-pmt)

        return list_per, list_ipmt, list_ppmt, list_pmt

    def total_interest_paid(self) -> float:
        """
        Calculate the total interest paid over the life of the loan.

        Returns:
            float: The total interest paid.
        """
        total_interest = sum([self.IPMT(i) for i in range(1, self.nper + 1)])
        return -total_interest

    def total_principal_paid(self) -> float:
        """
        Calculate the total principal paid over the life of the loan.

        Returns:
            float: The total principal paid.
        """
        total_principal = sum([self.PPMT(i) for i in range(1, self.nper + 1)])
        return -total_principal

    def remaining_balance(self, period: int) -> float:
        """
        Calculate the remaining balance of the loan after a specific period.

        Args:
            period (int): The payment period number.

        Returns:
            float: The remaining balance after the given period.
        """
        pmt = self.PMT()
        remaining_balance = self.capital * (1 + self.periodic_rate) ** period - \
                            pmt * (((1 + self.periodic_rate) ** period - 1) / self.periodic_rate)
        return remaining_balance

    def find_per_cumul_interest(self, threshold: float = 0.5) -> int:
        """
        Return the period number corresponding to a cumulative interest threshold.

        Args:
            threshold (float, optional): Share of total interest already paid (cumulative). Defaults to 0.5.

        Returns:
            int: The period when cumulative interest exceeds the threshold.
        """
        _, ipmt, _, _ = self.loan_schedule()
        ipmt_target = np.sum(ipmt) * threshold
        ipmt_cum = np.cumsum(ipmt)

        for p, i in zip(range(1, self.nper + 1), ipmt_cum):
            if i > ipmt_target:
                return p

    def unformated_depreciation_table(self):
        """
        Return a semi-formatted depreciation schedule.

        Returns:
            list: A list containing the depreciation table.
        """
        # Use default OS regional settings
        locale.setlocale(locale.LC_ALL, '')

        # Headers
        headers_FR = ["Echéance", "Mensualité\néchéance", "Capital\néchéance", "Intérêts\néchéance", "Capital\ncumulé", "Intérêts\ncumulé", "Capital\nrestant", "Intérêts\nrestants"]
        headers_ENG = ["Period", "Payment\nPeriodic", "Principal\nPeriodic", "Interest\nPeriodic", "Principal\nCumulated", "Interest\nCumulated", "Principal\nremaining", "Interest\nremaining"]

        # Get loan schedule
        per, ipmt, ppmt, pmt = self.loan_schedule()

        # Initialize the list
        loan_table = []

        # Loop
        for i in range(len(per)):
            periodic_payment = pmt[i]
            principal_periodic = ppmt[i]
            interest_periodic = ipmt[i]
            principal_cumulated = np.sum(ppmt[:i + 1])
            interest_cumulated = np.sum(ipmt[:i + 1])
            principal_remaining = np.sum(ppmt) - principal_cumulated
            interest_remaining = np.sum(ipmt) - interest_cumulated

            # Build the periodic line
            periodic_line = [
                per[i],
                locale.format_string('%.2f', periodic_payment, grouping=True),
                locale.format_string('%.2f', principal_periodic, grouping=True),
                locale.format_string('%.2f', interest_periodic, grouping=True),
                locale.format_string('%.2f', principal_cumulated, grouping=True),
                locale.format_string('%.2f', interest_cumulated, grouping=True),
                locale.format_string('%.2f', principal_remaining, grouping=True),
                locale.format_string('%.2f', interest_remaining, grouping=True)
            ]

            # Add the periodic line to the table
            loan_table.append(periodic_line)

        # Print the table
        print(tabulate(loan_table, headers=headers_FR, tablefmt="fancy_grid"))

        return loan_table

    def formated_depreciation_table(self, table_size: int = 12):
        """
        Return a formatted depreciation schedule.

        Args:
            table_size (int, optional): Number of periods used to split the table. Defaults to 12.

        Returns:
            str: "End" after printing the formatted tables.
        """
        # Use default OS regional settings
        locale.setlocale(locale.LC_ALL, '')

        # Headers
        headers_FR = ["Echéance", "Mensualité\néchéance", "Capital\néchéance", "Intérêts\néchéance", "Capital\ncumulé", "Intérêts\ncumulé", "Capital\nrestant", "Intérêts\nrestants"]
        headers_ENG = ["Period", "Payment\nPeriodic", "Principal\nPeriodic", "Interest\nPeriodic", "Principal\nCumulated", "Interest\nCumulated", "Principal\nremaining", "Interest\nremaining"]

        # Get loan schedule
        per, ipmt, ppmt, pmt = self.loan_schedule()

        # Initialize the list
        schedule_table = []
        loan_table = []

        # Table size definition
        list_per_cut = np.arange(0, self.nper, table_size)
        period_start = 0
        period_end = 0

        # Loop
        for i in range(len(per)):
            period_start = period_end

            periodic_payment = pmt[i]
            principal_periodic = ppmt[i]
            interest_periodic = ipmt[i]
            principal_cumulated = np.sum(ppmt[:i + 1])
            interest_cumulated = np.sum(ipmt[:i + 1])
            principal_remaining = np.sum(ppmt) - principal_cumulated
            interest_remaining = np.sum(ipmt) - interest_cumulated

            # Build the periodic line
            periodic_line = [
                per[i],
                locale.format_string('%.2f', periodic_payment, grouping=True),
                locale.format_string('%.2f', principal_periodic, grouping=True),
                locale.format_string('%.2f', interest_periodic, grouping=True),
                locale.format_string('%.2f', principal_cumulated, grouping=True),
                locale.format_string('%.2f', interest_cumulated, grouping=True),
                locale.format_string('%.2f', principal_remaining, grouping=True),
                locale.format_string('%.2f', interest_remaining, grouping=True)
            ]

            if per[i] - 1 not in list_per_cut:
                loan_table.append(periodic_line)

            if per[i] - 1 in list_per_cut:
                period_end = per[i]
                loan_table.append(periodic_line)

                # Print the table
                print(tabulate(loan_table, headers=headers_FR, tablefmt="fancy_grid"))
                print(f"Total périodes : {period_start} - {period_end}", '-' * 78)
                print("Capital cumulé :", locale.format_string('%.2f', principal_cumulated, grouping=True))
                print("Intérêts cumulés :", locale.format_string('%.2f', interest_cumulated, grouping=True))
                print('-' * 105)
                print(" ")
                
                schedule_table.append(loan_table) 
                loan_table = []
            
            

        return schedule_table

