import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List

from pyats import aetest
from pyats.topology import Device, Testbed

from utils.connection import connect_with_devices, disconnect_devices
from utils.models import DeviceConfig
from utils.testbed import get_iosxe_routers

logger = logging.getLogger(__name__)

IOSXE_ROUTERS = "iosxe_routers"
DEVICES_CONFIG = "devices_config"
BACKUP_FOLDER = "backup_folder"


def create_backup_folder(backup_path: Path) -> Path:
    todays_date = datetime.today().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H-%M-%S")
    backup_folder = backup_path / todays_date / current_time
    logger.info(f"Backup folder path: {backup_folder}")
    backup_folder.mkdir(parents=True, exist_ok=True)
    return backup_folder


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def prepare_devices(self, testbed: Testbed) -> None:
        iosxe_routers = get_iosxe_routers(testbed)
        connect_with_devices(iosxe_routers)
        self.parent.parameters[IOSXE_ROUTERS] = iosxe_routers

    @aetest.subsection
    def prepare_backup_folder(self, backup_path: str) -> None:
        logger.info(f"Creating backup folder")
        self.parent.parameters[BACKUP_FOLDER] = create_backup_folder(Path(backup_path))


class GetBackups(aetest.Testcase):
    @aetest.test
    def get_running_config(self, iosxe_routers: List[Device]) -> None:
        logger.info(f"Getting running configs from all IOSXE routers")
        devices_config = []
        for router in iosxe_routers:
            logger.info(f"Getting running config from {router.name}")
            running_config = router.execute("show running-config")
            devices_config.append(DeviceConfig(name=router.name, config=running_config))
        self.parameters[DEVICES_CONFIG] = devices_config

    @aetest.test
    def save_running_config(
        self, devices_config: List[DeviceConfig], backup_folder: Path
    ) -> None:
        logger.info(f"Saving running config into *.txt files")
        for device_config in devices_config:
            file_name = f"{device_config.name}.txt"
            file_path = backup_folder / file_name
            logger.info(f"Saving running config of {device_config.name} to {file_path}")
            with open(file_path, "w") as file:
                file.write(device_config.config)
        logger.info(f"All files were saved successfully!")


class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_devices(self, iosxe_routers: List[Device]) -> None:
        disconnect_devices(iosxe_routers)
