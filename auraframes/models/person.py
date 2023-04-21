from pydantic import BaseModel


class Person(BaseModel):
    id: str
    created_at: str
    name: str
    published_at: str
    similar_people_ids: list[str]
    thumb_file_name: str
    updated_at: str
    user_id: str


class PersonAssetSetting(BaseModel):
    asset_local_identifier: str
    created_at: str
    detected_face_id: str
    id: str
    person_id: str
    source_id: str
    updated_at: str
    user_action: str
    user_action_updated_at: str
