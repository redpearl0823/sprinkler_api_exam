import calendar
from datetime import datetime

from spr_api.listening.NameLookups import Topic, TopicGroup, Theme, KeywordList, Country, CustomField, \
    CustomMeasurement, ListeningMediaType
from spr_api.reporting.Request import ReportingRequest
from spr_api.reporting.Response import ReportingResponse, StreamResponse
from spr_api.spr_app import SprApp

SENTIMENT_MAP = {'Positive': 'pos',
                 'Negative': 'neg',
                 'Neutral': 'neu',
                 'Uncategorized': 'uncat'}

ASSET_CLASS_TO_CUSTOM_PROPERTY_DIMENSION_MAP = {'Message': 'INBOUND_CUSTOM_PROPERTY',
                                                'Topic': 'TOPIC_CUSTOM_PROPERTY',
                                                'Theme': 'THEME_CUSTOM_PROPERTY',
                                                'Product': 'PRODUCT_CUSTOM_PROPERTY',
                                                'Location': 'LOCATION_CUSTOM_PROPERTY'}


def not_empty(values):
    if not values:
        raise RuntimeError("Please pass some values")


class Query(ReportingRequest):

    def __init__(self, app: SprApp, start_time: str, end_time: str, page_size: int = 100):
        """
        Creates a Listening Query, user can add additional filters, groupbys, projections to the query before fetching
        results.
        Parameters
        ----------
        app : an instance of SprApp for authentication
        start_time : start_time for the query, in ISO 8601 format
        end_time : end_time for the query, in ISO 8601 format
        page_size : no of documents to be returned in one fetch call
        """
        start_time = self.get_millis_from_iso_date(start_time)
        end_time = self.get_millis_from_iso_date(end_time)
        super().__init__(app, start_time, end_time, page_size)
        self.query_filters = []
        self.query_groups = []
        self.query_projections = []
        self.date_format_columns = []
        self.include_request = False

    @staticmethod
    def get_millis_from_iso_date(iso_format_string):
        return calendar.timegm(datetime.fromisoformat(iso_format_string).utctimetuple()) * 1000

    def with_topics(self, topics):
        self.__topic_filter(topics, "IN")
        return self

    def excluding_topics(self, topics):
        self.__topic_filter(topics, "NIN")
        return self

    def __topic_filter(self, topics, filter_type="IN"):
        not_empty(topics)
        ids = Topic(self.lookup_api).get_id_from_names(topics)
        self.query_filters.append({"key": "topic", "operator": filter_type, "values": topics})
        self.with_filter_dimension("TOPIC_IDS", filter_type, ids)
        return self

    def with_topic_groups(self, topic_groups):
        self.__topic_group_filter(topic_groups, "IN")
        return self

    def excluding_topic_groups(self, topic_groups):
        self.__topic_group_filter(topic_groups, "NIN")
        return self

    def __topic_group_filter(self, topic_groups, filter_type="IN"):
        not_empty(topic_groups)
        ids = TopicGroup(self.lookup_api).get_id_from_names(topic_groups)
        self.query_filters.append({"key": "topic_group", "operator": filter_type, "values": topic_groups})
        self.with_filter_dimension("TOPIC_GROUP_IDS", filter_type, ids)

    def with_themes(self, themes):
        self.__theme_filter(themes, "IN")
        return self

    def excluding_themes(self, themes):
        self.__theme_filter(themes, "NIN")
        return self

    def __theme_filter(self, themes, filter_type="IN"):
        not_empty(themes)
        ids = Theme(self.lookup_api).get_id_from_names(themes)
        self.query_filters.append({"key": "theme", "operator": filter_type, "values": themes})
        self.with_filter_dimension("LST_THEME", filter_type, ids)
        return self

    def with_keyword_lists(self, keyword_lists):
        self.__keyword_list_filter(keyword_lists, "IN")
        return self

    def excluding_keyword_lists(self, keyword_lists):
        self.__keyword_list_filter(keyword_lists, "NIN")
        return self

    def __keyword_list_filter(self, keyword_lists, filter_type="IN"):
        not_empty(keyword_lists)
        ids = KeywordList(self.lookup_api).get_id_from_names(keyword_lists)
        self.query_filters.append({"key": "keyword_list", "operator": filter_type, "values": keyword_lists})
        self.with_filter_dimension("LST_KEYWORD_LIST", filter_type, ids)
        return self

    def with_topic_tags(self, topic_tags):
        self.__entity_tag_filter(topic_tags, "TOPIC_TAGS", "IN")
        return self

    def excluding_topic_tags(self, topic_tags):
        self.__entity_tag_filter(topic_tags, "TOPIC_TAGS", "NIN")
        return self

    def with_theme_tags(self, topic_tags):
        self.__entity_tag_filter(topic_tags, "LST_THEME_TAG", "IN")
        return self

    def excluding_theme_tags(self, topic_tags):
        self.__entity_tag_filter(topic_tags, "LST_THEME_TAG", "NIN")
        return self

    def __entity_tag_filter(self, tags, filter_name, filter_type="IN"):
        not_empty(tags)
        if not isinstance(filter_name, str):
            raise RuntimeError("Please pass valid filter name in string")
        self.query_filters.append({"key": filter_name.lower(), "operator": filter_type, "values": tags})
        self.with_filter_dimension(filter_name, filter_type, tags)
        return self

    def with_countries(self, countries):
        self.__country_filter(countries, "IN")
        return self

    def excluding_countries(self, countries):
        self.__country_filter(countries, "NIN")
        return self

    def __country_filter(self, countries, filter_type="IN"):
        not_empty(countries)
        ids = Country(self.lookup_api).get_id_from_names(countries)
        self.query_filters.append({"key": "country", "operator": filter_type, "values": countries})
        self.with_filter_dimension("COUNTRY", filter_type, ids)
        return self

    def with_country_exists(self, value="true"):
        self.query_filters.append({"key": "country", "operator": "EXISTS", "values": value})
        self.with_filter_dimension("COUNTRY", "EXISTS", [value])
        return self

    def with_permalinks(self, links):
        not_empty(links)
        self.query_filters.append({"key": "links", "operator": "IN", "values": links})
        self.with_filter_dimension("DOMAINS", "IN", links)
        return self

    def with_sources(self, sources):
        self.__source_filter(sources, "IN")
        return self

    def excluding_sources(self, sources):
        self.__source_filter(sources, "NIN")
        return self

    def __source_filter(self, sources, filter_type="IN"):
        not_empty(sources)
        ids = ListeningMediaType(self.lookup_api).get_id_from_names(sources)
        self.query_filters.append({"key": "sources", "operator": filter_type, "values": sources})
        self.with_filter_dimension("LISTENING_MEDIA_TYPE", filter_type, ids)
        return self

    def with_sentiments(self, sentiments):
        self.__sentiment_filter(sentiments, "IN")
        return self

    def excluding_sentiments(self, sentiments):
        self.__sentiment_filter(sentiments, "NIN")
        return self

    def __sentiment_filter(self, sentiments, filter_type="IN"):
        not_empty(sentiments)
        ids = []
        for sentiment in sentiments:
            key = SENTIMENT_MAP.get(sentiment)
            if key:
                ids.append(key)
            else:
                raise RuntimeError(
                    "Unknown value. Acceptable values are: [ Positive, Negative, Neutral, Uncategorized ]")
        self.query_filters.append({"key": "sentiment", "operator": filter_type, "values": sentiments})
        self.with_filter_dimension("SEM_SENTIMENT", filter_type, ids)
        return self

    def with_custom_field(self, custom_field_name, custom_field_values, asset_class="Message"):
        self.__custom_field_filter(custom_field_name, custom_field_values, asset_class, "IN")
        return self

    def excluding_custom_field(self, custom_field_name, custom_field_values, asset_class="Message"):
        self.__custom_field_filter(custom_field_name, custom_field_values, asset_class, "NIN")
        return self

    def with_custom_field_exists(self, custom_field_name, value="true", asset_class="Message"):
        self.__custom_field_filter(custom_field_name, [value], asset_class, "EXISTS")
        return self

    def __custom_field_filter(self, custom_field_name, custom_field_values, asset_class="Message", filter_type="IN"):
        not_empty(custom_field_name)
        not_empty(custom_field_values)
        custom_property_dimension = ASSET_CLASS_TO_CUSTOM_PROPERTY_DIMENSION_MAP.get(asset_class)
        custom_field_id = CustomField(self.lookup_api).get_id_from_name(custom_field_name)
        self.query_filters.append({"key": custom_field_id, "operator": filter_type, "values": custom_field_values})
        self.with_filter_dimension(custom_property_dimension, filter_type, custom_field_values,
                                   {'contentType': 'DB_FILTER', 'fieldName': custom_field_id,
                                    'reportName': 'SPRINKSIGHTS', 'srcType': 'CUSTOM'})
        return self

    def with_spam_category(self, categories):
        self.__spam_category_filter(categories, "IN")
        return self

    def excluding_spam_category(self, categories):
        self.__spam_category_filter(categories, "NIN")
        return self

    def __spam_category_filter(self, categories, filter_type):
        not_empty(categories)
        self.query_filters.append({"key": "spam category", "operator": filter_type, "values": categories})
        self.with_filter_dimension("SPAM_CAT", filter_type, categories)
        return self

    def group_by_topic(self, heading="Topics"):
        self.query_groups.append({"key": "topic", "heading": heading})
        self.group_by_dimension(heading, "TOPIC_IDS")
        return self

    def group_by_theme(self, heading="Themes"):
        self.query_groups.append({"key": "theme", "heading": heading})
        self.group_by_dimension(heading, "LST_THEME")
        return self

    def group_by_topic_tag(self, heading, topic_tag):
        if not isinstance(topic_tag, str):
            raise RuntimeError("Please pass valid topic tag name in string")
        field_name = "SPECIFIC_TOPIC_TAG_" + topic_tag
        self.query_groups.append({"key": field_name, "heading": heading})
        self.group_by_dimension(heading, field_name)
        return self

    def group_by_theme_tag(self, heading, theme_tag):
        if not isinstance(theme_tag, str):
            raise RuntimeError("Please pass valid theme tag name in string")
        field_name = "SPECIFIC_THEME_TAG_" + theme_tag
        self.query_groups.append({"key": field_name, "heading": heading})
        self.group_by_dimension(heading, field_name)
        return self

    def group_by_sentiment(self, heading="Sentiment"):
        self.query_groups.append({"key": "sentiment", "heading": heading})
        self.group_by_dimension(heading, "SEM_SENTIMENT")
        return self

    def group_by_day_of_week(self, heading="Day Of Week"):
        self.query_groups.append({"key": "day_of_week", "heading": heading})
        self.group_by_dimension(heading, "DAY_OF_WEEK")
        return self

    def group_by_time_of_day(self, heading="Time Of Day"):
        self.query_groups.append({"key": "time_of_day", "heading": heading})
        self.group_by_dimension(heading, "TIME_OF_DAY")
        return self

    def group_by_created_hour(self, heading="Hour", format="%Y-%m-%d %H:%M"):
        self.date_format_columns.append((len(self.query_groups), format))
        self.query_groups.append({"key": "created_hour", "heading": heading})
        self.group_by_dimension(heading, "SN_CREATED_TIME", "DATE_HISTOGRAM", {'interval': '1h'})
        return self

    def group_by_created_date(self, heading="Date", format="%Y-%m-%d"):
        self.date_format_columns.append((len(self.query_groups), format))
        self.query_groups.append({"key": "created_date", "heading": heading})
        self.group_by_dimension(heading, "SN_CREATED_TIME", "DATE_HISTOGRAM", {'interval': '1d'})
        return self

    def group_by_source(self, heading="Source"):
        self.query_groups.append({"key": "source", "heading": heading})
        self.group_by_dimension(heading, "LISTENING_MEDIA_TYPE")
        return self

    def group_by_country(self, heading="Country"):
        self.query_groups.append({"key": "country", "heading": heading})
        self.group_by_dimension(heading, "COUNTRY")
        return self

    def group_by_hashtag(self, heading="Hashtags"):
        self.query_groups.append({"key": "hashtag", "heading": heading})
        self.group_by_dimension(heading, "HASHTAGS")
        return self

    def group_by_domain(self, heading="Domain"):
        self.query_groups.append({"key": "domain", "heading": heading})
        self.group_by_dimension(heading, "DOMAINS")
        return self

    def project_mentions(self, heading, aggregate_function="SUM"):
        self.query_projections.append({"key": "mentions", "heading": heading})
        self.project_field(heading, "MENTIONS_COUNT", aggregate_function)
        return self

    def project_custom_measurement(self, heading, measurement_name, aggregate_function="SUM"):
        id = CustomMeasurement(self.lookup_api).get_id_from_name(measurement_name)
        self.query_projections.append({"key": id, "heading": heading})
        self.project_field(heading, id, aggregate_function)
        return self

    def with_request(self):
        self.include_request = True
        return self

    def fetch(self):
        payload = {
            "reportingEngine": "LISTENING",
            "report": "SPRINKSIGHTS",
            "startTime": self.start_time,
            "endTime": self.end_time,
            "timeZone": "UTC",
            "pageSize": self.page_size,
            "jsonResponse": self.json_response,
            "groupBys": [group_by.asdict() for group_by in self.group_bys],
            "projections": [projection.asdict() for projection in self.projections],
            "filters": [filter.asdict() for filter in self.filters],
            "sorts": [sort.asdict() for sort in self.sorts],
            "additional": self.additional
        }
        request = {
            "filters": self.query_filters,
            "groups": self.query_groups,
            "projections": self.query_projections,
            "page_size": self.page_size
        }
        return ReportingResponse(self.app, request, payload, self.date_format_columns, self.include_request)

    def fetch_all_with_time_groups(self):
        if not self.group_bys:
            raise RuntimeError("fetch_all_date_groups only works with groups involving data or time, "
                               "eg: group_by_created_date, group_by_created_hour")
        group_by = [group_by.asdict() for group_by in self.group_bys]
        time_group_exists = False
        for group in group_by:
            if 'dimensionName' in group:
                if group['dimensionName'] == 'SN_CREATED_TIME':
                    time_group_exists = True
                    break
        if not time_group_exists:
            raise RuntimeError("fetch_all_date_groups only works with groups involving data or time, eg: group_by_created_date, "
                               "group_by_created_hour")
        response = self.fetch()
        overall_response = {'rows': [], 'headings': []}

        for res in response:
            if 'rows' in res:
                overall_response['rows'].extend(res['rows'])
            if 'headings' in res and len(overall_response['headings']) == 0:
                overall_response['headings'].extend(res['headings'])

        if self.include_request:
            overall_response['request'] = response.request
        return overall_response

    def fetch_mentions(self):
        if self.projections:
            raise RuntimeError("fetchMentions does not support projections")
        elif self.group_bys:
            raise RuntimeError("fetchMentions does not support groups")
        self.group_by_dimension("Message Id", "ES_MESSAGE_ID")
        self.project_mentions("Mentions")
        self.additional["STREAM"] = True
        payload = {
            "reportingEngine": "LISTENING",
            "report": "SPRINKSIGHTS",
            "startTime": self.start_time,
            "endTime": self.end_time,
            "timeZone": "UTC",
            "pageSize": self.page_size,
            "jsonResponse": self.json_response,
            "groupBys": [group_by.asdict() for group_by in self.group_bys],
            "projections": [projection.asdict() for projection in self.projections],
            "filters": [filter.asdict() for filter in self.filters],
            "sorts": [sort.asdict() for sort in self.sorts],
            "additional": self.additional
        }
        return StreamResponse(self.app, payload)
