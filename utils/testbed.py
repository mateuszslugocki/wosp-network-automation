from typing import Callable, List

from pyats.topology import Device, Interface, Testbed

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
