from pprint import pprint

from iracing import iRacing


class Driver:
    def __init__(self) -> None:
        self.id = None
        self.name: str = ""
        self.localTimeZone: str = "America/Chicago"
        self.avavilabilitiesUTC: list = []
        self.tags: list = []
        self.averageLapTime: float = -1
        self.averageFuelUse: float = -1
        self.eventID = None
        self.lapTimes: list = []
        self.fuelUseage: list = []
        self.iracing = iRacing()
        while not self.iracing.ir_connected:
            self.iracing.check_iracing()
        self.getInitInformation()

    def calculateAverageLapTime(self):
        if len(self.lapTimes) > 0:
            self.averageLapTime = sum(self.lapTimes) / len(self.lapTimes)
        return self.averageLapTime

    def printDriverInfo(self):
        pprint(
            {
                "id": self.id,
                "name": self.name,
                "localTimeZone": self.localTimeZone,
                "avavilabilitiesUTC": self.avavilabilitiesUTC,
                "tags": self.tags,
                "averageLapTime": self.averageLapTime,
                "averageFuelUse": self.averageFuelUse,
                "eventID": self.eventID,
                "lapTimes": self.lapTimes,
            }
        )

    def calculateAverageFuelUseage(self):
        if len(self.fuelUseage) > 0:
            # The way we need to add to self.fuelUsage is by appending totalTankSize - reaminingFuel at end of lap
            self.averageFuelUse = self.fuelUseage[-1] / len(self.fuelUseage)
        return self.averageFuelUse

    def getInitInformation(self):
        ir = self.iracing.ir
        driverInfo = ir["DriverInfo"]
        driverIdx = driverInfo["DriverCarIdx"]
        self.id = driverInfo["Drivers"][driverIdx]["id"]
        self.name = driverInfo["Drivers"][driverIdx]["UserName"]
