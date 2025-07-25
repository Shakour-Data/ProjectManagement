import datetime
import jdatetime

def get_dates():
    # Get current Gregorian date
    gregorian_date = datetime.date.today()
    gregorian_str = gregorian_date.strftime("%Y-%m-%d")

    # Convert to Jalali (Persian) date
    jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)
    jalali_str = jalali_date.strftime("%Y-%m-%d")

    return gregorian_str, jalali_str

if __name__ == "__main__":
    gregorian, jalali = get_dates()
    print(f"Gregorian date: {gregorian}")
    print(f"Jalali date: {jalali}")
