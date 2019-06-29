import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
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
    print('Plese let us know for which city, month and day you want to see data for.')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Choose city: Chicago, New York or Washington?\n')
        if city not in ('New York', 'Chicago', 'Washington'):
            print("Wrong input! Please try again.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Choose month: January, February, March, April, May, June or \"all\" to apply no filter:\n")
        if month not in ('January', 'February', 'March', 'April', 'May', 'June', 'all'):
            print("Wrong input! Please try again.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Choose day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or \"all\" to apply no filter:\n")
        if day not in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'all'):
            print("Wrong input! Please try again.")
            continue
        else:
            break

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month.lower()
    df['day_of_week'] = df['Start Time'].dt.weekday_name.lower()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
         # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("Most popular month:", popular_month)

    # display the most common day of week

    popular_dow = df['day_of_week'].mode()[0]
    print("Most popular day of week:", popular_dow)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("Most popular hour:", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("Most popular start station:", popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("Most popular end station:", popular_end)

    # display most frequent combination of start station and end station trip
    df["Popular Station"] = df['Start Station'].astype(str).str.cat(df['End Station'].astype(str), sep=' & ')
    popular_comb = df["Popular Station"].mode()[0]
    print("Most popular combination of start and end station:", popular_comb)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_sum = df['Trip Duration'].sum(axis=0)
    print("Total travel time: ", travel_sum)

    # display mean travel time
    travel_mean = df['Trip Duration'].mean(axis=0)
    print("Mean travel time: ", travel_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_types = df['User Type'].value_counts()
        print("User type count:\n", user_types)
    except KeyError:
        print("User Types:\nNo data available for this month.")

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("\nGender count:\n", gender)
    except KeyError:
        print("\nGender Types:\nNo data available for this month.")

    # Display earliest, most recent, and most common year of birth
    try:
        print("\nEarliest year of birth: ", df['Birth Year'].min(axis=0))
    except KeyError:
        print("\nEarliest year of birth:\nNo data available for this month.")

    try:
        print("\nMost recent year of birth: ", df['Birth Year'].max(axis=0))
    except KeyError:
        print("\nMost recent year of birth:\nNo data available for this month.")

    try:
        print("\nMost common year of birth: ", df['Birth Year'].mode()[0])
    except KeyError:
        print("\nMost common year of birth:\nNo data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
