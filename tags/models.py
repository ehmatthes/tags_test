from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Tag(MPTTModel):

    text = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
            blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['text']

    def __str__(self):
        return self.text
