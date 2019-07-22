# Задание 1. Доработать приложение по поиску авиабилетов, чтобы оно возвращало билеты по названию города,
# а не по IATA коду. Пункт отправления и пункт назначения должны передаваться в качестве параметров.
# Сделать форматированный вывод, который содержит в себе пункт отправления, пункт назначения, дату вылета,
# цену билета (можно добавить еще другие параметры по желанию)

import requests
import sys


# Search flights from...to
def search_flights(origin='Москва', destination='Лондон', counts=10):
    try:
        # Request for get the IATA code of cities
        req = requests.get(f'https://www.travelpayouts.com/widgets_suggest_params?q={origin} {destination}')
    except ConnectionError:
        print('No connection to site: travelpayouts.com')
        exit(1)

    try:
        # Assign IATA parameters for second request
        iata_data = req.json()
        flight_params = {
            'origin': iata_data['origin']['iata'],
            'destination': iata_data['destination']['iata'],
            'one_way': 'true'
        }
        # Request for get the min-price of flights
        req2 = requests.get("http://min-prices.aviasales.ru/calendar_preload", params=flight_params)
    except ConnectionError:
        print('No connection to site: min-prices.aviasales.ru')
        exit(1)

    try:
        # Print format flights
        data = req2.json()
        tickets = data['best_prices'][:counts]
        for ticket in tickets:
            print(f"Пункт отправления: {iata_data['origin']['name']} ({ticket['origin']})")
            print(f"Пункт назначения: {iata_data['destination']['name']} ({ticket['destination']})")
            print(f"Дата вылета: {ticket['depart_date']}")
            print(f"Цена билета: {ticket['value']}")
            print(f"Поставщик услуги: {ticket['gate']}\n")
    except Exception:
        print(Exception)
        exit(1)


if __name__ == '__main__':
    try:
        # Parse the arguments
        origin = sys.argv[1]
        destination = sys.argv[2]
    except Exception:
        print('Please, set the origin and destination cities, and run from terminal (with arguments)')
        exit(1)

    search_flights(origin, destination)
