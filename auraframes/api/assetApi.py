from auraframes.api.baseApi import BaseApi

# TODO: Untested
from auraframes.models.asset import Asset, AssetPartialId


class AssetApi(BaseApi):

    def batch_update(self, asset: Asset) -> tuple[list[str], list[AssetPartialId]]:
        """
        Posts new metadata to the API. This does not appear to affect the frame; however subsequent calls to retrieve
        this asset will have the modified metadata.

        Primarily used to to update an asset after the image has been uploaded to S3.

        :param asset: Asset containing new metadata
        :return: List of sent remote ids, list of received AssetPartialId successes
        """
        json_response = self._client.put(f'/assets/batch_update.json', data={
            "assets": [
                asset.dict(
                    include={
                        'data_uti': True,
                        'favorite': True,
                        'file_name': True,
                        'height': True,
                        'local_identifier': True,
                        'location': True,
                        'md5_hash': True,
                        'modified_at': True,
                        'orientation': True,
                        'selected': True,
                        'taken_at': True,
                        'upload_priority': True,
                        'width': True
                    })
            ]
        })

        return json_response.get('ids'), [AssetPartialId(**partial_asset_id) for partial_asset_id in
                                          json_response.get('successes')]

    def get_asset_by_local_identifier(self, local_id: str):
        """
        Retrieves an asset given a local id.
        :param local_id: A local id string.
        :return: The retrieved asset, related child albums, and any smart adds related to the asset.
        """
        json_response = self._client.get(f'/assets/asset_for_local_identifier.json',
                                         query_params={'local_identifier': local_id})

        return Asset(**json_response.get('asset')), json_response.get('child_albums'), json_response.get('smart_adds')

    def update_taken_at_date(self, asset: Asset) -> Asset:
        """
        Updates an asset's taken_date and taken_at_granularity. This will modify the date displayed in the frame and
        from future responses.
        :param asset: Asset with new taken_at or taken_at_granularity
        :return: The asset with modified dates
        """
        request = {
            'taken_at': asset.taken_at,
            'taken_at_granularity': asset.taken_at_granularity
        }

        if asset.is_local_asset:
            request.update({'local_identifier': asset.local_identifier, 'source_id': asset.source_id})
        else:
            request.update({'id': asset.id})

        json_response = self._client.post(f'/assets/update_taken_at_date.json', data=request)
        return Asset(**json_response)

    def delete_asset(self, asset: Asset):
        """
        Deletes the asset. **Currently unknown if this is used, most deletions occur by removing
        the activity; maybe this deletes it from S3/Glacier** see :func:`FrameApi.remove_asset`

        :param asset: Asset for removal
        :return: TODO
        """
        if asset.is_local_asset:
            json_response = self._client.post(f'/assets/destroy_by_local_identifier.json',
                                              data={'local_identifier': asset.local_identifier})
        else:
            json_response = self._client.delete(f'/assets/{asset.id}.json')

        return json_response

    def crop_asset(self, asset: Asset) -> Asset:
        """
        Crops an asset, modifying `rotation_cw`, `user_landscape_rect`, `user_portrait_rect` and related
        aspect ratio rects.
        :param asset: Asset containing new rotation/rect data.
        :return: The asset with modified crop fields.
        """
        json_response = self._client.post(f'/assets/crop.json', data=asset.dict(
            include={
                'id': True,
                'local_identifier': True,
                'user_id': True,
                'rotation_cw': True,
                'user_landscape_16_10_rect': True,
                'user_landscape_rect': True,
                'user_portrait_4_5_rect': True,
                'user_portrait_rect': True
            }))

        return Asset(**json_response.get('asset'))
