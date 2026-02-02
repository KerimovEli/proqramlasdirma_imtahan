from .models import Tag 
 
def tags_processor(request): 
    return { 
        "navbar_tags": Tag.objects.all().order_by("name") 
    }