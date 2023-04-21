from auraframes.api.baseApi import BaseApi
from auraframes.models.person import Person


class PeopleApi(BaseApi):

    def get_people(self):
        json_response = self._client.get('/people.json')
        return [Person(**json_person) for json_person in json_response.get('people')]

    def get_people_assets(self, cursor: str = None):
        json_response = self._client.get('/people/all_assets.json', query_params={'cursor': cursor})

        return json_response

    def get_person(self, person_id: str):
        # TODO: This may not be operational
        json_response = self._client.get(f'/people/{person_id}.json')

        return json_response

    def get_person_assets(self, person_id: str):
        # TODO: This may not be operational
        json_response = self._client.get(f'/people/{person_id}/assets.json')
        return json_response
