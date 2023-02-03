# To run the file, 
1) download the main.py file
2) keep the transactions.csv file in the same location
3) run the program as python main.py int_val 
(int_vl represents any integer value)
4) The answer is printed on the console
5) Note: Edge cases, wrong inputs, and undesired behaviors are handled by rasining exceptions


# Rough overview
This script is used to load and process transactions data from a CSV file and calculate the remaining point balance for each payer after spending a certain amount of points. The data is loaded and processed in the following steps:

1) Load data from the CSV file using Pandas.
2) Keep only the necessary columns.
3) Handle inconsistent/un-intelligible data by converting the points to integer type.
4) Convert the date to a proper and easily usable format.
5) Check for any NaN/null values.
6) Initialize the data by summing up the points, sorting the transactions by date, and storing the point balances in a hashmap.
7) Calculate the remaining point balances for each payer after spending the specified amount of points.

Input: The script takes one command-line argument, an integer representing the amount of points to be spent. 
Output: The program then returns the point balance for each payer after spending the specified points.