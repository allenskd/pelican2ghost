"""
Pelican 2 Ghost import
============================

A simple script that will actively generate the Ghost JSON data file for you to import your Pelican
blog posts to Ghost blogging platform

"""

from pelican import signals
from pelican.contents import Article, Page
from pelican.utils import slugify
from bs4 import BeautifulSoup
import time
from pelicanconf import *
import os
import json
import re

def exporter(generator, writer):

    # Container for posts
    container = {}
    data = {}
    posts = []

    # meta info required for ghost
    now = time.time() * 1000
    metablock = {'meta': {'exported_on': now, 'version': '003'}}
    container.update(metablock)

    # Container for categories and tags
    posts_tags_container = []
    cat_container = []


    ghost_json = {}

    for post_id, article in enumerate(generator.articles, start=1):

        content = article._content

        # Report if any bugs, I'm unsure how it will behave for others
        content = content.replace('{filename}', SITEURL)
        metadata = article.metadata if article.metadata else None

        # Remove any unnecessary HTML elements
        title = BeautifulSoup(metadata['title']).get_text()
        created_date = time.mktime(metadata['date'].timetuple()) * 1000
        modified_date = time.mktime(metadata['modified'].timetuple()) * 1000 if 'modified' in metadata else None
        slug = slugify(title)

        post = {
            'id': post_id,
            'title': title,
            'html': content,
            'status': 'published',
            'author_id': 1,
            'slug': slug,
            'created_at': created_date,
            'created_by': 1,
            'published_at': created_date,
            'published_by': 1,

                }
        if modified_date:
            post['updated_at'] = modified_date
            post['updated_by'] = 1

        source_path = article.source_path

        # Taken from Python Markdown
        META_RE = re.compile(r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)', flags=re.IGNORECASE|re.MULTILINE)

        # Retrieve Markdown
        with open(source_path,'r') as raw_file:

            md_content = raw_file.read()

            marked_down = META_RE.sub('',md_content).strip()
            marked_down = marked_down.replace('{filename}', SITEURL)
            post['markdown'] = marked_down

        # Save post
        posts.append(post)

        # Get categories
        if metadata['category']:
            category_name = metadata['category']._name
            category_slug = slugify(category_name)
            category_id = len(cat_container)+1
            category_exists = False


            if len(cat_container) > 1:
                #TODO: Find a better way to do this
                for search_category in cat_container:
                    if search_category['name'] == category_name:
                        category_id = search_category['id']
                        category_name = search_category['name']
                        category_slug = slugify(category_name)
                        category_exists = True


            if False == category_exists:
                category = {
                    'id': category_id,
                    'name': category_name,
                    'slug': category_slug
                }
                cat_container.append(category)
            tagged_post = {'tag_id': category_id, 'post_id': post_id  }
            posts_tags_container.append(tagged_post)

    cwd = os.getcwd()
    ghost_dump_folder = os.path.join(cwd,"ghost_export")

    if not os.path.exists(ghost_dump_folder):
        os.makedirs(ghost_dump_folder)
        print("Pelican2Ghost: Creating folder in: %s" % ghost_dump_folder)

    ghost_data_file = os.path.join(ghost_dump_folder, "pelican2ghost.json")
    data = {
        'data': {

            'posts': posts,
            'tags': cat_container,
            'posts_tags': posts_tags_container
        }
    }

    container.update(data)
    ghost_json.update(container)
    json_output = json.dumps(ghost_json)

    with open(ghost_data_file, "w") as writer:
        writer.write(json_output)

    print("Pelican2Ghost: Finished exporting data to %s" % ghost_data_file)


def register():
    signals.article_writer_finalized.connect(importer)
