import uuid

from auraframes.api.baseApi import BaseApi
from auraframes.models.activity import Activity
from auraframes.models.asset import Asset, AssetPartialId
from auraframes.models.frame import Frame, FramePartial

from auraframes.utils.dt import get_utc_now, format_dt_to_aura


class FrameApi(BaseApi):

    def get_frames(self) -> list[Frame]:
        """
        Gets all frames available for the active user.
        :return: List of all frames the active user owns or is collaborating on.
        """
        json_response = self._client.get('/frames.json')
        return [Frame(**frame_data) for frame_data in json_response.get('frames')]

    def get_frame(self, frame_id: str) -> tuple[Frame, int]:
        """
        Gets frame data for a given `frame_id`
        :param frame_id: Frame id to retrieve
        :return: The hydrated frame and the frame's total asset count.
        """
        json_response = self._client.get(f'/frames/{frame_id}.json')
        return Frame(**json_response.get('frame')), json_response.get('total_asset_count')

    def get_assets(self, frame_id: str, limit: int = 1000, cursor: str = None) -> tuple[list[Asset], str]:
        """
        Gets assets for a `frame_id`. The results are paginated with `limit` results per page. To obtain the next set
        of pages, pass in the cursor from the response.

        :param frame_id: Frame ID to retrieve assets
        :param limit: Maximum number of assets per page / callout.
        :param cursor: The cursor from the previous page.
        :return: List of all the assets, and the next page's cursor (will be `None` if there are no more pages)
        """
        json_response = self._client.get(f'/frames/{frame_id}/assets.json',
                                         query_params={'limit': limit, 'cursor': cursor})
        if json_response.get('error'):
            # json_response.get('message')
            pass
        assets = [Asset(**asset_data) for asset_data in json_response.get('assets')]
        return assets, json_response.get('next_page_cursor')

    def get_activities(self, frame_id: str, cursor: str = None):
        """
        Gets activities associated to a frame. This appears to be paginated, although
        :param frame_id: Frame id to retrieve associated activities
        :param cursor: Cursor of the previous page TODO: **UNUSED?**
        :return: A list of activities, the cursor for the next page
        """
        json_response = self._client.get(f'/frames/{frame_id}/activities.json', query_params={'cursor': cursor})
        return [Activity(**json_activity) for json_activity in
                json_response.get('activities')], json_response.get('next_page_cursor')

    def show_asset(self, frame_id: str, asset_id: str, goto_time: str) -> bool:
        """
        Forces the frame to display the asset.

        :param frame_id: Frame id to control
        :param asset_id: Asset id to display on the frame
        :param goto_time: TODO: Unknown, appears to be the current datetime -- does setting it to the future queue the
                            asset?
        :return: Boolean describing if the frame was able to process the request.
        """
        json_response = self._client.post(f'/frames/{frame_id}/goto.json', data={
            'asset_id': asset_id,
            'frame_id': frame_id,
            'goto_time': goto_time if goto_time else format_dt_to_aura(get_utc_now()),
            'swipe_direction': 0,
            'impression_id': uuid.uuid4(),
            'select_asset': True
        })

        return json_response.get('showing')

    def update_frame(self, frame_id: str, frame_partial: FramePartial):
        """
        Updates a frame by id. This cannot update the frame id.
            TODO: Should we assume that FramePartial has `id` set and use that instead of `frame_id`?

        :param frame_id: Frame to update
        :param frame_partial: `FramePartial` containing changes to the frame.
        :return: Returns the hydrated frame with changes.
        """
        json_response = self._client.put(f'/frames/{frame_id}.json',
                                         data={'frame': frame_partial.dict(exclude_unset=True)})
        return Frame(**json_response.get('frame'))

    def select_asset(self, frame_id: str, asset_partial_id: AssetPartialId) -> int:
        """
        Associates an asset to a frame. This is typically done immediately before the asset is uploaded to S3.

        :param frame_id: Frame id
        :param asset_partial_id: The asset identifier to associate to the frame.
        :return: The number of assets that failed to be associated to the frame.
        """

        # Typical use of this endpoint results in a single AssetPartialId being sent per call.
        json_response = self._client.post(f'/frames/{frame_id}/select_asset.json',
                                          data={'assets': [asset_partial_id.to_request_format()]})

        return json_response.get('number_failed')

    def exclude_asset(self, frame_id: str, asset_partial_id: AssetPartialId) -> int:
        """
        Excludes an asset from displaying in the frame's slideshow. The asset will still show in the app.

        :param frame_id: Frame id
        :param asset_partial_id: The asset identifier to remove from the slideshow.
        :return: The number of assets that failed to be excluded from the frame.
        """

        # Typical use of this endpoint results in a single AssetPartialId being sent per call.
        json_response = self._client.post(f'/frames/{frame_id}/exclude_asset',
                                          data={'assets': [asset_partial_id.to_request_format()]})

        return json_response.get('number_failed')

    def remove_asset(self, frame_id: str, asset_partial_id: AssetPartialId) -> int:
        """
        Disassociates an asset from a frame. This does not seem to remove the asset from S3/Glacier.

        :param frame_id: Frame id containing the asset.
        :param asset_partial_id: The asset identifier to remove from the frame.
        :return: The number of assets that failed to be removed from the frame.
        """

        # Typical use of this endpoint results in a single AssetPartialId being sent per call.
        json_response = self._client.post(f'/frames/{frame_id}/remove_asset.json',
                                          data={'assets': [asset_partial_id.to_request_format()]})

        return json_response.get('number_failed')

    def reconfigure(self, frame_id: str):
        """
        TODO: Unknown
        :param frame_id:
        :return:
        """
        return self._client.post(f'/frames/{frame_id}/reconfigure.json', data=None)

    def add_playlist(self, frame_id: str, playlist_params: any):
        # TODO: Implement
        json_response = self._client.post(f'/frames/{frame_id}/add_playlist.json', data={})

        return json_response

    def remove_playlist(self, frame_id: str, playlist_params: any):
        # TODO: Implement
        json_response = self._client.post(f'/frames/{frame_id}/remove_playlist.json', data={})

        return json_response
