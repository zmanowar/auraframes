from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, validator

from auraframes.models.user import User
from auraframes.utils.dt import parse_aura_dt


class AssetPadding(BaseModel):
    top: float
    right: float
    bottom: float
    left: float


class AssetSetting(BaseModel):
    added_by_id: str
    asset_id: str
    created_at: str
    frame_id: str
    hidden: bool
    id: str
    last_impression_at: str
    reason: str  # TODO: Have only seen "user"
    selected: bool
    updated_at: str
    updated_selected_at: str


class Asset(BaseModel):
    auto_landscape_16_10_rect: Optional[str]
    auto_portrait_4_5_rect: Optional[str]
    burst_id: Any
    burst_selection_types: Any
    colorized_file_name: Optional[str]
    created_at_on_client: Optional[str]
    data_uti: str
    duplicate_of_id: Optional[str]
    duration: Optional[float]
    duration_unclipped: Optional[float]
    exif_orientation: int
    favorite: Optional[bool]
    file_name: str
    glaciered_at: str
    good_resolution: bool
    handled_at: Optional[str]
    hdr: Optional[bool]
    height: int
    horizontal_accuracy: Optional[float]
    id: str
    ios_media_subtypes: Optional[int]
    is_live: Optional[bool]
    is_subscription: bool
    landscape_16_10_url: Optional[str]
    landscape_16_10_url_padding: Optional[AssetPadding]
    landscape_rect: Optional[str]
    landscape_url: Optional[str]
    landscape_url_padding: Optional[AssetPadding]
    live_photo_off: Optional[bool]
    local_identifier: str
    location: Optional[list[float]]  # Lat/Long, seems to default to (-77.8943033, 34.1978216)
    location_name: Optional[str]
    md5_hash: Optional[str]
    minibar_landscape_url: Optional[str]
    minibar_portrait_url: Optional[str]
    minibar_url: Optional[str]
    modified_at: Optional[str]
    orientation: Optional[int]
    original_file_name: Optional[str]
    panorama: Optional[bool]
    portrait_4_5_url: Optional[str]
    portrait_4_5_url_padding: Optional[AssetPadding]
    portrait_rect: Optional[str]
    portrait_url: Optional[str]
    portrait_url_padding: Optional[AssetPadding]
    raw_file_name: Optional[str]
    represents_burst: Any
    rotation_cw: int
    selected: bool
    source_id: str
    taken_at: str
    taken_at_granularity: Any
    taken_at_user_override_at: Optional[str]
    thumbnail_url: Optional[str]
    unglacierable: bool
    upload_priority: int
    uploaded_at: str
    user: User
    user_id: str
    user_landscape_16_10_rect: Optional[str]
    user_landscape_rect: Optional[str]
    user_portrait_4_5_rect: Optional[str]
    user_portrait_rect: Optional[str]
    video_clip_excludes_audio: Optional[bool]
    video_clip_start: Any
    video_clipped_by_user_at: Optional[str]
    video_file_name: Optional[str]
    video_url: Optional[str]
    widget_url: Optional[str]
    width: int

    @property
    def taken_at_dt(self):
        return parse_aura_dt(self.taken_at)

    @property
    def is_local_asset(self):
        return self.id is None


class AssetPartialId(BaseModel):
    id: Optional[str] = None
    local_identifier: Optional[str] = None
    user_id: Optional[str] = None

    @validator('id')
    def check_id_or_local_id(cls, _id, values):
        if not values.get('local_identifier') and not _id:
            raise ValueError('Either id or local_identifier is required')
        return _id

    def to_request_format(self):
        # 'user_id': user_id # in the iphone version user_id is not passed in
        if self.id:
            return {'asset_id': self.id}
        else:
            return {'asset_local_identifier': self.local_identifier}
