# Loan Calculator


## Goals : 
    1) create a tool that calculate loan and various usual secondary calculation.
    2) display loan schedule in a text format
    3) display loan schedule and basic info in a PDF format
    4) code is written in OOP style and stored in a .py file


## Available fonctionnalities :

- get_ppmt(period) : return the principal part of the payment for a given period
- get_ipmt(period) : return the interest part of the payment for a given period
- get_basic_info() : return the basic info of the loan
- get_situation_at_period(period) : get the situation of the loan at a given period 
- get_period_for_targeted_cumulated_interest(threshold=0.5) : return the period where the cumulated interest share in reached
- get_formated_depreciation_table() : return a formated loan schedule in text, no useful but fun to built
- draw_graph(filename) : return a graph containing overall shape of the loan, stored in a png file
- generate_summary_pdf(FileName) : return a loan schedule and some general info about the loan. Main method of this project.

Secondary methods : aimed to be used by other methods
- _get_loan_schedule() : return 4 differents list containing periods, periodic interest, periodic principal, periodic payment
- _drawMyRuler() : draw x & y landmarks on the PDF page, visual help to position objets
- _get_summary() : built summary table used in generate_summary_pdf() method


## Requirements

Python 3.12.8 was used for this project, but should be very easy to use with others python version

Packages are listed in requirements.txt


## Use

Files : 
- loan-utils_v2.py contains the class Loan
- loan-calculator.ipynb display one example of loan
- loan-summary.pdf is the PDF generated by the method generate_summary_pdf()
- loan-graph.png is the file generated by the method draw_graph()



## Sources and interesting ressources


 - [Discussion on PMT() formulas | superuser.com](https://superuser.com/questions/871404/what-would-be-the-the-mathematical-equivalent-of-this-excel-formula-pmt)
 - [Discussion on IPMT() and PPMT() formulas | superuser.com](https://superuser.com/questions/1841485/what-would-be-the-the-mathematical-equivalent-of-this-excel-formula-ppmt-and)
 - [Python Project – Loan Calculator | Python Geeks](https://pythongeeks.org/python-loan-calculator-project/)
 - [Exemple de programme en Python : calcul d’un échéancier d’emprunt |auditsi.eu](https://www.auditsi.eu/?p=12153)
 