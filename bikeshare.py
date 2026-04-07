"""
Bikeshare Analysis Script
- Asks the user for filters (city, month, day)
- Loads the selected CSV into a pandas DataFrame
- Computes common statistics (time, stations, trip duration, user stats)

Note:
This script expects CSV files to be present in the same folder:
- chicago.csv
- new_york_city.csv
- washington.csv
"""

import time
import pandas as pd

# --- Constants (easy to maintain, avoids "magic strings") ---
CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}

MONTHS = ["all", "january", "february", "march", "april", "may", "june"]
DAYS = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


# --- Helper Functions (refactoring: reuse, readability) ---
def _normalize(text: str) -> str:
    """Normalize user input to a comparable format."""
    return text.strip().lower()


def _prompt_choice(prompt: str, valid_options: list[str]) -> str:
    """
    Prompt the user until they provide a valid choice.

    Args:
        prompt: Prompt string for input()
        valid_options: List of allowed values (already normalized)

    Returns:
        A valid normalized choice string.
    """
    valid_set = set(valid_options)
    while True:
        value = _normalize(input(prompt))
        if value in valid_set:
            return value
        print(f"Invalid input. Please choose one of: {', '.join(valid_options)}")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city  - name of the city to analyze
        (str) month - month to filter by, or "all"
        (str) day   - day of week to filter by, or "all"
    """
    print("Hello! Let's explore some US bikeshare data!")

    # Get user input with validation (no duplicated while loops)
    city = _prompt_choice(
        "Which city? (chicago, new york city, washington)\n> ",
        list(CITY_DATA.keys()),
    )

    month = _prompt_choice(
        "Which month? (all, january, february, march, april, may, june)\n> ",
        MONTHS,
    )

    day = _prompt_choice(
        "Which day? (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)\n> ",
        DAYS,
    )

    print("-" * 40)
    return city, month, day


def load_data(city: str, month: str, day: str) -> pd.DataFrame:
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city: city name (normalized)
        month: month name (normalized) or "all"
        day: day name (normalized) or "all"

    Returns:
        Filtered DataFrame.
    """
    # Load CSV for selected city
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    # Convert "Start Time" to datetime once (important for dt access)
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Create derived columns (refactoring-friendly: computed once, reused)
    df["month"] = df["Start Time"].dt.month          # 1..12
    df["day_name"] = df["Start Time"].dt.day_name()  # e.g., "Monday"
    df["hour"] = df["Start Time"].dt.hour

    # Filter by month if needed
    if month != "all":
        month_index = MONTHS.index(month)  # january -> 1, ... june -> 6
        df = df[df["month"] == month_index]

    # Filter by day if needed
    if day != "all":
        # Day names in pandas are capitalized ("Monday"), so normalize comparison
        df = df[df["day_name"].str.lower() == day]

    return df


def _print_time(label: str, fn, *args, **kwargs):
    """
    Small helper to measure runtime of a statistics function.
    (This is a refactoring trick to avoid duplicating timing code.)
    """
    print(f"\nCalculating {label}...\n")
    start_time = time.time()
    fn(*args, **kwargs)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def time_stats(df: pd.DataFrame):
    """Displays statistics on the most frequent times of travel."""

    # Most common month (only if data not empty)
    if df.empty:
        print("No data available for the selected filters.")
        return

    common_month_num = int(df["month"].mode()[0])  # number 1..12
    # Convert number back to name (we only list Jan-Jun in this project)
    common_month_name = MONTHS[common_month_num] if 0 <= common_month_num < len(MONTHS) else str(common_month_num)
    print(f"Most common month: {common_month_name.title()}")

    # Most common day of week
    common_day = df["day_name"].mode()[0]
    print(f"Most common day of week: {common_day}")

    # Most common start hour
    common_hour = int(df["hour"].mode()[0])
    print(f"Most common start hour: {common_hour}:00")


def station_stats(df: pd.DataFrame):
    """Displays statistics on the most popular stations and trip."""
    if df.empty:
        print("No data available for the selected filters.")
        return

    # Most commonly used start station
    start_station = df["Start Station"].mode()[0]
    print(f"Most commonly used start station: {start_station}")

    # Most commonly used end station
    end_station = df["End Station"].mode()[0]
    print(f"Most commonly used end station: {end_station}")

    # Most frequent combination of start station and end station
    trip_combo = (df["Start Station"] + " -> " + df["End Station"]).mode()[0]
    print(f"Most frequent trip: {trip_combo}")


def trip_duration_stats(df: pd.DataFrame):
    """Displays statistics on the total and average trip duration."""
    if df.empty:
        print("No data available for the selected filters.")
        return

    # Total travel time
    total_time = df["Trip Duration"].sum()
    print(f"Total travel time (seconds): {total_time:,}")

    # Mean travel time
    mean_time = df["Trip Duration"].mean()
    print(f"Mean travel time (seconds): {mean_time:,.2f}")


def user_stats(df: pd.DataFrame):
    """Displays statistics on bikeshare users."""
    if df.empty:
        print("No data available for the selected filters.")
        return

    # Display counts of user types
    if "User Type" in df.columns:
        print("\nCounts of user types:")
        print(df["User Type"].value_counts())
    else:
        print("\nUser Type column not available in this dataset.")

    # Display counts of gender (may not exist in Washington dataset)
    if "Gender" in df.columns:
        print("\nCounts of gender:")
        print(df["Gender"].value_counts(dropna=False))
    else:
        print("\nGender column not available in this dataset.")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        birth_years = df["Birth Year"].dropna()
        if not birth_years.empty:
            earliest = int(birth_years.min())
            most_recent = int(birth_years.max())
            most_common = int(birth_years.mode()[0])

            print("\nBirth year stats:")
            print(f"Earliest: {earliest}")
            print(f"Most recent: {most_recent}")
            print(f"Most common: {most_common}")
        else:
            print("\nBirth Year column exists but contains no valid values.")
    else:
        print("\nBirth Year column not available in this dataset.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Timing wrapper reduces duplication (nice refactor)
        _timed_print("The Most Frequent Times of Travel", time_stats, df)
        _timed_print("The Most Popular Stations and Trip", station_stats, df)
        _timed_print("Trip Duration", trip_duration_stats, df)
        _timed_print("User Stats", user_stats, df)

        restart = input("\nWould you like to restart? Enter yes or no.\n> ")
        if _normalize(restart) != "yes":
            break


if __name__ == "__main__":
    main()