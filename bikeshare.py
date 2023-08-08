import time
import pandas as pd
import numpy as np


CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington).
    while True:
        city = input('Choose city name chicago, new york city or washington: ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid city name, please try again.')

    # Get user input for month (all, january, february, ..., june).
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('Enter month name (all, january,february,march,april,may,june): ').lower()
        if month in months:
            break
        else:
            print('Invalid month name, please try again.')

    # Get user input for day of the week (all, monday, tuesday, ..., sunday).
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('Enter day of the week (all,monday,tuesday,wednesday,thursday,friday,saturday,sunday): ').lower()
        if day in days:
            break
        else:
            print('Invalid day name, please try again.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load the CSV file into a Pandas DataFrame.
    df = pd.read_csv(CITY_DATA[city])

    # Convert the 'Start Time' column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of the week from the 'Start Time' column.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # Filter by month if applicable.
    if month != 'all':
        month_number = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month_number]

    # Filter by day of the week if applicable.
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month.
    most_popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('Most common month of the year is:', months[most_popular_month - 1])

    # Display the most common day of the week.
    most_popular_day = df['day_of_week'].mode()[0]
    print('Most common day of the week: is', most_popular_day.capitalize())

    # Display the most common start hour.
    df['hour'] = df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()[0]
    print('Most common start hour of the day is:', most_popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display the most commonly used start station.
    popular_start_station = df['Start Station'].mode()[0]
    print('Most common start station:', popular_start_station)

    # Display the most commonly used end station.
    most_popular_end_station = df['End Station'].mode()[0]
    print('Most common end station:', most_popular_end_station)

    # Display the most frequent combination of start station and end station trip.
    most_popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most common trip:', most_popular_trip[0], 'to', most_popular_trip[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time.
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time, 'seconds')

    # Display mean travel time.
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    user_types = df['User Type'].value_counts()
    print('Below are the counts of user types:\n', user_types)

    # Display counts of gender.
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nBelow are the counts of gender:\n', gender_counts)
    else:
        print('\nGender data not available for the specified city.')

    # Display earliest, most recent, and most common year of birth.
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        print('\nEarliest birth year:', int(earliest_birth_year))
        
        most_recent_birth_year = df['Birth Year'].max()
        print('Most recent birth year:', int(most_recent_birth_year))
        
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('Most common birth year:', int(most_common_birth_year))
    else:
        print('\nBirth Year data not available for the specified city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Displays 5 lines of raw data from the DataFrame at a time.
    Asks the user if they want to see more, and continues displaying the next 5 lines until the user says 'no'.
    """
    index = 0
    while True:
        raw_data = df.iloc[index:index + 5]
        print('\nDisplaying 5 lines of raw data:\n', raw_data)

        if index + 5 >= len(df):
            print("\nNo more raw data to display.")
            break

        show_more = input('\nWould you like to see more raw data? Enter "yes" or "no": ')
        if show_more.lower() != 'yes':
            break

        index += 5
        
def main():
    while True:
        # Get user-selected city, month, and day filters
        city, month, day = get_filters()
        
        # Load data based on the selected filters
        df = load_data(city, month, day)
		
		# Display time-related statistics
        time_stats(df)
        
		# Display station-related statistics
		station_stats(df)
		
		# Display trip duration-related statistics
        trip_duration_stats(df)
		
		# Display user-related statistics
        user_stats(df)
        
        show_data = input('\nWould you like to see raw data? Enter "yes" or "no": ')
        if show_data.lower() = 'yes':
            display_raw_data(df)
             

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()