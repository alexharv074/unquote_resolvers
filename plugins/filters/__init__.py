import warnings
from jinja2.ext import Extension
from unquote_resolvers import unquote_resolvers


class FilterModule:
    def filters(self):
        return {"unquote_resolvers": unquote_resolvers}


class CustomFiltersExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        filters = FilterModule().filters()
        for filter in filters:
            if filter in environment.filters:
                warnings.warn("Filter name collision detected changing "
                              "filter name to custom_{0} "
                              "to avoid clobbering".format(filter),
                              RuntimeWarning)
                filters["custom_" + filter] = filters[filter]
                del filters[filter]

        environment.filters.update(filters)
