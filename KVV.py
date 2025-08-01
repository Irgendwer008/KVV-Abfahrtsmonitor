from datetime import datetime
import requests

def get(url: str, requestor_ref: str, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", timestamp: datetime = datetime.now()) -> requests.Response:

    headers = {'Content-Type': 'text/xml; charset=utf-8', 
               'User-Agent': f'{user_agent}'}

    xml_body = f'''<?xml version="1.0" encoding="UTF-8"?>
    <Trias version="1.1" xmlns="http://www.vdv.de/trias" xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.vdv.de/trias file:///C:/development/HEAD/extras/TRIAS/TRIAS_1.1/Trias.xsd">
        <ServiceRequest>
            <siri:RequestTimeStamp>{timestamp.replace(microsecond=0).isoformat()}</siri:RequestTimeStamp>
            <siri:RequestorRef>{requestor_ref}</siri:RequestorRef>
            <RequestPayload>
                <StopEventRequest>
                    <Location>
                        <LocationRef>
                            <StopPointRef>de:08212:3</StopPointRef>
                        </LocationRef>
                        <DepArrTime>2025-08-01T17:20:00</DepArrTime>
                    </Location>
                    <Params>
                        <NumberOfResults>8</NumberOfResults>
                        <StopEventType>departure</StopEventType>
                        <IncludeRealtimeData>true</IncludeRealtimeData>
                    </Params>
                    </StopEventRequest>

            </RequestPayload>
        </ServiceRequest>
    </Trias>
    '''

    return requests.post(url, headers=headers, data=xml_body.encode('utf-8'))