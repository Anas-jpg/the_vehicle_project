from rest_framework.throttling import SimpleRateThrottle


class BrandThrottle(SimpleRateThrottle):
    scope = 'brand_throttle'

    def get_cache_key(self, request, view):

        if request.user.is_authenticated:
            print(f"{self.scope}:{request.user.pk}")
            return f"{self.scope}:{request.user.pk}"
        else:
            print(f"{self.scope}:{request.META['REMOTE_ADDR']}")
            return f"{self.scope}:{request.META['REMOTE_ADDR']}"

