from django.conf import settings

def supabase_config(request):
    """
    Injects Supabase configuration into all template contexts.
    This allows JS in templates to safely read the public Supabase URL and Anon Key.
    """
    return {
        'SUPABASE_URL': getattr(settings, 'SUPABASE_URL', ''),
        'SUPABASE_KEY': getattr(settings, 'SUPABASE_KEY', ''),
    }
