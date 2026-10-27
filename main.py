#!python3
import math

import irsdk

ir = irsdk.IRSDK()
ir.startup()

while True:
    t = ir["SessionTime"]
    print("session time:", t)
    laps = ir["CarIdxLapCompleted"]
    print(ir)  # idk if this will work but I would like to see more of what we can get

    # Variables that are needed for calculations
    averageLapTime = ir["LapLastNLapTime"]  # Figure out how this works
    totalTankSize = 0  # Need to find where this is
    fuelLevel = ir["FuelLevel"]
    fuelPerLap = 0  # TODO: Figure out the calculation for this
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
        continue

    totalLaps = math.ceil(eventLength / leaderAverageLapTime)
    remainingLaps = math.ceil(eventLengthRemaining / leaderAverageLapTime)
    fuelNeeded = totalLaps * fuelPerLap
    stintLength = (
        totalTankSize * fuelPerLap
    ) / averageLapTime  # This might need to be optimized on the formula
    estimatedNextStintTime = 0  # Need to figure out calculation
    estimatedNumberOfStints = eventLength / stintLength
