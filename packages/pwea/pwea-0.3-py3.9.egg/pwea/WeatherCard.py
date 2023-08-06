from pwea.ascii_art import ascii_dict

from rich.console import Console, ConsoleOptions, RenderResult
from rich.panel import Panel
from rich.table import Table

from datetime import date, timedelta

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

        pattern = 'United States of America'
        self.location_header = (
            f"{weather_report['location']['name']}, "
            f"{weather_report['location']['region']}, "
            f"{weather_report['location']['country'].replace(pattern, 'USA')}"
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

        def format():
            renderables = (
                f"[underline bold]"
                f"{self.location_header}\n"
                f"[/underline bold]"
                f"{self.time_header}\n\n"
                f"{self.last_updated_header}\n\n"
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

        self.renderables = format()

        return None

    def __rich_console__(self, console: Console,
                         options: ConsoleOptions) -> RenderResult:
        yield Panel(self.renderables, expand=False)

class DailyForecastCard:

    def __init__(self, weather_report, unit, days, verbosity):

        def format():
            renderables = (
                f"{self.location_header}\n"
                f"{self.localtime}.\n\n"
                f"{self.conditions}."
                f"\n\n"
                f"{self.ascii_art}\n\n"
                f"[indian_red]"
                f"High: "
                f"{self.max_temp} "
                f"Low: "
                f"{self.min_temp}.\n"
                f"Average: {self.avg_temp}\n"
                f"Humidity: {self.humidity}\n"
                f"UV Index: {self.uv}\n"
                f"Wind speed: {self.max_wind}\n"
                f"Visibility: {self.avg_vis}"
            )

            return renderables

        self.days = int(days)
        self.renderables = {}

        for day in range(self.days):
            self.ascii_art = (
                ascii_dict['day'][weather_report['forecast']['forecastday'][day]
                                ['day']['condition']
                                ['text'].replace(' ', '_').lower()]
            )

            pattern = "United States of America"
            self.location_header = (
                f"{weather_report['location']['name']}, "
                f"{weather_report['location']['region']}, "
                f"{weather_report['location']['country'].replace(pattern, 'USA')}"
            )

            self.lat_long = (
                f"{weather_report['location'],['lat']},"
                f"{weather_report['location'],['lon']},"
            )

            self.localtime = (
                f"{weather_report['location']['localtime']}"
            )

            self.date = f"{weather_report['forecast']['forecastday'][day]['date']}"
            self.timezone = f"{weather_report['location']['tz_id']}"

            self.conditions = (
                f"{weather_report['forecast']['forecastday'][day]['day']['condition']['text']}"
            )

            self.humidity = (
                f"{weather_report['forecast']['forecastday'][day]['day']['avghumidity']}"
            )

            self.uv = (
                f"{weather_report['forecast']['forecastday'][day]['day']['uv']}"
            )

            self.sunrise = (
                f"{weather_report['forecast']['forecastday'][day]['astro']['sunrise']}"
            )

            self.sunset = (
                f"{weather_report['forecast']['forecastday'][day]['astro']['sunset']}"
            )

            self.moonrise = (
                f"{weather_report['forecast']['forecastday'][day]['astro']['moonrise']}"
            )

            self.moonset = (
                f"{weather_report['forecast']['forecastday'][day]['astro']['moonset']}"
            )

            self.moon_phase = (
                f"{weather_report['forecast']['forecastday'][day]['astro']['moon_phase']}"
            )

            self.moon_illumination = (
                f"{weather_report['forecast']['forecastday'][day]['astro']['moon_illumination']}"
            )

            if weather_report['forecast']['forecastday'][day]['day']['daily_will_it_rain']:
                self.rain_percent = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['daily_chance_of_rain']}"
                )

            if weather_report['forecast']['forecastday'][day]['day']['daily_will_it_snow']:
                self.rain_percent = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['daily_chance_of_snow']}"
                )


            if unit == 'metric':
                self.max_temp = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['maxtemp_c']}°C"
                )
                self.min_temp = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['mintemp_c']}°C"
                )
                self.avg_temp = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['avgtemp_c']}°C"
                )
                self.max_wind = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['maxwind_kph']}kph"
                )
                self.total_precip = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['totalprecip_mm']}mm"
                )
                self.avg_vis = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['avgvis_km']}km"
                )

            else:
                self.max_temp = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['maxtemp_f']}°F"
                )
                self.min_temp = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['mintemp_f']}°F"
                )
                self.avg_temp = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['avgtemp_f']}°F"
                )
                self.max_wind = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['maxwind_mph']}mph"
                )
                self.total_precip = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['totalprecip_in']}in"
                )
                self.avg_vis = (
                    f"{weather_report['forecast']['forecastday'][day]['day']['avgvis_miles']}miles"
                )

            self.renderables[day] = format()

    def __rich_console__(self, console: Console,
                         options: ConsoleOptions) -> RenderResult:
        renderable_table = Table()

        for day in range(self.days):
            renderable_table.add_column(str(date.today() + timedelta(day)))

        renderable_table.add_row(*self.renderables.values())
        yield renderable_table
