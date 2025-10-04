import os
from supabase import create_client
from django.conf import settings

# Use settings.py environment variables
SUPABASE_URL = getattr(settings, "SUPABASE_URL", None)
SUPABASE_KEY = getattr(settings, "SUPABASE_KEY", None)

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and KEY must be set in settings.py or environment variables.")

# Create a Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
