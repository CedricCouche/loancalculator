

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


