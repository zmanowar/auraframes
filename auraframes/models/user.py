from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: str
    created_at: str
    updated_at: str
    name: str
    email: str
    short_id: Optional[str]
    show_push_prompt: bool
    latest_app_version: Optional[str]
    attribution_id: Optional[str]
    attribution_string: Optional[str]
    test_account: Optional[bool]
    avatar_file_name: Optional[str]
    has_frame: Optional[bool]
    analytics_optout: bool = None
    admin_account: Optional[bool] = False
    auth_token: str = None
