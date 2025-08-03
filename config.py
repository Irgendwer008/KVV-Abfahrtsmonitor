from log import logger
import yaml
from abc import abstractmethod

class Config:
    @abstractmethod
    def read(file_list: list[str] = ["config.yaml", "config.yml"]) -> dict:
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
            logger.critical("Error while reading configuration, quitting program!", exc_info=True)
            quit()
        
        return config
    
    @abstractmethod
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
    
    @abstractmethod
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
                logger.critical('KeyError while reading windows configuration, have you typed "station" correctly? Quitting program.', exc_info=True)
            else:
                logger.critical(f'KeyError while reading station {try_station_key}\'s configuration, have you typed "stop_point_ref", "prefix" and "suffix" correctly? Quitting program.', exc_info=True)
            quit()
        except ValueError:
            logger.critical(f'ValueError while reading station {try_station_key}\'s configuration, invalid property "{try_optional_argument}"! Quitting program.', exc_info=True)
            quit()
        
        return station_config
    
    @abstractmethod
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
    
    @abstractmethod
    def check(config: str) -> tuple[list, dict, dict]:
        windows_config = Config._check_and_get_windows(config)
        stations_config = Config._check_and_get_stations(config)
        credentials_config = Config._check_and_get_credentials(config)
        
        return windows_config, stations_config, credentials_config

if __name__ == "__main__":
    Config.check(Config.read())