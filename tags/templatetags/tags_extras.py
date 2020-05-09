from django import template

register = template.Library()


def all_siblings_leaf(tag, all_tags):
    """Calls tag.all_siblings_leaf() with argument all_tags.
    """
    return tag.all_siblings_leaf(all_tags)

    
register.filter('all_siblings_leaf', all_siblings_leaf)