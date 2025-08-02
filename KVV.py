from datetime import datetime, timedelta
import requests

class KVV:
    def __init__(self, url: str, requestor_ref: str, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"):
        self.url = url
        self.requestor_ref = requestor_ref
        self.user_agent = user_agent

        self.headers = {'Content-Type': 'text/xml; charset=utf-8', 
                'User-Agent': f'{self.user_agent}'}
        
    def _get_formatted_xml_string(self, request_timestamp: datetime, stop_point_ref: str, time_delta: timedelta, number_of_results) -> str:
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
            request_timestamp: datetime = datetime.now()
            ) -> requests.Response:

        xml_body = self._get_formatted_xml_string(request_timestamp, stop_point_ref, time_delta, number_of_results)
        
        response = requests.post(self.url, headers=self.headers, data=xml_body).content.decode("utf-8")

        return response