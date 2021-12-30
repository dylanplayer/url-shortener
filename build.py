import json
from os.path import exists

ROUTES_LOCATION = './static/data/routes.json'

def load_routes():
    if exists(ROUTES_LOCATION):
        routes_json = open(ROUTES_LOCATION, 'r')
        routes_data = json.load(routes_json)['routes']
        routes_json.close()
        return routes_data
    else:
        create_routes_file()
        return load_routes()

def create_routes_file():
    routes_file = open(ROUTES_LOCATION, 'w')
    routes_data = {'routes': []}
    json.dump(routes_data, routes_file)
    routes_file.close()

def update_routes(routes):
    routes_file = open(ROUTES_LOCATION, 'w')
    routes_data = {'routes': routes}
    json.dump(routes_data, routes_file)
    routes_file.close()
    return load_routes()

def print_routes(routes):
    if len(routes) > 0:
        print('\nCurrent Routes:')
        for route in routes:
            print(f'Route: {route["route"]} | URL: {route["url"]}')
        print()
    else:
        print('No routes exist')

def route_exists(routes, new_route):
    for route in routes:
        if route['route'] == new_route:
            return True
    return False

def delete_route(routes, del_route):
    if route_exists(routes, del_route):
        for route in routes:
            if route['route'] == del_route:
                del routes[routes.index(route)]
                print(f'{route["route"]} deleted\n')
                return update_routes(routes)
    else:
        print(f'{del_route} does not exist')
        return routes

def print_commands():
    print('\nCommands: ')
    print('/a | add route')
    print('/d | delete route')
    print('/v | view routes')
    print('/h | help')
    print('/q | quit\n')

print('-------- URL Shortener --------')
routes = load_routes()

user_input = ''
while user_input != '/q':
    user_input = input('Enter a command (/h for help): ')
    if user_input == '/h':
        print_commands()
    elif user_input == '/a':
        route = input('Enter route: ')
        if route[0] != '/':
            route = '/' + route
        while route_exists(routes, route):
            print('Route Already Exists')
            route = input('Enter route: ')
            if route[0] != '/':
                route = '/' + route
        url = input('Enter URL: ')
        routes.append({
            'route': route,
            'url':  url,
        })
        routes = update_routes(routes)
    elif user_input == '/v':
        print_routes(routes)
    elif user_input == '/d':
        if len(routes) > 0:
            route = input('\nEnter route to delete: ')
            if route[0] != '/':
                route = '/' + route
            routes = delete_route(routes, route)
        else:
            print('No routes to delete')
    elif user_input != '/q':
        print('Command Unknown\n')
