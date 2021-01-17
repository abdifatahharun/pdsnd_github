import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
            city = input('What city would you like to see data from?? Chicago, New York City, or Washington? \n').title()
            if city not in CITY_DATA:
                print('\n oop..... invalid city name, please try again!\n')
                continue
            else:
                print()
            break

    # get user input for days of th week and month (all, january, february, ... , june)
    MONTH_LIST = ['January', 'February', 'March', 'April', 'May', 'June']
    DAY_LIST =  ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    while True:
        filter_by = input('Would you like to filter the data by month, day, or not at all? typ "none" for no time filter. \n').lower()
        print()
        if filter_by == 'month':
            month = input('Which month? January, February, March, April, May, or June \n').title()
            if month not in MONTH_LIST:
                print('\n oop..... invalid input, please try again!\n')
                continue
            else:
                print()
                day = 'All'
                break

        elif filter_by == 'day':
            day = input('Which day? Please type day as: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday \n').title()
            if day not in DAY_LIST:
                print('\n oop..... invalid input, please try again!  \n')
                continue
            else:
                print()
                month = 'All'
                break
        elif filter_by == 'none':
                month = 'All'
                day = 'All'
                break
        else:
            print('\n oop..... invalid input, please try again!')
            continue


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'] )

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour']= df['Start Time'].dt.hour



    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        df = df[df['month'] == month]
    if day != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('\nWhat is the most popular month for traveling?')
    print(df['Start Time'].dt.month_name().mode()[0])

    # display the most common day of week
    print('\nWhat is the most popular day of the week for traveling?')
    print(df['Start Time'].dt.day_name().mode()[0])

    # display the most common start hour
    print('\nWhat is the most popular hour of the day to start your travels?')
    print(df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nWhat is the most popular start station?')
    print(df['Start Station'].mode()[0])

    # display most commonly used end station
    print('\nWhat is the most popular end station?')
    print(df['End Station'].mode()[0])


    # display most frequent combination of start station and end station trip
    print('\nWhat is the most common start and end station combination?\n')
    df['combo_station'] = df['Start Station'] + " / " + df['End Station']
    print('The most frequent combination of start station and end station respectively is:\n {}'.format(df['combo_station'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['travel'] = df['End Time'] - df['Start Time']
    print('The total travel time was {}\n'.format(df['travel'].sum()))


    # display mean travel time
    print('The average travel time was {}'.format(df['travel'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\n What is the breakdown of users?')
    print(df['User Type'].value_counts())

    # Display counts of gender
    print('\nWhat is the breakdown of gender?')
    try:
        print(df['Gender'].value_counts())
        print()
    except Exception as e:
        print('System couldn\'t calculate the break down of users as there is no {} data to share'.format(e))



    # Display earliest, most recent, and most common year of birth
    print('\nWhat is earliest, most recent, and most common year of birth?')
    if 'Birth Year' not in df.columns:
        print('\nNo birth year data to share.\n')
    else:
        print('\nThe oldest year of birth is {}, \nthe youngest year of birth is {}, \nand the popular or most common year of birth is {}'.format(df['Birth Year'].min(), df['Birth Year'].max(),  df['Birth Year'].mode()[0]))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """ Display 5 lines raw data as requested by the user."""

    display_raw_input = input('\nWould you like to view 5 rows of individual trip raw data? Enter yes or no\n').lower()
    start_loc = 0
    while display_raw_input .lower() == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_display = input('Do you wish to continue?:Enter yes or no.\n' ).lower()
        if view_display.lower() != 'yes':
            break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
