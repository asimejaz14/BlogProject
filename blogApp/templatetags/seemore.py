from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
import re

register = template.Library()

seemore_showscript = ''.join([
    "this.parentNode.style.display='none';",
    "this.parentNode.parentNode.getElementsByClassName('more')[0].style.display='inline';",
    "return false;",
])


@register.filter
def seemore(txt, showwords=10):
    global seemore_showscript
    words = re.split(r' ', escape(txt))

    if len(words) <= showwords:
        return txt

    # wrap the more part
    words.insert(showwords, '<span class="more" style="display:none;">')
    words.append('</span>')

    # insert the seemore part
    words.insert(showwords, '<span class="seemore">... <a href="#" onclick="')
    words.insert(showwords + 1, seemore_showscript)
    words.insert(showwords + 2, '">see more</a>')
    words.insert(showwords + 3, '</span>')

    # Wrap with <p>
    words.insert(0, '<p>')
    words.append('</p>')

    return mark_safe(' '.join(words))


seemore.is_safe = True
