# 1. Name:
#      Roger Galan Manzano
# 2. Assignment Name:
#      Lab 03: Calendar
# 3. Assignment Description:
#      This program is meant to display a monthly calendar generated from user input.
# 4. What was the hardest part? Be as specific as possible.
#      The hardest part for me was displaying the calendar days in an identical fashion
#      as the assignment example. Since the lab's example is slightly indented for the 
#      day headers and the beginning of each week, I struggled with getting these to 
#      align together. Eventually I was able to use the "end" keyword within the print 
#      statement to format the display as I wanted. My initial design for the function, 
#      display_table(), contained a nested for-loop in a for-loop and it took me some
#      time to refactor the code so that it contained one for-loop for better run time 
#      efficiency. 
# 5. How long did it take for you to complete the assignment?
#      5 hours

def main():
    month = get_month()
    year = get_year()
    dow = compute_offset(year, month)
    dom = days_in_month(month, year)
    display_table(dom, dow)


def get_month():
    while True:
        month = (input("Enter a month number: "))
        try:
            month = int(month)
            if month < 1 or month > 12:
                print("Enter a value between 1 and 12.")
                continue
        except ValueError:
            print("Invalid input. Please enter a whole number between 1 and 12.")
            continue
        break

    return month

def get_year():   
    while True:
        year = input("Enter year: ")
        try:
            year = int(year)
            if year < 1753:
                print("Gregorian Calendar began after 1752. Enter a greater value.")
                continue
        except ValueError:
            print("Invalid input. Please enter a value greater than 1752.")
            continue
        break
    return year


def compute_offset(year, month):
    '''Accepts an integer, year, that is used to calculate the total number 
    of years from year to 1752 (when calendar was adopted). Calculates remainder
      and returns it as the day of the week depending on if the year was a leap year'''
    total_days = 0

    for year_count in range(1753, year):
        total_days += days_in_year(year_count)

    for month_count in range(1, month):
        total_days += days_in_month(month_count, year)
    
    return (total_days + 1) % 7


def display_table(num_days, dow):
    print("  Su  Mo  Tu  We  Th  Fr  Sa")
    print("  ", end="")
    day = 1 

    for i in range(num_days + dow):
        if i < dow:
            print("  ", end="  ")
        else:
            print(f"{day:>2}", end="  ")
            day += 1

        if i > 0 and (i + 1) % 7 == 0:
            print("\n", end="")
            print("  ", end="")
        

def days_in_month(month, year):
    months_one = [1,3,5,7,8,10,12]
    months_two = [4,6,9,11]

    if month in months_one:
        dom = 31
    elif month in months_two:    
        dom = 30
    elif month == 2:
        if is_leap_year(year):
            dom = 29
        else:
            dom = 28

    return dom


def days_in_year(year):
    if not is_leap_year(year):
        return 365
    else: 
        return 366


def is_leap_year(year):
    if year % 4 != 0:
        return False
    
    if year % 100 != 0:
        return True

    return year % 400 == 0


if __name__ == "__main__":
    main()