from auraframes.api.baseApi import BaseApi
from auraframes.models.user import User
from auraframes.utils import settings


class AccountApi(BaseApi):

    def login(self, email: str, password: str) -> User:
        """
        Authenticates with the API.

        :param email: Registered email
        :param password: Registered password (plaintext)
        :return: Hydrated user object
        """
        login_payload = {
            'user': {
                'email': email,
                'password': password
            },
            'locale': settings.LOCALE,
            'app_identifier': settings.AURA_APP_IDENTIFIER,
            'identifier_for_vendor': settings.DEVICE_IDENTIFIER,
            'client_device_id': settings.DEVICE_IDENTIFIER
        }

        json_response = self._client.post('/login.json', login_payload)
        if json_response.get('error') or not json_response.get('result'):
            # TODO: Error handling
            pass

        return User(**json_response.get('result').get('current_user'))

    def register(self, email: str, password: str, name: str) -> User:
        """
        Registers an account.

        :param email: Email to register with
        :param password: Password (plaintext) to register with
        :param name: Display name
        :return: Hydrated user object for the registered user.
        """
        register_payload = {
            'email': email,
            'name': name,
            'password': password,
            'identifier_for_vendor': settings.DEVICE_IDENTIFIER,
            'smart_suggestions_off': True,
            'auto_upload_off': True,
            'locale': settings.LOCALE,
            'client_device_id': settings.DEVICE_IDENTIFIER
        }

        json_response = self._client.post('/account/register.json', data=register_payload)

        if json_response.get('error') or not json_response.get('result'):
            # TODO: Error handling
            pass

        return User(**json_response.get('result').get('current_user'))

    def delete(self) -> bool:
        """
        Deletes the currently logged in user.
        :return: Boolean describing if the user was successfully deleted.
        """
        json_response = self._client.delete(f'/account/delete')

        return json_response.get('result').get('success') and not json_response.get('error')
