import requests
from django.core.cache import cache
from rest_framework import serializers
from django.conf import settings

CACHE_KEY = "catapi_breeds"

def _fetch_breeds_from_api():
    resp = requests.get(settings.CATAPI_URL, timeout=5)
    resp.raise_for_status()
    return [b["id"] for b in resp.json()]

def validate_breed_id(breed_id: str) -> str:
    CACHE_TTL = 60*5  # 5 minutes
    breeds = cache.get(CACHE_KEY)
    if not breeds:
        breeds = _fetch_breeds_from_api()
        cache.set(CACHE_KEY, breeds, CACHE_TTL)

    if breed_id in breeds:
        return breed_id

    fresh = _fetch_breeds_from_api()
    cache.set(CACHE_KEY, fresh, CACHE_TTL)
    if breed_id not in fresh:
        raise serializers.ValidationError(f"Breed id '{breed_id}' is invalid (TheCatAPI).")

    return breed_id
