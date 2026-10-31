from pprint import pprint

import irsdk


class iRacing:
    def __init__(self) -> None:
        self.ir_connected = False
        self.last_car_setup_tick = -1
        self.ir = irsdk.IRSDK()

    def check_iracing(self):
        if self.ir_connected and not (self.ir.is_initialized and self.ir.is_connected):
            self.ir_connected = False
            self.last_car_setup_tick = -1
            self.ir.shutdown()
            print("irsdk disconnected")
        elif (
            not self.ir_connected
            and self.ir.startup()
            and self.ir.is_initialized
            and self.ir.is_connected
        ):
            self.ir_connected = True
            print("irsdk connected")

    def getFuelTankInfo(self):
        try:
            driver_info = self.ir["DriverInfo"]

            if driver_info:
                max_fuel_ltr = driver_info.get("DriverCarFuelMaxLtr", None)
                max_fuel_pct = driver_info.get("DriverCarMaxFuelPct", None)

                if max_fuel_ltr is not None and max_fuel_pct is not None:
                    # Calculate the actual limit enforced by the session rules
                    true_limit = max_fuel_ltr * max_fuel_pct
                    fuelTankData = {
                        "physicalTankCapacity": round(max_fuel_ltr, 4),
                        "sessionFuelLimit": round(max_fuel_pct, 5),
                        "UsableFuelCapacity": round(true_limit, 4),
                    }
                    pprint(fuelTankData)
                    return fuelTankData
                else:
                    print("Could not find fuel variables in SessionInfo")

        except Exception as e:
            print(f"Error parsing Session Info: {e}")
