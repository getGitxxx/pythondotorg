import datetime
import feedparser

from django.template.loader import render_to_string
from django.utils.timezone import utc

from boxes.models import Box
from .models import BlogEntry


def get_all_entries(feed_url):
    """ Retrieve all entries from a feed URL """
    d = feedparser.parse(feed_url)
    entries = []

    for e in d['entries']:
        published = datetime.datetime(*e['updated_parsed'][:7])
        published = published.replace(tzinfo=utc)

        entry = {
            'title': e['title'],
            'summary': e['summary'],
            'pub_date': published,
            'url': e['link'],
        }
        entries.append(entry)

    return entries


def _render_blog_supernav(entry):
    """ Utility to make testing update_blogs management command easier """
    return render_to_string('blogs/supernav.html', {'entry': entry})


def update_blog_supernav():
    """Retrieve latest entry and update blog supernav item """
    latest_entry = BlogEntry.objects.latest()
    rendered_box = _render_blog_supernav(latest_entry)

    box = Box.objects.get(label='supernav-python-blog')
    box.content = rendered_box
    box.save()
