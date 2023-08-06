from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from docusign_esign import ApiClient, EnvelopesApi, TemplatesApi

from buildblock.decorators import memoized_classproperty

_LIST_STATUS_CHANGE_DATE_RANGE = relativedelta(months=6)


class DocusignService:
    account_id = settings.DOCUSIGN_ACCOUNT_ID

    @memoized_classproperty
    def _client(cls):
        api_client = ApiClient()
        api_client.host = settings.DOCUSIGN_BASE_PATH
        api_client.set_default_header("Authorization", "Bearer " + settings.DOCUSIGN_ACCESS_TOKEN)
        return api_client

    @memoized_classproperty
    def _envelopes_api(cls):
        return EnvelopesApi(cls._client)

    @memoized_classproperty
    def _templates_api(cls):
        return TemplatesApi(cls._client)

    @classmethod
    def envelope_list_status_changes(cls):
        # https://developers.docusign.com/esign-rest-api/reference/Envelopes/Envelopes/listStatusChanges
        from_date = (datetime.utcnow() - _LIST_STATUS_CHANGE_DATE_RANGE).isoformat()
        return cls._envelopes_api.list_status_changes(cls.account_id, from_date=from_date)

    @classmethod
    def create_envelope(cls, envelope_definition):
        return cls._envelopes_api.create_envelope(cls.account_id, envelope_definition=envelope_definition)

    @classmethod
    def create_recipient_view(cls, envelope_id, user_name, user_email, user_id, return_url):
        # https://developers.docusign.com/esign-rest-api/reference/Envelopes/EnvelopeViews/createRecipient
        request = {
            "email": user_email,
            "userName": user_name,
            "returnUrl": return_url,
            "clientUserId": user_id,
            "AuthenticationMethod": "None",
        }
        results = cls._envelopes_api.create_recipient_view(cls.account_id, envelope_id, recipient_view_request=request)
        return results.url

    @classmethod
    def get_document(cls, envelope_id):
        # https://developers.docusign.com/esign-rest-api/v2/reference/Envelopes/EnvelopeDocuments/get
        return cls._envelopes_api.get_document(cls.account_id, "combined", envelope_id)

    @classmethod
    def get_envelope(cls, envelope_id):
        # https://developers.docusign.com/esign-rest-api/reference/Envelopes/Envelopes/get
        return cls._envelopes_api.get_envelope(cls.account_id, envelope_id)

    @classmethod
    def get_template_list(cls, envelope_id):
        # https://developers.docusign.com/esign-rest-api/reference/Templates/Templates/list
        return cls._templates_api.list_custom_fields(cls.account_id, envelope_id)
