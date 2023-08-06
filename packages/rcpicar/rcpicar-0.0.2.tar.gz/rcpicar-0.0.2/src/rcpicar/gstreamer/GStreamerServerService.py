from __future__ import annotations
from subprocess import PIPE, TimeoutExpired
from typing import Optional, Tuple
from .GStreamerRequestMessage import GStreamerRequestMessage
from .GStreamerResponseMessage import GstreamerResponseMessage
from .VideoSettings import VideoSettings
from ..constants import caps_line_prefix
from ..process import IProcess, ProcessFactory
from ..reliable import IReliableDisconnectListener, IReliableService
from ..receive import IReceiveListener, IReceiveService
from ..send import ISendService
from ..service import IService, IServiceManager
from ..util.argument import IArguments
from ..util.ConnectionDetails import ConnectionDetails
from ..util.Lazy import Lazy
from ..util.Placeholder import Placeholder


class GStreamerPipeline:
    def __init__(
            self,
            address: Tuple[str, int],
            caps: str,
            raspivid_process: IProcess,
            settings: VideoSettings
    ) -> None:
        self.address = address
        self.caps = caps
        self.raspivid_process = raspivid_process
        self.settings = settings


class GStreamerServerArguments(IArguments):
    def __init__(self) -> None:
        self.bin_gst_launch = Lazy(lambda store: 'gst-launch-1.0')
        self.bin_raspivid = Lazy(lambda store: 'raspivid')


class GStreamerServerService(
    IService,
    IReceiveListener,
    IReliableDisconnectListener
):
    def __init__(
            self,
            arguments: GStreamerServerArguments,
            process_factory: ProcessFactory,
            receive_service: IReceiveService,
            reliable_service: IReliableService,
            send_service: ISendService,
            service_manager: IServiceManager,
    ) -> None:
        self.arguments = arguments
        self.caps: Placeholder[str] = Placeholder()
        self.gstreamer_pipeline: Placeholder[GStreamerPipeline] = Placeholder()
        self.process_factory = process_factory
        self.send_service = send_service
        receive_service.add_receive_listener(self)
        reliable_service.add_reliable_disconnect_listener(self)
        service_manager.add_service(self)

    def get_service_name(self) -> str:
        return __name__

    def join_service(self, timeout_seconds: Optional[float] = None) -> bool:
        gstreamer_pipeline = self.gstreamer_pipeline.get_optional()
        if gstreamer_pipeline is not None:
            try:
                gstreamer_pipeline.raspivid_process.wait(timeout_seconds)
                return False
            except TimeoutExpired:
                return True
        else:
            return False

    def open_video(self, address: Tuple[str, int], settings: VideoSettings) -> str:
        with self.gstreamer_pipeline as (gstreamer_pipeline, set_gstreamer_pipeline):
            if gstreamer_pipeline is not None:
                if gstreamer_pipeline.address == address \
                        and gstreamer_pipeline.settings.bit_rate == settings.bit_rate \
                        and gstreamer_pipeline.settings.fps == settings.fps \
                        and gstreamer_pipeline.settings.height == settings.height \
                        and gstreamer_pipeline.settings.width == settings.width:
                    return gstreamer_pipeline.caps
                else:
                    gstreamer_pipeline.raspivid_process.terminate()
            raspivid_process = self.process_factory((
                self.arguments.bin_raspivid.get(),
                '-n', '-t', '0',
                '-h', str(settings.height),
                '-w', str(settings.width),
                '-fps', str(settings.fps),
                '-b', str(settings.bit_rate),
                '-o', '-'
            ), None, PIPE)
            gst_launch_process = self.process_factory((
                self.arguments.bin_gst_launch.get(), '-v', 'fdsrc', '!', 'h264parse', '!', 'rtph264pay', '!', 'udpsink',
                f'host={address[0]}', f'port={address[1]}'
            ), raspivid_process.get_stdout(), PIPE)
            caps = None
            while caps is None:
                line = gst_launch_process.get_stdout().readline().decode()
                if line.startswith(caps_line_prefix):
                    caps = line[len(caps_line_prefix):-1]
            return set_gstreamer_pipeline(GStreamerPipeline(address, caps, raspivid_process, settings)).caps

    def on_receive(self, message: bytes, details: ConnectionDetails) -> None:
        request = GStreamerRequestMessage.decode(message)
        self.send_service.send(
            GstreamerResponseMessage(self.open_video(
                request.address,
                request.settings,
            ), request.address[1]).encode())

    def start_service(self) -> None:
        pass

    def stop_service(self) -> None:
        gstreamer_pipeline = self.gstreamer_pipeline.get_optional_and_clear()
        if gstreamer_pipeline is not None:
            gstreamer_pipeline.raspivid_process.terminate()

    def on_reliable_disconnect(self, details: ConnectionDetails) -> None:
        self.stop_service()
