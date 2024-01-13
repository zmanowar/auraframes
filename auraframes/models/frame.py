from enum import Enum
from typing import Optional

import pydantic
from pydantic import BaseModel

from auraframes.models.meta import AllOptional
from auraframes.models.user import User


class Feature(Enum):
    SKIP_VIDEO_PRELOAD = 'skip_video_preload'
    UDP_COMMANDS = 'udp_commands'
    MQTT_ENABLED = 'mqtt_enabled'


class Frame(BaseModel):
    id: str
    name: str
    user_id: str
    software_version: str
    build_version: str
    hw_android_version: str
    created_at: str
    updated_at: str
    handled_at: str
    deleted_at: Optional[str]
    updated_at_on_client: Optional[str]
    orientation: int
    auto_brightness: bool
    min_brightness: int
    max_brightness: int
    brightness: Optional[int]
    sense_motion: bool
    default_speed: Optional[str]
    slideshow_interval: int
    slideshow_auto: bool
    digits: int
    contributors: Optional[list[User]]
    contributor_tokens: list[dict]
    hw_serial: str
    matting_color: str
    trim_color: str
    is_handling: bool
    calibrations_last_modified_at: str
    gestures_on: bool
    portrait_pairing_off: Optional[bool]
    live_photos_on: bool
    auto_processed_playlist_ids: list[object]  # unknown
    time_zone: str
    wifi_network: str
    cold_boot_at: Optional[str]
    is_charity_water_frame: bool
    num_assets: int
    thanks_on: bool
    frame_queue_url: Optional[str]
    client_queue_url: str
    scheduled_display_sleep: bool
    scheduled_display_on_at: Optional[str]
    scheduled_display_off_at: Optional[str]
    forced_wifi_state: Optional[str]
    forced_wifi_recipient_email: Optional[str]
    is_analog_frame: bool
    control_type: str
    display_aspect_ratio: str
    has_claimable_gift: Optional[bool]
    gift_billing_hint: Optional[str]
    locale: str
    frame_type: Optional[int]
    description: Optional[str]
    representative_asset_id: Optional[str]
    sort_mode: Optional[str]
    email_address: str
    features: Optional[list[Feature]]
    letterbox_style: Optional[str]
    user: User
    playlists: list[dict]  # TODO
    delivered_frame_gift: Optional[dict]  # TODO
    last_feed_item: dict
    last_impression: Optional[dict]
    last_impression_at: str
    child_albums: list
    smart_adds: list
    recent_assets: list

    def is_portrait(self):
        return self.orientation == 2 or self.orientation == 3

    def get_frame_type(self):
        return self.frame_type if self.frame_type else "normal"


class FramePartial(Frame, metaclass=AllOptional):
    pass
