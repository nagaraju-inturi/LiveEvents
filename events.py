import os
import requests

def getEvents(keyword, city, zipcode, evdate, page):
    # TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
    TICKETMASTER_API_KEY = "R5unI6FfUKMxj7oAKappEHj7uyhfJInA"
    inputStr = ""
    if keyword is not None and keyword != "":
        inputStr = inputStr + "&keyword=" + keyword
    if city  != "":
         inputStr = inputStr + "&city=" + city
    if zipcode  != "":
        inputStr = inputStr + "&postalCode=" + zipcode
    
    inputStr = inputStr + "&startDateTime=" + evdate + "T00:00:00Z"

    # url = ("https://app.ticketmaster.com/discovery/v2/events?apikey="
    #        + TICKETMASTER_API_KEY 
    #        + inputStr
    #        + "&startDateTime=2024-05-19T20:00:00Z"
    #        + "&endDateTime=2024-12-32T20:00:00Z"
    #        + "&page="
    #        + page
    # )
    url = ("https://app.ticketmaster.com/discovery/v2/events?apikey="
           + TICKETMASTER_API_KEY 
           + inputStr
           + "&page="
           + page
           + "&stort=date,asc"
    )
    # print (url)

    ticketmaster_request = requests.get(url=url)

    ticketmaster_response_json = ticketmaster_request.json()

    events = []
    event = {}
    totalPages = {}

    try:
        for i in ticketmaster_response_json["_embedded"]["events"]:
            event = {}
            
            try:
                event["event_id"] = i["id"]
            except KeyError as e:
                event["event_id"] = "TBD"

            try:
                event["title"] = i["name"]
            except KeyError as e:
                event["title"] = "TBD"
            
            # try:
            #     event["imageUrl"] = i["images"][0]["url"]
            # except KeyError as e:
            #     event["imageUrl"] = "TBD"

            try:
                event["date"] = i["dates"]["start"]["localDate"]
            except KeyError as e:
                event["date"] = "TBD"

            try:
                event["city"] = i["_embedded"]["venues"][0]["city"]["name"]
            except KeyError as e:
                event["city"] = "TBD"
            
            try:
                event["zipcode"] = i["_embedded"]["venues"][0]["postalCode"]
            except KeyError as e:
                event["zipcode"] = "TBD"
            
            try:
                event["minPrice"] = "$" + str(i["priceRanges"][0]["min"])
            except KeyError as e:
                event["minPrice"] = "TBD"

            try:
                event["maxPrice"] = "$" + str(i["priceRanges"][0]["max"])
            except KeyError as e:
                event["maxPrice"] = "TBD"

            events.append(event)
        
                    
    except KeyError as e:
        return None

    return events


if __name__ == '__main__':
    # Example usage:
    p1_events = getEvents('1')
    p2_events = getEvents('2')
    print (p1_events)
    print ("\nPAGE2:\n")
    print (p2_events)
    print (p1_events == p2_events)
