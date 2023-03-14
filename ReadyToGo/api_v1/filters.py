def active_only_filter(queryset, request):
    params = request.GET
    active_only = params.get('active_only')
    if not active_only:
        return queryset
    if active_only.lower() == 'true':
        return queryset.filter(is_active=True)
    return queryset
