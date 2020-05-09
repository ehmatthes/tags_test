"""Make a bunch of sample tags."""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tags_test.settings')

import django
django.setup()


from random import choice
from django.core import management

from faker import Faker

from tags.models import Tag


# Flush data.
management.call_command('flush', '--noinput')
print("Flushed db.")

faker = Faker()

NUM_TAGS = 300

all_tags = []
for tag_num in range(NUM_TAGS):
    new_tag = Tag(text=f"{faker.word()} {tag_num}")
    new_tag.save()
    all_tags.append(new_tag)

print(f"Saved {NUM_TAGS} new tags.")

# Assign last 80% tags one of the first 20% as parents.
parent_tags = all_tags[:NUM_TAGS//3]
child_tags = all_tags[NUM_TAGS//5:]
# assert len(parent_tags) + len(child_tags) == NUM_TAGS
# for ct in child_tags:
#     assert ct not in parent_tags

print('parent_tags:', parent_tags)
print('child tags:', child_tags)

for child_tag in child_tags:
    parent_tag = choice(parent_tags)
    child_tag.parent = parent_tag
    try:
        child_tag.save()
    except Exception as e:
        print('Exception: ct, pt', child_tag, parent_tag)
        print(e)
        print('done')

print("Assigned parents to most tags.")

Tag.objects.rebuild()
print("Rebuilt tree.")