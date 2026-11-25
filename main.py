import math
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from drivers import Driver
from iracing import iRacing


class StintPlanner:
    def __init__(self):
        self.irClass = iRacing()
        self.ir = self.irClass.ir
        self.driver = Driver()

    def main(self):
        self.irClass.check_iracing()
        if self.irClass.ir_connected:
            self.irClass.getFuelTankInfo()
            self.driver.printDriverInfo()
        self.lap = 0
        try:
            self.irClass.check_iracing()
            if self.irClass.ir_connected:
                self.fuelInfo = self.irClass.getFuelTankInfo()
                self.fuelTank = self.fuelInfo["UsableFuelCapacity"]
                self.loop()
        except KeyboardInterrupt:
            pass

    def loop(self):
        while True:
            if self.ir["Lap"] > self.lap:
                fuelLevel = self.ir["FuelLevel"]
                print(self.ir["Lap"])
                self.lap = self.ir["Lap"]
                self.driver.lapTimes.append(self.ir["LapLastLapTime"])
                self.driver.fuelUseage.append(self.fuelTank - fuelLevel)
                self.driver.calculateAverageLapTime()
                self.driver.calculateAverageFuelUseage()
                if self.driver.averageFuelUse == 0 and self.fuelTank == 0:
                    continue
                self.calculateStintInfo(fuelLevel)

            time.sleep(0.5)

    def calculateStintInfo(self, fuelLevel):
        self.estimatedTotalLaps = math.floor(self.driver.averageFuelUse / self.fuelTank)
        self.estimatedRemainingLaps = math.floor(self.driver.averageFuelUse / fuelLevel)
        self.estimatedRemainingTime = (
            self.estimatedRemainingLaps * self.driver.averageLapTime
        )
        self.estimatedEndOfStint = datetime.now(
            ZoneInfo(self.driver.localTimeZone)
        ) + timedelta(seconds=self.estimatedRemainingTime)

    def printStintInfo(self):
        print(f"Average Lap Time: {self.driver.averageLapTime}")
        print(f"Average Fuel Useage: {self.driver.averageFuelUse}")
        print(f"Laps on Tank: {self.estimatedTotalLaps}")
        print(f"Remaining Laps on Tank: {self.estimatedRemainingLaps}")
        print(f"Remaining Time on Tank: {self.estimatedRemainingTime}")
        print(f"End of Stint: {self.estimatedEndOfStint}")


if __name__ == "__main__":
    StintPlanner().main()
