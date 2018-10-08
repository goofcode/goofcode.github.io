import sys
import os
import shutil
import re
from datetime import time, date

posts_path = '_posts'
image_path = os.path.join('assets', 'img')

new_posts = []

for file in os.listdir(posts_path):
    # if new post (has no date on file name)
    if re.search('^((?!(\d{4}(-\d\d){2})).)*\.md$', file) is not None:
        new_posts.append(file)

if len(new_posts) == 0:
    print("no new post found")

for new_post in new_posts:

    post_filename = new_post
    post_path = os.path.join(posts_path, post_filename)
    post_title = post_filename.replace('.md', '')

    print("new post found: ", post_title)

    # move images to assets/img
    post_img_path = shutil.move(os.path.join("_posts", post_title), image_path)
    print("[*] image files moved to", post_img_path)

    # read whole post file
    with open(post_path, 'r') as f:
        post_file = f.read()

    # TODO remove in-post title
    # TODO remove in-post tags

    # find all image tags
    img_tags = re.findall('!\[\]\(.*\)', post_file)

    # change image path
    for img_tag in img_tags:
        new_path = os.path.join(image_path, img_tag[4:-1])
        new_tag = '![](/' + new_path + ')'
        post_file = post_file.replace(img_tag, new_tag)
    print("[*] image path adjusted")

    # generate jekyll "front matter"
    front_matter = '---\n' \
                   'title: {}\n' \
                   '---\n'.format(post_title)
    post_file = front_matter + post_file
    print("[*] jekyll front matter generated")

    # write post file
    with open(post_path, 'w') as f:
        f.write(post_file)

    # rename post to jekyll post file format
    format_today = date.today().strftime("%Y %m %d ")
    jekyll_format_name = (format_today + post_title).replace(" ", "-") + '.md'
    new_post_path = os.path.join(posts_path, jekyll_format_name)
    os.rename(post_path, new_post_path)
    print("[*] post file renamed to follow jekyll post naming")
