#  Copyright (c) 2021. Mulliken, LLC - All Rights Reserved
#  You may use, distribute and modify this code under the terms
#  of the attached license. You should have received a copy of
#  the license with this file. If not, please write to:
#  joshua@mulliken.net to receive a copy
import asyncio
import time
from threading import Thread
from typing import Any, List, Optional, Dict, Callable, Tuple

from wyzeapy.services.base_service import BaseService
from wyzeapy.types import Device, DeviceTypes, Event
from wyzeapy.utils import return_event_for_device


class Camera(Device):
    def __init__(self, dictionary: Dict[Any, Any]):
        super().__init__(dictionary)

        self.last_event: Optional[Event] = None
        self.last_event_ts: int = int(time.time() * 1000)
        self.on: bool = True


class CameraService(BaseService):
    _updater_thread: Optional[Thread] = None
    _subscribers: List[Tuple[Camera, Callable[[Camera], None]]] = []

    async def update(self, camera: Camera):
        response = await self.get_full_event_list(10)
        raw_events = response['data']['event_list']
        latest_events = [Event(raw_event) for raw_event in raw_events]

        if (event := return_event_for_device(camera, latest_events)) is not None:
            camera.last_event = event
            camera.last_event_ts = event.event_ts

        return camera

    async def register_for_updates(self, camera: Camera, callback: Callable[[Camera], None]):
        if not self._updater_thread:
            self._updater_thread = Thread(target=self.update_worker, daemon=True)

        self._subscribers.append((camera, callback))

    def update_worker(self):
        loop = asyncio.get_event_loop()
        while True:
            if len(self._subscribers) < 1:
                time.sleep(0.1)
            else:
                for camera, callback in self._subscribers:
                    callback(asyncio.run_coroutine_threadsafe(self.update(camera), loop).result())

    async def get_cameras(self) -> List[Camera]:
        if self._devices is None:
            self._devices = await self.get_devices()

        cameras = [device for device in self._devices if device.type is DeviceTypes.CAMERA]

        return [Camera(camera.raw_dict) for camera in cameras]

    async def turn_on(self, camera: Device):
        if camera.type in [
            DeviceTypes.CAMERA
        ]:
            await self.run_action(camera, "power_on")

    async def turn_off(self, camera: Device):
        if camera.type in [
            DeviceTypes.CAMERA
        ]:
            await self.run_action(camera, "power_off")
