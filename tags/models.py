from django.db import models

import auto_prefetch

from mptt.models import MPTTModel, TreeForeignKey, TreeManager


class Tag(MPTTModel, auto_prefetch.Model):

    text = models.CharField(max_length=100)
    parent = auto_prefetch.ForeignKey('self', on_delete=models.CASCADE, null=True,
            blank=True, related_name='children')


    def __str__(self):
        return self.text

    def all_siblings_leaf(self, all_tags):
        """Return true if all siblings, including self, are leaf nodes.
        """
        # siblings = self.get_siblings(include_self=True)
        if self.parent is None:
            siblings = [t for t in all_tags if t.parent is None]
        else:
            siblings = [t for t in all_tags if t.parent == self.parent]
            
        return all([s.is_leaf_node() for s in siblings])


    class MPTTMeta:
        order_insertion_by = ['text']

    class MyManager(TreeManager, auto_prefetch.Manager):
        pass

    objects = MyManager()