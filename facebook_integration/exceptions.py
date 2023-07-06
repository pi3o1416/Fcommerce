

class AddCatalogItemFailed(Exception):
    def __init__(self, response, *args, **kwargs):
        self.response = response
        super().__init__(*args, **kwargs)


class SyncBetweenMerchantAndFacebookFailed(Exception):
    def __init__(self, response, *args, **kwargs):
        self.response = response
        super().__init__(*args, **kwargs)


class DeleteCatalogItemFailed(Exception):
    pass


class FacebookIntegrationIsNotComplete(Exception):
    pass
