from pexpect.screen import unicode

from repository.ext.db.tags import tags_list


def tag_news(title, html_content):
    tags = []

    content = unicode(f"{title} {html_content}".lower())

    for tag in tags_list:
        if any(unicode(word.lower()) in content for word in tag["keywords"]):
            tags.append(tag["name"])

    return tags
