# DOCUMENTATION
# https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/


# [TO DO]
# - Add if __name__ == "__main__":
#           app.run(debug=True)
#   So that restarting the server is not necessary to detect major changes

import os

from flask import Flask
# Used to render the button from the html led_button template
from flask import render_template

# [RASBERRYPI CODE] - Commented out since modules do not work on main desktop
# LED support
from gpiozero import LED
import time

# [LEDS]
ledRed = LED(4)
ledBlue = LED(5)
ledYellow = LED(6)

# [RELAYS]
k1Relay = LED(17)

def blink(led, seconds, speed=2):
    speed = 1 / speed
    for i in range(seconds):
        led.on()
        time.sleep(speed)
        led.off()
        time.sleep(speed)

def led_on(led):
    led.on()

def led_off(led):
    led.off()


def create_app(test_config=None):
    # Creates and configures the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Loads the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Loads the test config if passed in
        app.config.from_mapping(test_config)

    # Attempts to determine if the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Test page that goes home
    @app.route('/')
    def home():
        return render_template('base.html')

    # [TEST] LED ON FUNCTION
    #@app.route('/led_change', defaults={'led_state': None})
    @app.route('/led_change')
    def led_menu():
        return render_template('led_button.html')

    @app.route('/led_change/<led_state>')
    def led_change(led_state):
        # Turning LED on [CODE]
        if led_state == "off":
            print("led is off")
            led_off(ledYellow)
            
        elif led_state == "on":
            print('led is on')
            led_on(ledYellow)

        else:
            print('Changing LED can be done here!')

        blink(ledBlue, 3, 5)
        return render_template('led_button.html') #'led_changed'

    @app.route('/outside_lights_change')
    def lights_menu():
        return render_template('outside_lights_change.html')

    @app.route('/outside_lights_change/<lights_state>')
    def outside_lights_change(lights_state):
        # Turning LED on [CODE]
        if lights_state == "off":
            print("lights are off")
            # Inverted since relay is using NC -- normally closed
            led_on(k1Relay)
            
        elif lights_state == "on":
            print('lights are on')
            # Inverted since relay is using NC -- normally closed
            led_off(k1Relay)

        else:
            print('Changing OUTSIDE LIGHTS can be done here!')

        #[#]blink(ledBlue, 3, 5)
        return render_template('outside_lights_change.html') #'led_changed'



    @app.route('/about_us')
    def about_us():
        return 'About Us'


    @app.route('/contact_us')
    def contact_us():
        return 'Contact us'

    # Imports function from the factory
    from . import db
    db.init_app(app)

    return app
