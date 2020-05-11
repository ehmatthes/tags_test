This is a simple project for testing whether the [django-auto-prefetch](https://pypi.org/project/django-auto-prefetch/) package improves the efficiency of queries for a project using [django-mptt](https://django-mptt.readthedocs.io/en/latest/).

This is a very specific use case. I have a project that uses tags, which exist in a tree hierarchy. I want to treat nodes where all siblings are leaf nodes differently, so I implemented an `all_sibings_leaf()` method on the `Tag` model. This uses the `get_siblings()` method, which is supplied by mptt. But each call to this method costs one trip to the db, so on a page with a large number of tags, this is a lot of queries. I was able to bring this down to 1 query by fetching siblings myself through each node's parent, after using `select_related()` in the original query which I pass to `all_siblings_leaf()`.

## Prediction

I did not have high hopes that `django-auto-prefetch` would help, because the querying that's being done is happening through a number of calls, and using another library. However, that was part of what made me curious - if `django-auto-prefetch` could follow all of these lines and do the proper optimization, that would be quite impressive and a strong argument for using the library. I also haven't read the documentation closely for when a queryset is converted to SQL, so I don't have a strong basis for understanding how difficult it is for an optimizer to improve the efficiency of a given query.

## Results

I made a demo project with a single Tag model that just inherits from MPTTModel initially. I generated 200 fake tags, with various parent relationships. I wrote a model method `all_siblings_leaf()`, which uses the method `get_siblings()` that MPTT provides. The MPTT `get_siblings()` method does a query of all tags, with a filter that references the parent of the given tag if it exists.

I made a single page that shows all tags, and shows the results of the `all_siblings_leaf()` method. I used debug toolbar to see how many queries are being run to render the page. Here's what I found:

- In the first pass, without `django-auto-prefetch`, the page used 201 queries. This was not surprising; the cost of `all_siblings_leaf()` is one query per tag.
In the next pass, I installed `django-auto-prefetch` and integrated `django-auto-prefetch` into the Tag model. I destroyed the db and migrations, and rebuilt the db and sample data. When I reloaded the page, it was still at 201 queries.
- I rewrote `all_siblings_leaf()` to do my own siblings lookup. This way I'm explicitly doing a query that uses the parent tag. There was a slight change; the page took 158 queries. I think this is because the root nodes don't require a query when I get the siblings myself.
- I added `select_related('parent')` to the tag query in the view function. This dropped the query count to 1.

I don't think `django-auto-prefetch` did anything in this demo. I don't think it was able to pick up what was happening in the `get_siblings()` call I was originally using. Later on, I don't think it was able to pick up what I was doing when I built the set of siblings myself either.

## Running the demo

- Download this repo.
- Create a virtual environment, install requirements from requirement.txt.
- Run `python manage.py migrate`.
- Run `git checkout c49213`, and then run `python make_sample_tags.py`.
  - This will generate 200 tags. Start the dev server, and visit the home page. You'll see 1 query on the home page, because this page is just using mptt's built-in recursetree tag.
  - Click the link to *All tags with all_siblings_leaf*. You'll see 201 queries for this page, with the call to `all_siblings_leaf()`, which uses the default `get_siblings()` from mptt.
  - This commit uses `auto_prefect.Model`.
- Run `git checkout 5cf65f`. Reload the all_siblings_leaf page, and you'll see it's down to 160 queries.
  - This uses my own code to get siblings in all_siblings_leaf. There are no queries for the root nodes, so there are fewer queries.
- Run `git checkout 098b7c`. Reload the page, and you'll see it's down to 1 query.
  - The query to get the tags has `select_related('parent')` now, and this queryset is passed to `all_siblings_leaf()`.

This was a really interesting exercise, and I'm happy to answer any questions about what you see here.
