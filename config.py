from log import logger
import re
import yaml
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

class Config:
    def __init__(self, file_list: list[str] = ["config.yaml", "config.yml"]):
        # Import config
        try:
            success = False
            last_exception: Exception = None
            for file in file_list:
                try:
                    with open(file, "r") as file:
                        config = yaml.safe_load(file)
                    success = True
                    break
                except FileNotFoundError as e:
                    last_exception = e
            if not success:
                raise last_exception
        except FileNotFoundError:
            logger.critical('FileNotFoundError while opening file "config.yaml", does it exist? Quitting program.')
            quit()
        except Exception:
            logger.critical("Error while opening configuration file, quitting program!", exc_info=True)
            quit()
            
        self.config = config
        
        self._check_and_get_general()
        self._check_and_get_windows()
        self._check_and_get_stations()
        self._check_and_get_credentials()
        self._check_and_get_colors()
    
    def _check_and_get_general(self):
        try:
            self.general_config: dict = self.config["general"]
            
            setting = "time_zone"
            Helper.is_valid_ZoneInfo(self.general_config[setting])
            
            setting = "SEV-lines use normal line icon colors"
            Helper.is_true_false_caseinsensitive(setting)
            
            setting = "QR-Code-height"
            if not Helper.is_in_range(0, 1):
                raise ValueError
        except KeyError:
            logger.critical(f'KeyError while reading general setting "{setting}", have you typed it correctly? Quitting program.', exc_info=True)
            quit()
        except ValueError:
            logger.critical(f'ValueError while reading general setting "{setting}", it is not a valid value for this setting! Quitting program.', exc_info=True)
            quit()
        except ZoneInfoNotFoundError:
            logger.critical(f'ZoneInfoNotFoundError while reading general setting "{setting}", it is not a valid time sone identifier! See more in the README about this setting. Quitting program.', exc_info=True)
            quit()
    
    def _check_and_get_windows(config) -> list:
        # check if windows where configured correctly
        try:
            index = None
            windows_config: list = config["windows"]
            for try_window in windows_config:
                index = windows_config.index(try_window)
                # check if fields exist and are of correct type
                int(try_window["position_x"])
                int(try_window["position_y"])
                int(try_window["width"])
                int(try_window["height"])
                expected_station = try_window["station"]
                try:
                    config["stations"][expected_station] # also check if the wanted station actually exists in the stations config
                except KeyError:
                    logger.critical(f'KeyError while reading windows configuration, mentioned station {expected_station} does not exist in the station config part! Make sure you haven\'t mistyped it ore the stations config! Quitting program.', exc_info=True)
                    quit()
        except KeyError:
            if index is None:
                logger.critical('KeyError while reading windows configuration, have you typed "windows" correctly? Quitting program.', exc_info=True)
            else:
                logger.critical(f'KeyError while reading window #{index}\'s configuration, have you typed "position_x", "position_y", "width", "height" and "station" correctly? Quitting program.', exc_info=True)
            quit()
        except ValueError:
            logger.critical(f'ValueError while reading window #{index}\'s configuration, are "position_x", "position_y", "width" and "height" integers? Quitting program.', exc_info=True)
            quit()
        
        return windows_config
    
    def _check_and_get_stations(config) -> dict:
        # check if stations where configured correctly
        try:
            try_station = None
            station_config: dict = config["stations"]
            for try_station_key in station_config.keys():
                try_station = station_config[try_station_key]
                for stop_point in try_station:
                    stop_point["stop_point_ref"]
                    for try_optional_argument in stop_point.keys():
                        if try_optional_argument not in ["stop_point_ref", "prefix", "suffix"]:
                            raise ValueError
        except KeyError:
            if try_station is None:
                logger.critical('KeyError while reading station configuration, have you typed "station" correctly? Quitting program.', exc_info=True)
            else:
                logger.critical(f'KeyError while reading station {try_station_key}\'s configuration, have you typed "stop_point_ref", "prefix" and "suffix" correctly? Quitting program.', exc_info=True)
            quit()
        except ValueError:
            logger.critical(f'ValueError while reading station {try_station_key}\'s configuration, invalid property "{try_optional_argument}"! Quitting program.', exc_info=True)
            quit()
        
        return station_config
    
    def _check_and_get_colors(config) -> dict:
        # check if configured colors are valid
        try:
            color = None
            color_config: dict = config["colors"]
            for color in ["header_background", "header_text", "departure_entry_lighter", "departure_entry_darker", "departure_entry_text", "default_icon_background", "default_icon_text", "qr_code_background", "qr_code_foregreound"]:
                if not Config._is_color_valid(color_config[color]):
                    raise ValueError
            
        except KeyError:
            if color is None:
                logger.critical('KeyError while reading color configuration, have you typed "colors" correctly? Quitting program.', exc_info=True)
            else:
                logger.critical(f'KeyError while reading color {color}\'s configuration, have you typed it correctly? Quitting program.', exc_info=True)
            quit()
        except ValueError:
            logger.critical(f'ValueError while reading color {color}\'s configuration, it is not a valid hex code color! Quitting program.', exc_info=True)
            quit()
        
        return color_config
    
    def _check_and_get_credentials(config) -> dict:
        # check if credentials section exists
        try:
            credentials_config: dict = config["credentials"]
        except KeyError:
            logger.critical(f'KeyError while reading credentials config section, have you typed "credentials" correctly? Quitting program.', exc_info=True)
            quit()
        
        # check if url exists
        try:
            credentials_config["url"]
        except KeyError:
            logger.critical(f'KeyError while reading credentials config section, have you typed "url" correctly? Quitting program.', exc_info=True)
            quit()
            
        # check if requestor_ref exists and is prosumeably correct
        try:
            if credentials_config["requestor_ref"].__len__() != 12:
                raise ValueError
        except KeyError:
            logger.critical(f'KeyError while reading credentials config section, have you typed "requestor_ref" correctly? Quitting program.', exc_info=True)
            quit()
        except ValueError:
            logger.warning(f'The requestor_ref given by the config has an unusual length, are you shure it is correct?')
        
        return credentials_config

if __name__ == "__main__":
    print(Config().config)

class Helper:
    hex_color_regex = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    
    @staticmethod
    def does_exist(dict: dict, key) -> None:
        dict[key]
    
    @staticmethod
    def is_color_valid(color_string: str) -> bool:
        regexp = re.compile(Helper.hex_color_regex)
        if regexp.search(color_string):
            return True
        return False
        
    @staticmethod
    def is_in_range(x: float, range: tuple[float, float] | tuple[None, float] | tuple[float, None]) -> bool:
        if range[0] is None:
            return x <= range[1]
        elif range[1] is None:
            return x >= range[0]
        else:
            return x <= max(range) and x >= min(range)
    
    @staticmethod
    def is_valid_ZoneInfo(string: str) -> bool:
        return ZoneInfo(string)
    
    @staticmethod
    def is_true_false_caseinsensitive(string: str, valid_values: list[str] = ['true', 'false']) -> None:
        if str(string).lower() not in valid_values:
            raise ValueError