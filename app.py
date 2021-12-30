from flask import Flask, render_template, redirect, flash
from os.path import exists
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET')

ROUTES_LOCATION = './static/data/routes.json'

def load_routes():
    if exists(ROUTES_LOCATION):
        routes_json = open(ROUTES_LOCATION, 'r')
        routes_data = json.load(routes_json)['routes']
        routes_json.close()
        return routes_data
    else:
        return []


def resolve_route(routes, route):
    for temp_route in routes:
        print(temp_route)
        if temp_route['route'] == route:
            return temp_route['url']
    flash('Test', 'warning')
    return '/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<route>')
def router(route):
    routes = load_routes()
    return redirect(resolve_route(routes, '/' + route))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)