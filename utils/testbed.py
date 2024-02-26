from typing import Callable, List, Optional

from pyats.topology import Device, Testbed, Interface

from utils.enums import DeviceOS

def get_iosxe_routers(testbed: Testbed) -> List[Device]:
    return [
        device
        for device in testbed.devices.values()
        if device.os == DeviceOS.IOSXE.value
    ]

def get_interfaces_by_condition(
    device: Device, condition: Callable[[Interface], bool]
) -> List[Interface]:
    return [
        interface for interface in device.interfaces.values() if condition(interface)
    ]
