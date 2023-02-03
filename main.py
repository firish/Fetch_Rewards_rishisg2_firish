"""
Fetch Rewards Backend Software Engineering Internship Take-Home Test. 
"""

# Imports
import sys
import argparse
import pandas as pd
from collections import defaultdict


__author__ = "Rishi Gulati"
__email__ = "rishisg2@illinois.edu"
__challengeUrl__ = "https://docs.google.com/document/d/1Yn_xAonwLOINma3MquU5ag6KoNMkrH3uA-99pJvqaWs/edit"
__solutionUrl__ = ""
__version__ = "0.1.0"
__license__ = "MIT"



def load_data(name):
    # function to load data, given name
    # name var actually contains the entire relative path 
    df = pd.read_csv(name)

    # Exception handling 1, keep only the necessary columns
    columns_to_keep = ['payer', 'points', 'timestamp']
    df = df.drop(columns=[col for col in df.columns if col not in columns_to_keep])

    # Exception handling 2, handle for any inconsistent/un-itelligible data
    try:
        df['points'] = pd.to_numeric(df['points'], errors='coerce').astype(int)
    except Exception as err:
        print('Exception while reading values ::: ' + 'IntConversionError ::: ' + str(err))
        sys.exit()

    return df



def preprocess_date(df):
    # This function converts the date to a proper and easily usable format
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%dT%H:%M:%SZ')
    
    # Extract time, day, month, and year
    try:
        # ts stands for timestamp
        df['time'] = df['timestamp'].dt.time
        df['day'] = df['timestamp'].dt.day
        df['month'] = df['timestamp'].dt.month
        df['year'] = df['timestamp'].dt.year

        # At this time, we can now drop the timestap attribute to save memory
        df = df.drop(columns=['timestamp'])
    except Exception as err:
        print('Exception while converting values ::: ' + 'DateTimeError ::: ' + str(err))
        sys.exit()
    
    return df


def detect_nulls(df):
    try:
        if df.isnull().values.any():
            raise ValueError("Data contains NaN/Null/None values")
    except ValueError as ve:
        print('Exception while parsing values ::: ' + 'NullValueError ::: ' + str(ve))
        sys.exit()


def initialize_data(df):
    # Exception handling, I use a sum variable that keeps track of the total sum
    # if the points to be used are greater than the sum, an error should be raised
    total_points = df['points'].sum()
    
    # Create a queue to make sure that elements are accessed in the order they are entered
    # Enter elements in ascending order by time
    # (suggestion) At a later point, if we want to add and subract points in the same program, we should a priority heap.
    df = df.sort_values(by=['year', 'month', 'day', 'time'])
    pipeline = df.values.tolist()

    # Make a hashmap with point balance of each payer
    balances = defaultdict(int)
    for transaction in pipeline:
        balances[transaction[0]] += transaction[1]
    
    return (total_points, pipeline, balances)


def get_answer(total_points, pipeline, balances, points_to_spend):
    if points_to_spend > total_points:
        print('Exception in passed parameter ::: WrongParameterError ::: The user does not have ' + str(points_to_spend) + ' in their account.')
        sys.exit()
    elif points_to_spend <= 0:
        print('Exception in passed parameter ::: WrongParameterError ::: Please input a positive, non-zero integer')
        sys.exit()

    for transaction in pipeline:
        # print(total_points, balances)
        if points_to_spend == 0:
            break

        payer, points = transaction[0], transaction[1]
        if points <= points_to_spend:
            balances[payer] -= points
            points_to_spend -= points
        else:
            balances[payer] -= points_to_spend
            points_to_spend = 0

    return balances



def main():
    """ Main entry point of the script """

    # load the points to be spent parameter 
    # handle the exception when no value or a value in wrong format is inputed
    parser = argparse.ArgumentParser(description='This program takes one command line argument')
    parser.add_argument('value', type=int, help='An integer value')
    points_to_spend = parser.parse_args().value

    df = load_data('transactions.csv')
    detect_nulls(df)

    df = preprocess_date(df)
    total_points, pipeline, balances = initialize_data(df)
    res = get_answer(total_points, pipeline, balances, points_to_spend)
    
    # print the output
    print(dict(res))


if __name__ == "__main__":
    main()