from cachetools import TTLCache

admin_data = {}
user_data = TTLCache(maxsize=3, ttl=7200)
user_contact_data = {}
user_context_data = []