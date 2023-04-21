from auraframes.api.baseApi import BaseApi


class PlaylistApi(BaseApi):

    def get_playlist_assets(self, playlist_id: str, frame_id: str, _filter: str = None, limit: int = None,
                            cursor: str = None):
        self._client.get(f'/playlists/{playlist_id}/assets.json',
                         query_params={'frame_id': frame_id, 'filter': _filter, 'limit': limit, 'cursor': cursor})
