import requests

def get_location_by_ip(ip_address):
    try:
        response = requests.get("http://ip-api.com/json/{}".format(ip_address))
        js = response.json()
        location = {
            'ipaddr': js['query'],
            'city': js['city'],
            'country': js['country'],
            'zipcode': js['zip']
        }
        return location
    except Exception as e:
        return None
    
if __name__ == '__main__':
    # Example usage:
    print (get_location_by_ip("142.250.191.174"))
