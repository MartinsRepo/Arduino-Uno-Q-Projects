from arduino.app_utils import *
import time

def loop():
    # One time message
    Bridge.call("display_print", "Python verbunden!\nWarndaten laden...")
    time.sleep(2)
    
    counter = 0
    while True:
        # Dynamical Teststring
        message = f"System Status: OK\nLaufzeit: {counter}s\nQualcomm Power!"
        Bridge.call("display_print", message)
        
        counter += 1
        time.sleep(1.0) # actualize every 5 seconds 

App.run(user_loop=loop)
