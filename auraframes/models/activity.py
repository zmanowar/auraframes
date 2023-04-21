from __future__ import annotations

import typing
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from auraframes.models.asset import Asset
from auraframes.models.user import User


class ReactionType(Enum):
    THANKS = 'thanks'
    LOVE = 'love'
    THERE_IN_SPIRIT = 'be_there_in_spirit'
    WELL_WISHES = 'make_a_wish'
    HUGS_KISSES = 'hugs_and_kisses'
    FAMILY_HUGS = 'family_hugs'
    WELCOME = 'welcome'


class Reaction(BaseModel):
    activity_id: str
    created_at: str
    formatted_text: str
    plain_text: str
    type: ReactionType
    user: User
    user_id: str
    id: str


class Comment(BaseModel):
    content: str
    created_at: str
    id: str
    user_id: str


class ActivityType(Enum):
    ALBUM_ADDED = 'album_added'
    ALBUM_PHOTOS_ADDED = 'album_photos_added'
    ENTER_CLAIM_CODE = 'enter_claim_code'
    FORCED_WIFI_CLAIMED = 'forced_wifi_frame_claimed'
    FORCED_WIFI_CREATE = 'forced_wifi_frame_created'
    FRAME_CREATED = 'frame_created'
    FRAME_GIFT_CLAIMED = 'frame_gift_claimed'
    FRAME_GIFT_CREATED = 'frame_gift_created'
    PHOTOS_ADDED = 'photos_added'
    USER_JOINED = 'user_joined'


class SuggestionManifest(BaseModel):
    local_identifier: str
    location: list[float]
    taken_at: str


class Activity(BaseModel):
    id: str
    asset_count: int
    comment_count: int
    commenters: list[User]
    created_at: str
    formatted_text: str
    frame_id: str
    plain_text: str
    playlist: typing.Any  # unknown
    playlist_id: Optional[str]
    reactions: list[Reaction]
    recent_comments: list[Comment]
    representative_asset_ids: list[str]
    type: ActivityType
    user_id: str
    viewable_asset_count: int
    suggestion_manifest: Optional[list[SuggestionManifest]] = None
    user: Optional[User] = None
    representative_assets: Optional[list[Asset]] = None
