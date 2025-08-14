from datetime import datetime, timedelta
import requests

class KVV:
    """This Class handles everything to do with the KVV Trias API
    """
    def __init__(self, url: str, requestor_ref: str, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"):
        """Creates an instance for API requests an sets static settings

        Args:
            url (str): The URL given to you for API access
            requestor_ref (str): The RequestorRef given to you for API Access
            user_agent (str, optional): The user agent used to make the requests. Defaults to "Mozilla/5.0 (Windows NT 10.0; Win64; x64)".
        """
        
        # set static variables
        self.url = url
        self.requestor_ref = requestor_ref
        self.user_agent = user_agent
        self.headers = {'Content-Type': 'text/xml; charset=utf-8', 
                'User-Agent': f'{self.user_agent}'}
        
    def _get_formatted_xml_string(self, request_timestamp: datetime, stop_point_ref: str, time_delta: timedelta, number_of_results) -> str:
        """Returns a formatted xml string that can then be sent to the API

        Args:
            request_timestamp (datetime): Timestamp of the request to be made
            stop_point_ref (str): StopPointRef to uuse for the request
            time_delta (timedelta): Timedelta between now and when the departures start to be shown (aka walk time to station)
            number_of_results (_type_): Number of results to request

        Returns:
            str: formatted xml string
        """    
        #TODO: double check time_delta
            
        # XLM body for the KVV Trias API request
        # The XML structure is based on the KVV Trias API documentation
        # https://www.kvv-efa.de/trias-api.html
        return f'''<?xml version="1.0" encoding="UTF-8"?>
        <Trias version="1.1" xmlns="http://www.vdv.de/trias" xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.vdv.de/trias file:///C:/development/HEAD/extras/TRIAS/TRIAS_1.1/Trias.xsd">
            <ServiceRequest>
                <siri:RequestTimeStamp>{request_timestamp.replace(microsecond=0).isoformat()}</siri:RequestTimeStamp>
                <siri:RequestorRef>{self.requestor_ref}</siri:RequestorRef>
                <RequestPayload>
                    <StopEventRequest>
                        <Location>
                            <LocationRef>
                                <StopPointRef>{stop_point_ref}</StopPointRef>
                            </LocationRef>
                            <DepArrTime>{(request_timestamp + time_delta).replace(microsecond=0).isoformat()}</DepArrTime>
                        </Location>
                        <Params>
                            <NumberOfResults>{number_of_results}</NumberOfResults>
                            <StopEventType>departure</StopEventType>
                            <IncludeRealtimeData>true</IncludeRealtimeData>
                        </Params>
                    </StopEventRequest>
                </RequestPayload>
            </ServiceRequest>
        </Trias>
        '''.encode('utf-8')
        
    def get(self,
            stop_point_ref,
            number_of_results: int,
            time_delta: timedelta = timedelta(minutes=3),
            ) -> requests.Response:
        """Exeecute an API request to the KVV Trias API

        Args:
            stop_point_ref (_type_): StopPoint to request departures for
            number_of_results (int): Number of results to request
            time_delta (timedelta, optional): Timedelta between now and when the departures start to be shown (aka walk time to station). Defaults to timedelta(minutes=3).
            request_timestamp (datetime, optional): Timestamp of the request. Defaults to datetime.now().

        Returns:
            requests.Response: _description_
        """
        
        request_timestamp = datetime.now()

        # Get formatted xml string
        xml_body = self._get_formatted_xml_string(request_timestamp, stop_point_ref, time_delta, number_of_results)
        
        # Save response
        response = requests.post(self.url, headers=self.headers, data=xml_body).content.decode("utf-8")
        
        # Also write it to the disk for backup or debugging
        with open("response.xml", "w") as f:
            f.write(response)

        # Return the response
        return response