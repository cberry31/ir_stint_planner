from pprint import pprint

from iracing import iRacing


class Driver:
    def __init__(self) -> None:
        self.id = None
        self.name = None
        self.localTimeZone = None
        self.avavilabilitiesUTC = None
        self.tags = None
        self.averageLapTime = None
        self.averageFuelUse = None
        self.eventID = None
        self.lapTimes = []
        self.fuelUseage = []
        self.iracing = iRacing()
        self.getInitInformation()

    def calculateAverageLapTime(self):
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
        self.averageFuelUse = sum(self.fuelUseage) / len(self.fuelUseage)
        return self.averageFuelUse

    def getInitInformation(self):
        ir = self.iracing.ir
        driverInfo = ir["DriverInfo"]
        driverIdx = driverInfo["DriverCarIdx"]
        self.id = driverInfo["id"]
        self.name = driverInfo["Drivers"][driverIdx]["UserName"]
