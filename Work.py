import time
import pandas as pd
import numpy as np
import datetime
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DIC = {'1': 'January', '2': 'February', '3': 'March','4': 'April', '5': 'May', '6': 'June'}
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #print('Please choose a city to analyze: chicago, new york city or washington')
    #print('Now, please choose a month (january, february...) or type "All" if you want the whole year')
    #print('Last thing =), please select a day of the week: monday, tuesday... or "All" to see the data from the whole week')
    #return ('The city is: {}, the month  is: {} and the day is {}'.format(city, month, day))
    city = ''
    month = ''
    day = ''
    while True:
        city = input('Please choose a city to analyze: chicago, new york city or washington: ').lower().strip()
        if city in ('chicago','new york city','washington'):
            break
        else:
            print('There must be a typo, try again')
            continue

    while True:
        month = input('Now, please choose a month (january, february...) or type "All" if you want the whole year: ').lower().strip()
        if month in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            break
        else:
            print('There must be a typo, try again')
            continue
    while True:
        day = input('Last thing =), please select a day of the week: monday, tuesday... or "All" to see the data from the whole week: ').lower().strip()
        if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            break
        else:
            print('There must be a typo, try again')
            continue   
    # get user input for city (chicago, new york city, washington).

    # get user input for month (all, january, february, ... , june)


    # get user input for day of week (all, monday, tuesday, ... sunday)


    print('-'*40)
    return city, month, day
#print(get_filters())

"""HASTA AQUÍ VAMOS BIEN"""



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
    df = pd.read_csv("/Users/braul/OneDrive/Escritorio/Udacity/Python/{}".format(CITY_DATA[city]))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['common station'] = df[['Start Station', 'End Station']].apply(' - '.join, axis = 1)
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    
    #Displays statistics on the most frequent times of travel.
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    most_common_month = str(df['month'].mode()[0])
    print('The most common month is: {}'.format(MONTH_DIC[most_common_month]))
    
    # display the most common day of week
    most_common_day = str(df['day_of_week'].mode()[0])
    print('The most common day is: {}'.format(most_common_day))
    # display the most common start hour
    most_common_hour = str(df['hour'].mode()[0])
    print('The most common hour is: {}:00'.format(most_common_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    #Displays statistics on the total and average trip duration.

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = str(datetime.timedelta(0,int((df['Trip Duration'].sum()))))
    travel_time_sec = df['Trip Duration'].sum()
    print('The total travel time is: {} seconds or {}'.format(travel_time_sec, travel_time))

    # display mean travel time
    travel_avg= round((int(df['Trip Duration'].mean())),0)
    print('On average, a trip lasts {} seconds'.format(travel_avg))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts(dropna=True)
    print('Number of customers by user type category: ')
    print(user_types)

    # Display counts of gender
    try:
        gender_type = df['Gender'].value_counts(dropna=True)
        print('\nNumber of customers by gender: ')
        print(gender_type)
    except KeyError:
        print('\n Sorry, This city has no gender data :(')
    

    # Display earliest, most recent, and most common year of birth
    try:
        print('\nThe earliest (amin), most recent (amax) and most common year (mean) of birth of our customers: \n')
        birth = round(df['Birth Year'].agg([np.min, np.max, np.mean]),0)
        print(birth)
    except KeyError:
        print('\n Sorry, This city has no birth data :(')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most commonly start station is: {}'.format(start_station))

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('\nThe most commonly end station is: {}'.format(end_station))
    # display most frequent combination of start station and end station trip
    combination_stations = df['common station'].mode()[0]
    print('\nThe most frequent combination of start station and end station trip is: {}'.format(combination_stations))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    raw_counter = 0
    raw = input('Would you like to watch the first five rows of the data? type yes, if you don´t want type no: ').lower().strip()
    if raw == 'yes':
        print(df.head())
        raw_counter += 5
        while True:
            next_raw = input('Wanna see 5 more? then type yes, else type no: ').lower().strip()
            if next_raw == 'yes':
                print(df.iloc[raw_counter:raw_counter + 5:])
                raw_counter += 5
            else: 
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
