from auraframes.api.baseApi import BaseApi

from auraframes.models.activity import Activity, Comment
from auraframes.models.asset import Asset, AssetSetting
from auraframes.models.user import User


class ActivityApi(BaseApi):

    def get_comments(self, activity_id: str) -> tuple[list[Comment], int, list[User]]:
        """
        Gets all comments on an activity.

        :param activity_id: Activity id to retrieve comments
        :return: A list of comments, the number of new (unseen)
            comments, and a list of user data associated to the comments.
        """
        json_response = self._client.get(f'/activities/{activity_id}/comments.json')
        return (
            [Comment(**json_comment) for json_comment in json_response.get('comments')],
            json_response.get('new_count'),
            [User(**json_user) for json_user in json_response.get('users')]
        )

    def create_comment(self, activity_id: str, content: str) -> tuple[Activity, Comment]:
        """
        Creates a comment on an activity.
        :param activity_id: Activity id
        :param content: The text content of the comment.
        :return: The hydrated activity and the hydrated comment.
        """
        json_response = self._client.post(f'/activities/{activity_id}/create_comment.json', data={'content': content})

        return Activity(**json_response.get('activity')), Comment(**json_response.get('comment'))

    def remove_comment(self, activity_id: str, comment_id: str):
        """
        Removes a comment from an activity.
        :param activity_id: Activity id
        :param comment_id: Comment id associated to the activity
        :return: The hydrated activity with the comment removed.
        """
        json_response = self._client.post(f'/activities/{activity_id}/remove_comment.json',
                                          data={'comment_id': comment_id})

        return Activity(**json_response.get('activity'))

    def get_activity_assets(self, activity_id: str, limit: int = 1000, cursor: str = None):
        """
        Gets assets associated to an activity. The results are paginated with `limit` results per page. To obtain the next set
        of pages, pass in the cursor from the response.

        TODO: The API doesn't seem to produce a cursor.

        :param activity_id: Activity id
        :param limit: Maximum number of assets per page / callout.
        :param cursor: The cursor from the previous page.
        :return: A list of assets and a list of asset settings.
        """
        json_response = self._client.get(f'/activities/{activity_id}/assets.json',
                                         query_params={'limit': limit, 'cursor': cursor})
        return (
            [Asset(**json_asset) for json_asset in json_response.get('assets')],
            [AssetSetting(**json_asset_setting) for json_asset_setting in json_response.get('asset_settings')]
        )

    def post_activity(self, activity_id: str, frame_id: str, data: dict):
        """
        TODO: Unknown
        :param activity_id:
        :param frame_id:
        :param data:
        :return:
        """
        json_response = self._client.post(f'/activities/{activity_id}/copy.json', data=data,
                                          query_params={'frame_id': frame_id})
        return json_response

    def delete_activity(self, activity_id: str) -> None:
        """
        Deletes the activity. TODO: Better description
        :param activity_id: Activity to remove
        """
        self._client.delete(f'/activities/{activity_id}')

        # Response is typically an empty JSON object.
        return None
