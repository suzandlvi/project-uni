from django.utils.text import slugify


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title, allow_unicode=True)
    instance_class = instance.__class__
    qs = instance_class.objects.filter(slug=slug)
    if qs.exists():
        slug = f'{slug}-{instance.id}'
        return unique_slug_generator(instance, slug)
    return slug
