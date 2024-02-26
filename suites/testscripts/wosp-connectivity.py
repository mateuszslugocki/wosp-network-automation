import ipaddress
import logging
from typing import List

from pyats import aetest
from pyats.topology import Device, Testbed

from utils.connection import connect_with_devices, disconnect_devices
from utils.testbed import get_interfaces_by_condition, get_iosxe_routers

logger = logging.getLogger(__name__)

IOSXE_ROUTERS = "iosxe_routers"


def get_connectivity_test_ips(device: Device) -> List[ipaddress.IPv4Address]:
    connectivity_test_interfaces = get_interfaces_by_condition(
        device,
        lambda interface: hasattr(interface, "connectivity_test")
        and interface.connectivity_test,
    )
    return [interface.ipv4.ip for interface in connectivity_test_interfaces]


def ping_devices(source_device: Device, destination_devices: List[Device]):
    for destination_device in destination_devices:
        if source_device.name == destination_device.name:
            logger.info(
                f"Source device name is the same as destination device name, skipping..."
            )
            continue
        logger.info(
            f"Checking connectivity to {destination_device.name} from {source_device.name}"
        )
        destination_ips = get_connectivity_test_ips(destination_device)
        for destination_ip in destination_ips:
            if not is_ping_success_rate_higher_than_80_percent(
                source_device, destination_ip
            ):
                logger.warning(
                    f"Connectivity to {destination_device.name} from {source_device.name} is not working as expected!"
                )
                return False
    logger.info(f"Full mesh connectivity works as expected")
    return True


def is_ping_success_rate_higher_than_80_percent(
    device: Device, destination: ipaddress.IPv4Address
) -> bool:
    cmd = f"ping {destination}"
    ping_output = device.parse(cmd)
    logger.info(f"Pinging {destination} from {device.name}")
    success_percenet_rate = ping_output["ping"]["statistics"]["success_rate_percent"]
    logger.info(f"Ping success percent rate: {success_percenet_rate}")
    if success_percenet_rate >= 80:
        return True
    return False


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def prepare_devices(self, testbed: Testbed) -> None:
        iosxe_routers = get_iosxe_routers(testbed)
        connect_with_devices(iosxe_routers)
        self.parent.parameters[IOSXE_ROUTERS] = iosxe_routers


class TestFullMeshConnectivity(aetest.Testcase):
    @aetest.test
    def test_connectivity(self, iosxe_routers: List[Device]) -> None:
        logger.info(f"Testing full mesh connectivity")
        for router in iosxe_routers:
            if not ping_devices(router, iosxe_routers):
                self.failed(f"Full mesh connectivity doesn't work as expected!")


class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_devices(self, iosxe_routers: List[Device]) -> None:
        disconnect_devices(iosxe_routers)
