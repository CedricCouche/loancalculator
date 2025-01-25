import numpy as np
import locale
from decimal import Decimal, getcontext
from typing import List, Tuple

# for PDF print
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


# Set high precision for financial calculations
getcontext().prec = 10

class Loan:
    def __init__(self, capital: int, annual_rate: float, years: int, periods_per_year: int):
        if capital <= 0 or annual_rate <= 0 or years <= 0 or periods_per_year <= 0:
            raise ValueError("All parameters must be positive.")
        
        self.capital = Decimal(str(capital))
        self.annual_rate = Decimal(str(annual_rate))
        self.years = years
        self.periods_per_year = periods_per_year
        self.nper = years * periods_per_year
        self.periodic_rate = self.annual_rate / Decimal(str(periods_per_year))
        self.pmt = self._calculate_pmt()
        self.schedule = self._generate_schedule()

    def _calculate_pmt(self) -> Decimal:
        """Calculate the periodic payment (PMT)."""
        rate = self.periodic_rate
        numerator = rate * self.capital
        denominator = 1 - (1 + rate) ** (-self.nper)
        return -numerator / denominator

    def _generate_schedule(self) -> Tuple[List[int], List[Decimal], List[Decimal], List[Decimal]]:
        """Generate the full amortization schedule upfront."""
        periods, ipmt_list, ppmt_list, pmt_list = [], [], [], []
        remaining_balance = self.capital
        
        for period in range(1, self.nper + 1):
            interest = remaining_balance * self.periodic_rate
            principal = self.pmt - interest
            remaining_balance -= principal
            
            periods.append(period)
            ipmt_list.append(interest)
            ppmt_list.append(principal)
            pmt_list.append(self.pmt)
        
        return periods, ipmt_list, ppmt_list, pmt_list

    def get_payment(self) -> float:
        """Return the periodic payment."""
        return float(self.pmt)

    def get_interest_payment(self, period: int) -> float:
        """Return the interest payment for a specific period."""
        self._validate_period(period)
        return float(self.schedule[1][period-1])

    def get_principal_payment(self, period: int) -> float:
        """Return the principal payment for a specific period."""
        self._validate_period(period)
        return float(self.schedule[2][period-1])

    def _validate_period(self, period: int):
        if not 1 <= period <= self.nper:
            raise ValueError(f"Period must be between 1 and {self.nper}.")

    # ... (other methods like total_interest_paid, remaining_balance, etc.)

    def formatted_table(self, locale_code: str = 'en_US') -> List[List[str]]:
        """Generate a formatted table using locale settings."""
        try:
            locale.setlocale(locale.LC_ALL, locale_code)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')
        
        headers = ["Period", "Payment", "Principal", "Interest", "Remaining Balance"]
        table = []
        
        for period in range(self.nper):
            row = [
                f"{self.schedule[0][period]}",
                locale.currency(float(self.schedule[3][period]), grouping=True),
                locale.currency(float(self.schedule[2][period]), grouping=True),
                locale.currency(float(self.schedule[1][period]), grouping=True),
                locale.currency(float(self.schedule[2][period]), grouping=True)
            ]
            table.append(row)
        
        return table
    
    def _validate_period(self, period: int):
        """Validate that the period is within the loan term."""
        if not 1 <= period <= self.nper:
            raise ValueError(f"Period must be between 1 and {self.nper}.")

    def get_interest_payment(self, period: int) -> float:
        """
        Return the interest payment for a specific period (positive value).
        
        Args:
            period (int): Payment period number (1-based index).
        
        Returns:
            float: Interest payment amount for the period.
        """
        self._validate_period(period)
        return -self.IPMT(period)  # Convert negative result to positive

    def get_principal_payment(self, period: int) -> float:
        """
        Return the principal payment for a specific period (positive value).
        
        Args:
            period (int): Payment period number (1-based index).
        
        Returns:
            float: Principal payment amount for the period.
        """
        self._validate_period(period)
        return -self.PPMT(period)  # Convert negative result to positive


    def generate_summary_pdf(self, filename: str = "loan_summary.pdf"):
        """
        Generate a PDF summary of the loan details.
        
        Args:
            filename (str): Output PDF filename. Defaults to "loan_summary.pdf".
        """
        # Create a PDF canvas
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 50, "Loan Summary Report")

        # Loan Details
        c.setFont("Helvetica", 12)
        y = height - 100
        details = [
            ("Principal", f"{locale.currency(self.capital, grouping=True)}"),
            ("Annual Rate", f"{self.annual_rate * 100:.2f}%"),
            ("Term (Years)", f"{self.years}"),
            ("Periods/Year", f"{self.periods_per_year}"),
            ("Periodic Rate", f"{self.periodic_rate * 100:.2f}%"),
            ("Total Payments", f"{self.nper}"),
            ("Periodic Payment", f"{locale.currency(-self.PMT(), grouping=True)}"),
            ("Total Interest Paid", f"{locale.currency(self.total_interest_paid(), grouping=True)}"),
            ("Total Principal Paid", f"{locale.currency(self.total_principal_paid(), grouping=True)}")
        ]

        # Draw details
        for label, value in details:
            c.drawString(100, y, f"{label}: {value}")
            y -= 20

        # Amortization Schedule Table (First 12 periods)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y - 40, "Amortization Schedule (First 12 Periods):")

        # Get schedule data
        periods, ipmt, ppmt, pmt = self.loan_schedule()
        table_data = [["Period", "Payment", "Principal", "Interest", "Remaining Balance"]]
        for i in range(12):
            if i >= len(periods):
                break
            remaining_balance = self.remaining_balance(periods[i])
            table_data.append([
                str(periods[i]),
                locale.currency(pmt[i], grouping=True),
                locale.currency(ppmt[i], grouping=True),
                locale.currency(ipmt[i], grouping=True),
                locale.currency(remaining_balance, grouping=True)
            ])

        # Create and style the table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Draw the table
        table.wrapOn(c, width - 200, height)
        table.drawOn(c, 100, y - 200)

        # Save the PDF
        c.save()