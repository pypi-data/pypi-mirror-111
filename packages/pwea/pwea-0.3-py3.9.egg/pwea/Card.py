from pwea.ascii_art import ascii_dict

from rich.console import Console, ConsoleOptions, RenderResult
from rich.panel import Panel
from rich.table import Table

from datetime import date, timedelta


class WeatherCard:

    def __init__(self, weather_report, unit, verbosity):

        def format():
            renderables = (
                f"{self.location_header}\n"
                f"{self.time_header}\n\n"
                f"{self.last_updated_header}\n\n"
                f"{self.ascii_art}\n\n"
                f"[indian_red]"
                f"{self.temperature_header}, {self.conditions}\n"
                f"Humidity: {self.humidity}\tPressure: {self.pressure}\n"
                f"UV Index: {self.uv_index}\n"
                f"Current wind speed is {self.wind_speed} to the "
                f"{self.wind_dir} "
                f"({self.wind_degree} degrees)."
                f"[indian_red]"
            )

            return renderables

        self.weather_report = weather_report
        self.unit = unit

        if weather_report['current']['is_day']:
            self.ascii_art = ascii_dict['day'][weather_report['current']
                                               ['condition']
                                               ['text'].replace
                                               (' ', '_').lower()]

        else:
            self.ascii_art = ascii_dict['night'][weather_report['current']
                                                 ['condition']
                                                 ['text'].replace
                                                 (' ', '_').lower()]

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
                f"({weather_report['current']['feelslike_c']}°C)"
            )
            self.wind_speed = f"{weather_report['current']['wind_kph']} kph"
            self.pressure = f"{weather_report['current']['pressure_mb']} mb"
            self.precip = f"{weather_report['current']['precip_mm']} mm"
            self.visibility = f"{weather_report['current']['vis_km']} km"
            self.wind_gusts = f"{weather_report['current']['gust_kph']}"

        else:
            self.temperature_header = (
                f"{weather_report['current']['temp_f']}°F "
                f"({weather_report['current']['feelslike_f']}°F)"
            )
            self.wind_speed = f"{weather_report['current']['wind_mph']} mph"
            self.pressure = f"{weather_report['current']['pressure_in']} in"
            self.precip = f"{weather_report['current']['precip_in']}"
            self.visibility = f"{weather_report['current']['vis_miles']}"
            self.wind_gusts = f"{weather_report['current']['gust_mph']}"

        self.lat_long = (
            f"{weather_report['location'],['lat']},"
            f"{weather_report['location'],['lon']},"
        )

        self.timezone = f"{weather_report['location']['tz_id']}"
        self.cloud = f"{weather_report['current']['cloud']}"
        self.air_quality = weather_report['current']['air_quality']

        self.renderables = format()

    def __rich_console__(self, console: Console,
                         options: ConsoleOptions) -> RenderResult:
        yield Panel(self.renderables, expand=False)


class DailyForecastCard:

    def __init__(self, weather_report, unit, days, verbosity):

        def format():
            renderables = (
                f"{self.location_header}\n"
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

        location_dict = weather_report['location']
        forecast_dict = weather_report['forecast']['forecastday']

        for day in range(self.days):
            self.ascii_art = (
                ascii_dict['day'][forecast_dict[day]['day']['condition']
                                  ['text'].replace(' ', '_').lower()]
            )

            self.location_header = (
                f"{location_dict['name']}, "
                f"{location_dict['region']}, "
                f"{location_dict['country']}"
            )

            self.lat_long = (
                f"{location_dict['lat']},"
                f"{location_dict['lon']},"
            )

            self.localtime = (
                f"{location_dict['localtime']}"
            )

            self.date = f"{forecast_dict[day]['date']}"
            self.timezone = f"{weather_report['location']['tz_id']}"

            self.conditions = (
                f"{forecast_dict[day]['day']['condition']['text']}"
            )

            self.humidity = (
                f"{forecast_dict[day]['day']['avghumidity']}"
            )

            self.uv = (
                f"{forecast_dict[day]['day']['uv']}"
            )

            self.sunrise = (
                f"{forecast_dict[day]['astro']['sunrise']}"
            )

            self.sunset = (
                f"{forecast_dict[day]['astro']['sunset']}"
            )

            self.moonrise = (
                f"{forecast_dict[day]['astro']['moonrise']}"
            )

            self.moonset = (
                f"{forecast_dict[day]['astro']['moonset']}"
            )

            self.moon_phase = (
                f"{forecast_dict[day]['astro']['moon_phase']}"
            )

            self.moon_illumination = (
                f"{forecast_dict[day]['astro']['moon_illumination']}"
            )

            if forecast_dict[day]['day']['daily_will_it_rain']:
                self.rain_percent = (
                    f"{forecast_dict[day]['day']['daily_chance_of_rain']}"
                )

            if forecast_dict[day]['day']['daily_will_it_snow']:
                self.rain_percent = (
                    f"{forecast_dict[day]['day']['daily_chance_of_snow']}"
                )

            if unit == 'metric':
                self.max_temp = (
                    f"{forecast_dict[day]['day']['maxtemp_c']}°C"
                )
                self.min_temp = (
                    f"{forecast_dict[day]['day']['mintemp_c']}°C"
                )
                self.avg_temp = (
                    f"{forecast_dict[day]['day']['avgtemp_c']}°C"
                )
                self.max_wind = (
                    f"{forecast_dict[day]['day']['maxwind_kph']} kph"
                )
                self.total_precip = (
                    f"{forecast_dict[day]['day']['totalprecip_mm']} mm"
                )
                self.avg_vis = (
                    f"{forecast_dict[day]['day']['avgvis_km']} km"
                )

            else:
                self.max_temp = (
                    f"{forecast_dict[day]['day']['maxtemp_f']}°F"
                )
                self.min_temp = (
                    f"{forecast_dict[day]['day']['mintemp_f']}°F"
                )
                self.avg_temp = (
                    f"{forecast_dict[day]['day']['avgtemp_f']}°F"
                )
                self.max_wind = (
                    f"{forecast_dict[day]['day']['maxwind_mph']} mph"
                )
                self.total_precip = (
                    f"{forecast_dict[day]['day']['totalprecip_in']} in"
                )
                self.avg_vis = (
                    f"{forecast_dict[day]['day']['avgvis_miles']} miles"
                )

            self.renderables[day] = format()

    def __rich_console__(self, console: Console,
                         options: ConsoleOptions) -> RenderResult:
        renderable_table = Table()

        for day in range(self.days):
            renderable_table.add_column(str(date.today() + timedelta(day)))

        renderable_table.add_row(*self.renderables.values())
        yield renderable_table
