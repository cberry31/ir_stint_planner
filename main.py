import math
import yaml
import irsdk
import time
from pprint import pprint

# this is our State class, with some helpful variables
class State:
    ir_connected = False
    last_car_setup_tick = -1

# here we check if we are connected to iracing
# so we can retrieve some data
def check_iracing():
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        # don't forget to reset your State variables
        state.last_car_setup_tick = -1
        # we are shutting down ir library (clearing all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')

# our main loop, where we retrieve data
# and do something useful with it
def loop_1():
    # on each tick we freeze buffer with live telemetry
    # it is optional, but useful if you use vars like CarIdxXXX
    # this way you will have consistent data from those vars inside one tick
    # because sometimes while you retrieve one CarIdxXXX variable
    # another one in next line of code could change
    # to the next iracing internal tick_count
    # and you will get incosistent data
    ir.freeze_var_buffer_latest()

    # retrieve live telemetry data
    # check here for list of available variables
    # https://github.com/kutu/pyirsdk/blob/master/vars.txt
    # this is not full list, because some cars has additional
    # specific variables, like break bias, wings adjustment, etc
    t = ir['SessionTime']
    print('session time:', t)

    # retrieve CarSetup from session data
    # we also check if CarSetup data has been updated
    # with ir.get_session_info_update_by_key(key)
    # but first you need to request data, before checking if its updated
    car_setup = ir['CarSetup']
    if car_setup:
        car_setup_tick = ir.get_session_info_update_by_key('CarSetup')
        if car_setup_tick != state.last_car_setup_tick:
            state.last_car_setup_tick = car_setup_tick
            print('car setup update count:', car_setup['UpdateCount'])
            # now you can go to garage, and do some changes with your setup
            # this line will be printed, only when you change something
            # and press apply button, but not every 1 sec
    # note about session info data
    # you should always check if data exists first
    # before do something like ir['WeekendInfo']['TeamRacing']
    # so do like this:
    # if ir['WeekendInfo']:
    #   print(ir['WeekendInfo']['TeamRacing'])

    # and just as an example
    # you can send commands to iracing
    # like switch cameras, rewind in replay mode, send chat and pit commands, etc
    # check pyirsdk.py library to see what commands are available
    # https://github.com/kutu/pyirsdk/blob/master/irsdk.py#L134 (class BroadcastMsg)
    # when you run this script, camera will be switched to P1
    # and very first camera in list of cameras in iracing
    # while script is running, change camera by yourself in iracing
    # and notice how this code changes it back every 1 sec
    ir.cam_switch_pos(0, 1)


def loop():
    t = ir["SessionTime"]
    print("session time:", t)
    laps = ir["CarIdxLapCompleted"]

    # Variables that are needed for calculations
    averageLapTime = ir["LapLastNLapTime"]  # Figure out how this works
    print(f"AVERAGE LAP: {averageLapTime}")
    totalTankSize = 0  # Need to find where this is
    fuelLevel = ir["FuelLevel"]
    fuelPerLap = 1  # TODO: Figure out the calculation for this
    estimatedLapsInStint = math.floor(totalTankSize / fuelPerLap)
    estimatedFuelRemainingAtEndStint = totalTankSize - (
        fuelPerLap * estimatedLapsInStint
    )
    eventLength = ir["SessionTimeTotal"]
    eventLengthRemaining = ir["SessionTimeRemain"]
    leaderAverageLapTime = 1.5  # TODO: Calculate this out

    if (
        not isinstance(eventLength, float)
        or not isinstance(eventLengthRemaining, float)
        or not isinstance(averageLapTime, float)
    ):
        print("Event Length not float", eventLength)
        print("Event Length Remaining not float", eventLengthRemaining)
        print("Average Lap Time not float", averageLapTime)
        return

    totalLaps = math.ceil(eventLength / leaderAverageLapTime)
    remainingLaps = math.ceil(eventLengthRemaining / leaderAverageLapTime)
    fuelNeeded = totalLaps * fuelPerLap
    # stintLength = (
    #     totalTankSize * fuelPerLap
    # ) / averageLapTime  # This might need to be optimized on the formula
    estimatedNextStintTime = 0  # Need to figure out calculation
    # estimatedNumberOfStints = eventLength / stintLength
    print(f"{fuelLevel} / {ir['DriverCarFuelMaxLtr']}")
    print(ir["LapCompleted"])
    print(ir['Drivers'])
    print(ir["CarIdxLap"])

    # ir.session_info is a raw YAML string; load it into a Python dict
    pprint(ir["SessionInfo"])
    allSessions = ir["SessionInfo"]
    currSessionIdx = allSessions.get("CurrentSessionNum",0)
    session_info = ir['SessionInfo']["Sessions"][currSessionIdx]
    pprint(session_info)
        

def getFuelTankInfo():
    try:
        # Access the DriverInfo block
        driver_info = ir['DriverInfo']
        
        # Extract the fuel variables
        max_fuel_ltr = driver_info.get('DriverCarFuelMaxLtr', None)
        max_fuel_pct = driver_info.get('DriverCarMaxFuelPct', None)
        
        if max_fuel_ltr is not None and max_fuel_pct is not None:
            # Calculate the actual limit enforced by the session rules
            true_limit = max_fuel_ltr * max_fuel_pct
            
            print("\n--- Fuel Tank Specification ---")
            print(f"Physical Tank Capacity : {max_fuel_ltr:.2f} L")
            print(f"Session Fuel Limit %   : {max_fuel_pct * 100:.1f}%")
            print(f"Actual Usable Fuel     : {true_limit:.2f} L")
            print(f"Remaining Fuel         : {ir['FuelLevel']:.3f} L")
        else:
            print("Could not find fuel variables in SessionInfo. Are you in a car?")
            
    except Exception as e:
        print(f"Error parsing Session Info: {e}")

if __name__ == '__main__':
    # initializing ir and state
    ir = irsdk.IRSDK()
    state = State()

    try:
        # infinite loop
        while True:
            # check if we are connected to iracing
            check_iracing()
            # if we are, then process data
            if state.ir_connected:
                # loop()
                getFuelTankInfo()
            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            time.sleep(60)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
