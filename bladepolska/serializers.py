from django.db.models.query import RawQuerySet


class Serializer(object):
    def __init__(self, request):
        self.request = request

    def set_qs(self, qs):
        self.qs = qs

    def prepare_qs(self):
        return self.queryset_copy().values()

    def serialize_qs(self, list_qs):
        return list_qs

    def queryset_copy(self):
        return self.qs.all()

    def serialize(self):
        qs = list(self.prepare_qs())
        return self.serialize_qs(qs)


class PaginationFastSerializer(Serializer):
    def __init__(self, request):
        self.request = request
        offset = self.request.GET.get('offset', 0)
        try:
            offset = int(offset)
            self.offset = max(offset, 0)
        except ValueError:
            self.offset = 0

        limit = self.request.GET.get('limit', 15)
        try:
            limit = int(limit)
            self.limit = min(limit, 15)
        except ValueError:
            self.limit = 15

    def prepare_qs(self):
        self.wrapped_serializer = self.__class__.object_serializer_class(self.request)
        self.wrapped_serializer.set_qs(self.queryset_copy())
        prepared_qs = self.wrapped_serializer.prepare_qs()

        if isinstance(prepared_qs, RawQuerySet):
            prepared_qs.query.sql += " OFFSET %d LIMIT %d" % (self.offset, self.limit + 1)
            paginated_results_plus_one_object = list(prepared_qs)
        elif isinstance(prepared_qs, list):
            paginated_results_plus_one_object = prepared_qs[self.offset:self.offset + self.limit + 1]
        else:
            paginated_results_plus_one_object = list(prepared_qs[self.offset:self.offset + self.limit + 1])

        if len(paginated_results_plus_one_object) > self.limit:
            there_is_more = True
            paginated_results = paginated_results_plus_one_object[:-1]
        else:
            there_is_more = False
            paginated_results = paginated_results_plus_one_object

        return [{
            'there_is_more': there_is_more,
            'objects': self.wrapped_serializer.serialize_qs(paginated_results)
        }]

    def serialize_qs(self, list_qs):
        return list_qs[0]
