import math
import time
from pprint import pprint

from drivers import Driver
from iracing import iRacing


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
    print(ir["Drivers"])
    print(ir["CarIdxLap"])

    # ir.session_info is a raw YAML string; load it into a Python dict
    pprint(ir["SessionInfo"])
    allSessions = ir["SessionInfo"]
    currSessionIdx = allSessions.get("CurrentSessionNum", 0)
    session_info = ir["SessionInfo"]["Sessions"][currSessionIdx]
    pprint(session_info)


if __name__ == "__main__":
    irClass = iRacing()
    ir = irClass.ir
    driver = Driver()

    print(ir.var_headers_names)

    irClass.check_iracing()
    if irClass.ir_connected:
        irClass.getFuelTankInfo()
        driver.printDriverInfo()
    lap = 0

    try:
        while True:
            irClass.check_iracing()
            if irClass.ir_connected:
                fuelInfo = irClass.getFuelTankInfo()
                fuelTank = fuelInfo["UsableFuelCapacity"]
                print(ir["Lap"])
                if ir["Lap"] > lap:
                    lap = ir["Lap"]
                    driver.lapTimes.append(ir["LapLastLapTime"])
                    print(f"Average Lap Time: {driver.calculateAverageLapTime()}")
                    print(f"Average Fuel Useage: {driver.calculateAverageFuelUseage()}")
                    if driver.averageFuelUse:
                        print(
                            f"Estimated Remaining Laps on Tank: {math.floor(driver.averageFuelUse / fuelTank)}"
                        )
                # loop()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
