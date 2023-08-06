from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich import print
from pwea.ascii_art import ascii_dict
from rich.console import RenderGroup
from dataclasses import dataclass
from rich.console import Console, ConsoleOptions, RenderResult, render_group, Segment, Measurement
from rich.table import Table
import datetime

class WeatherCard:

    def __init__(self, weather_report, unit, verbosity):
        self.weather_report = weather_report
        self.unit = unit

        if weather_report['current']['is_day']:
            self.ascii_art = ascii_dict['day'][weather_report['current']
            ['condition']['text'].replace(' ', '_').lower()]
        else:
            self.ascii_art = ascii_dict['night'][weather_report['current']
            ['condition']['text'].replace(' ', '_').lower()]

        self.location_header = (
            f"{weather_report['location']['name']}, "
            f"{weather_report['location']['region']}, "
            f"{weather_report['location']['country']}"
        )

        self.time_header = (
            f"The current time is "
            f"{weather_report['location']['localtime']}"
        )

        self.last_updated_header = (
            f"Weather report "
            f"(last updated at {weather_report['current']['last_updated']})"
        )

        self.conditions = f"{weather_report['current']['condition']['text']}"
        self.humidity = f"{weather_report['current']['humidity']}%"
        self.uv_index = f"{weather_report['current']['uv']}"
        self.wind_dir = f"{weather_report['current']['wind_dir']}"
        self.wind_degree = f"{weather_report['current']['wind_degree']}"

        if self.unit == 'metric':

            self.temperature_header = (
                f"{weather_report['current']['temp_c']}°C "
                f"({weather_report['current']['feelslike_c']}°F)"
            )

            self.wind_speed = f"{weather_report['current']['wind_kph']}"
            self.pressure = f"{weather_report['current']['pressure_mb']}mb"

        else:
            self.temperature_header = (
                f"{weather_report['current']['temp_f']}°F "
                f"({weather_report['current']['feelslike_f']}°F)"
            )

            self.wind_speed = f"{weather_report['current']['wind_mph']}"
            self.pressure = f"{weather_report['current']['pressure_in']}in"

        # All self attributes in __init__ below this comment are currently
        # unused. To be used in future versions where verbosity level arguments
        # actually do something.

        self.lat_long = (
            f"{weather_report['location'],['lat']},"
            f"{weather_report['location'],['lon']},"
        )

        self.timezone = f"{weather_report['location']['tz_id']}"

        self.cloud = f"{weather_report['current']['cloud']}"
        self.air_quality = weather_report['current']['air_quality']

        if self.unit == 'metric':
            self.precip = f"{weather_report['current']['precip_mm']}"
            self.visibility = f"{weather_report['current']['vis_km']}"
            self.wind_gusts = f"{weather_report['current']['gust_kph']}"

        else:
            self.precip = f"{weather_report['current']['precip_in']}"
            self.visibility = f"{weather_report['current']['vis_miles']}"
            self.wind_gusts = f"{weather_report['current']['gust_mph']}"

        def format_weathercard():
            renderables = (
                f"[underline bold][#5fd7d7]"
                f"{self.location_header}\n"
                f"[/underline bold]"
                f"{self.time_header}\n\n"
                f"{self.last_updated_header}\n\n"
                f"[/#5fd7d7]"
                f"{self.ascii_art}\n\n"
                f"[indian_red]"
                f"{self.temperature_header}, {self.conditions}\n"
                f"Humidity: {self.humidity}\tPressure: {self.pressure}\n"
                f"UV Index: {self.uv_index}\n"
                f"Current wind speed is {self.wind_speed} to the {self.wind_dir} " \
                f"({self.wind_degree} degrees)."
                f"[indian_red]"
            )

            return renderables

        self.renderables = format_weathercard()

        return None

    def __rich_console__(self, console: Console,
                         options: ConsoleOptions) -> RenderResult:
        yield Panel(self.renderables, expand=False)

class DailyForecastCard:

    def __init__(self, weather_report, unit, verbosity):
        self.days = 1

        self.location_header = (
            f"{weather_report['location']['name']}, "
            f"{weather_report['location']['region']}, "
            f"{weather_report['location']['country']}"
        )

        self.lat_long = (
            f"{weather_report['location'],['lat']},"
            f"{weather_report['location'],['lon']},"
        )

        self.date = f"{weather_report['forecastday']['date']}"
        self.timezone = f"{weather_report['location']['tz_id']}"

        self.humidity = f"{weather_report['forecastday']['day']['avghumidity']}"

        print(weather_report)


    @render_group()
    def get_panels_iterable(iterable):
        for i in iterable:
            yield Panel(i, style="on blue")

    def __rich_console__(self, console: Console,
                         options: ConsoleOptions) -> RenderResult:

        my_table = Table("Attribute", "Value")
        my_table.add_row(self.display_text_metric, self.display_text_metric,
                         self.display_text_metric)
        yield my_table
