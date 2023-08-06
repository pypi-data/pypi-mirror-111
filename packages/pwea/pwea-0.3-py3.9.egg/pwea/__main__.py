import requests
import argparse

from rich import print
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel

from pwea.key import KEY
from pwea.Card import WeatherCard, DailyForecastCard


def get_weather(report_type, location, days):
    base_url = f'https://api.weatherapi.com/v1'
    if report_type == 'current':
        weather_report = requests.get(f"{base_url}/{report_type}.json?"
                                      f"key={KEY}&q={location}&aqi=yes")
    elif report_type == 'forecast':
        weather_report = requests.get(f"{base_url}/{report_type}.json?"
                                      f"key={KEY}&q={location}"
                                      f"&days={str(days)}&aqi=yes")
    return weather_report


def main():
    parser = argparse.ArgumentParser(
        usage='pwea [location]',
        description="description: pwea is a simple tool used to retrieve"
        "current weather weather_reportrmation")

    parser.add_argument('location', nargs='+',
                        help="Input a city name, US/UK/Canadian postal code,"
                        "IP address, or Latitude / Longitude (in decimal"
                        "degree)")
    parser.add_argument("-t" "--type", dest="report_type", default="current",
                        help="Valid report types are 'current' or 'forecast'")
    parser.add_argument("-d" "--days", dest="days", default="3",
                        help=(
                            f"Number of days to forecast. Default 3. Max 3 "
                            f"when using free API key"
                        ))
    parser.add_argument("-u", "--unit", dest="unit", default="metric")
    parser.add_argument("-v", "--verbosity", dest="verbosity",
                        action="count", default=2,
                        help="Feature not yet added")

    args = parser.parse_args()

    location = ' '.join(args.location)
    args.report_type = args.report_type.lower()
    args.unit = args.unit.lower()

    if args.report_type == 'current':
        weather_report = get_weather(args.report_type, location,
                                     days=None).json()
        print(WeatherCard(weather_report, args.unit, args.verbosity))

    elif args.report_type == 'forecast':
        weather_report = get_weather(args.report_type, location,
                                     args.days).json()

        print(DailyForecastCard(weather_report, args.unit, args.days,
                                args.verbosity))

    else:
        print(f"Invalid report type. See 'pwea -h' for more information")


if __name__ == '__main__':
    main()
