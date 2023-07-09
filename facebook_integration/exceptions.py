

class FacebookAPIErrorException(Exception):
    def __init__(self, message=None, response=None, *args, **kwargs):
        self.response = response
        self.message = message
        super().__init__(*args, **kwargs)


class AddCatalogItemFailed(FacebookAPIErrorException):
    pass


class SyncBetweenMerchantAndFacebookFailed(FacebookAPIErrorException):
    pass


class DeleteCatalogItemFailed(FacebookAPIErrorException):
    pass


class UpdateCatalogItemFailed(FacebookAPIErrorException):
    pass


class FacebookIntegrationIsNotComplete(FacebookAPIErrorException):
    pass


class BulkProductAddFailed(FacebookAPIErrorException):
    pass
