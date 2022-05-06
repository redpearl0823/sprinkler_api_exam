from spr_api.lookup_api import LookupApi, LookupRequest


class Theme:
    def __init__(self, lookupApi: LookupApi):
        self.lookupApi = lookupApi

    def get_id_from_names(self, names):
        lookup_request = LookupRequest()
        lookup_request.type("LST_THEME_NAME")
        lookup_request.add_keys(names)
        response_dict = self.lookupApi.lookup(lookup_request)
        if len(response_dict) != len(names):
            raise RuntimeError(
                "Could not resolve all Themes for names. Missing names : " + str(names - response_dict.keys()))
        return list(response_dict.values())


class Topic:

    def __init__(self, lookupApi: LookupApi):
        self.lookupApi = lookupApi

    def get_id_from_names(self, names):
        lookup_request = LookupRequest()
        lookup_request.type("LST_TOPIC_NAME")
        lookup_request.add_keys(names)
        response_dict = self.lookupApi.lookup(lookup_request)
        if len(response_dict) != len(names):
            raise RuntimeError(
                "Could not resolve all Topics for names. Missing names : " + str(names - response_dict.keys()))
        return list(response_dict.values())


class TopicGroup:

    def __init__(self, lookupApi: LookupApi):
        self.lookupApi = lookupApi

    def get_id_from_names(self, names):
        lookup_request = LookupRequest()
        lookup_request.type("LST_TOPIC_GROUP_NAME")
        lookup_request.add_keys(names)
        response_dict = self.lookupApi.lookup(lookup_request)
        if len(response_dict) != len(names):
            raise RuntimeError(
                "Could not resolve all Topic Groups for names. Missing names : " + str(names - response_dict.keys()))
        return list(response_dict.values())


class KeywordList:

    def __init__(self, lookupApi: LookupApi):
        self.lookupApi = lookupApi

    def get_id_from_names(self, names):
        lookup_request = LookupRequest()
        lookup_request.type("LST_KEYWORD_LIST_NAME")
        lookup_request.add_keys(names)
        response_dict = self.lookupApi.lookup(lookup_request)
        if len(response_dict) != len(names):
            raise RuntimeError(
                "Could not resolve all Keyword Groups for names. Missing names : " + str(names - response_dict.keys()))
        return list(response_dict.values())


class Country:

    def __init__(self, lookupApi: LookupApi):
        self.lookupApi = lookupApi

    def get_id_from_names(self, names):
        lookup_request = LookupRequest()
        lookup_request.type("LST_COUNTRY_NAME")
        lookup_request.add_keys(names)
        response_dict = self.lookupApi.lookup(lookup_request)
        if len(response_dict) != len(names):
            raise RuntimeError(
                "Could not resolve all Countries for names. Missing names : " + str(names - response_dict.keys()))
        return list(response_dict.values())


class CustomField:

    def __init__(self, lookupApi: LookupApi):
        self.lookupApi = lookupApi

    def get_id_from_name(self, name):
        lookup_request = LookupRequest()
        lookup_request.type("CUSTOM_FIELD_NAME")
        lookup_request.add_key(name)
        response_dict = self.lookupApi.lookup(lookup_request)
        if len(response_dict) != 1:
            raise RuntimeError("Could not resolve custom field for name: " + name)
        return list(response_dict.values())[0]


class CustomMeasurement:

    def __init__(self, lookupApi: LookupApi):
        self.lookupApi = lookupApi

    def get_id_from_name(self, name):
        lookup_request = LookupRequest()
        lookup_request.type("CUSTOM_METRIC_NAME")
        lookup_request.add_key(name)
        response_dict = self.lookupApi.lookup(lookup_request)
        if len(response_dict) != 1:
            raise RuntimeError("Could not resolve custom measurement for name: " + name)
        return list(response_dict.values())[0]


class ListeningMediaType:

    def __init__(self, lookupApi: LookupApi):
        self.lookupApi = lookupApi

    def get_id_from_names(self, names):
        lookup_request = LookupRequest()
        lookup_request.type("LISTENING_MEDIA_TYPE_NAME")
        lookup_request.add_keys(names)
        response_dict = self.lookupApi.lookup(lookup_request)
        if len(response_dict) != len(names):
            raise RuntimeError(
                "Could not resolve all Sources for names. Missing names : " + str(names - response_dict.keys()))
        return list(response_dict.values())
