import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ' '
    while city.strip().lower() not in ['chicago', 'new york city', 'washington'] :
        city = input('please inter one city from (chicago, new york city, washington) : \n').lower()

    filterr = input('would you like to filter the data by month ,day,both or not at all "type (none) for no time filter"... ??\n')
    
    # TO DO: get user input for month (all, january, february, ... , june)
    if filterr.strip().lower() == 'month':
        month = input("which month ?? please give us name from ('january', 'february', 'march', 'april', 'may', 'june')...\n").strip()
        days = 'all'    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    elif filterr.strip().lower() == 'day':
        month = 'all' 
        try:
            days = input('which day?? "please give us the name of the day"').strip()
        except:
            days = input('which day?? "please try again and give us the name of the day "').strip()

    elif  filterr.strip().lower() == 'both':
        month = input("which month ?? please give us name from ('january', 'february', 'march', 'april', 'may', 'june')...\n").strip()
        days = input('which day?? "please give us the name of the day"').strip() 
    else:
        month = 'all'
        days = 'all'
        
       
    print('-'*40)
    return city, month, days


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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower())+1

        # filter by month to create the new dataframe
        df = df[df.month == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'].apply(lambda x:x.lower() ) == day.lower()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].value_counts().index[0]

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].value_counts().index[0]

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].value_counts().index[0]

    print('the most common month : {} \nthe most common day of week : {} \nthe most common start hour : {}'.format(most_common_month,most_common_day,most_common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_startStation = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    most_common_endStation = df['End Station'].mode()[0]
   
    # TO DO: display most frequent combination of start station and end station trip
    df['combination_station'] = df['Start Station']+' to '+df['End Station']
    combination_station= df['combination_station'].mode()[0]

    print('most commonly used start station : {} \nmost commonly used end station : {} \nmost frequent combination of start station and end station trip : {}'.format(most_common_startStation,most_common_endStation,combination_station))    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean() 
    
    print('total travel time : {} \nmean travel time : {} '.format(total_travel_time,mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    
    print("{} : {} \n{} : {}".format(user_types.index[0],user_types[0],user_types.index[1],user_types[1]))
    # TO DO: Display counts of gender
    try :
        gender = df['Gender'].value_counts()
        print("{} : {} \n{} : {}".format(gender.index[0],gender[0],gender.index[1],gender[1]))
    except:
        print()
    
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        sortBirthYear = df['Birth Year'].sort_values()
        earliest = sortBirthYear[sortBirthYear.dropna().index[0]]
        m_recent = sortBirthYear[sortBirthYear.dropna().index[-1]]
        common = df['Birth Year'].mode()[0]
        print('earliest year : {} \nmost recent year : {} \ncommon year : {}'.format(earliest,m_recent,common))
    except:
        print()
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

        show_data = input('\nWould you like to show data? Enter yes or no.\n')
        if show_data.lower() =='yes':
            x=5
            print(df.iloc[:x,:])
            continuee = input('\nWould you like to show more? Enter yes or no.\n')
            while continuee.lower() == 'yes':
                x+=5
                print(df.iloc[x-5:x,:])
                continuee = input('\nWould you like to show more? Enter yes or no.\n')

               
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
