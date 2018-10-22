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
    post_thumbnail = None
    post_tags = None

    print("new post found: ", post_title)

    # move images to assets/img
    try:
        post_img_path = shutil.move(os.path.join("_posts", post_title), image_path)
        print("[*] image files moved to", post_img_path)
    except FileNotFoundError:
        print("[**] No image directory found: skip moving image")

    # read whole post file
    with open(post_path, 'r') as f:
        post_file = f.read()

    # remove in-post title (assume H1 tag on the top of the file is containing title)
    in_post_titles = re.findall("^# .*\n", post_file)
    post_file = re.sub("^# .*\n", "", post_file)
    print("[*] in-post title removed", in_post_titles)

    # remove in-post tags and save tag
    in_post_tags = re.findall("#\w+", post_file)
    post_file = re.sub("#\w+", "", post_file)
    post_tags = [tag.replace("#", "") for tag in in_post_tags]
    print("[*] in-post tag removed", in_post_tags)

    # find all image tags
    img_tags = re.findall('!\[\]\(.*\)', post_file)

    # change image path
    for idx, img_tag in enumerate(img_tags):
        new_path = os.path.join(image_path, img_tag[4:-1])
        new_tag = '![](/' + new_path + ')'
        post_file = post_file.replace(img_tag, new_tag)
        if idx == 0:
            post_thumbnail = new_path
    print("[*] image path adjusted")

    # generate jekyll "front matter"
    front_matter = '---\n'
    front_matter += 'title: {}\n'.format(post_title)
    front_matter += ('thumbnail: {}\n'.format(post_thumbnail) if (post_thumbnail is not None) else '')
    front_matter += ('tags: [{}]\n'.format(",".join(post_tags)) if (post_tags is not None) else '')
    front_matter += '---\n'
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
