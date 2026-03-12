import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Tag, Project, Article, Event, Video, Certification, Skill, Experience

models = [Tag, Project, Article, Event, Video, Certification, Skill, Experience]

for model in models:
    print(f"Propagating translations for {model.__name__}...")
    items = model.objects.all()
    for item in items:
        updated = False
        # Get translation fields for this model
        # For simplicity, we'll try to guess based on fields ending in _fr
        fields = [f.name for f in model._meta.fields]
        fr_fields = [f for f in fields if f.endswith('_fr')]
        
        for fr_f in fr_fields:
            base_f = fr_f[:-3] # remove _fr
            base_val = getattr(item, base_f)
            fr_val = getattr(item, fr_f)
            
            if base_val and not fr_val:
                setattr(item, fr_f, base_val)
                updated = True
                print(f"  Filled {fr_f} with base value for ID {item.id}")
        
        if updated:
            item.save()

print("Done!")
