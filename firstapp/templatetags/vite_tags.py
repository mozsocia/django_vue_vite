
from django import template
import os
import json
from django.templatetags.static import static
from django.conf import settings
from django.utils.safestring import mark_safe
from pathlib import Path
from pprint import pprint

register = template.Library()

@register.simple_tag
def render_vite_dev_scripts():
    scripts = []

    if getattr(settings, 'DEV_ENV', False):
        port = getattr(settings, 'VITE_DEV_PORT', 3080)  # Default port is 3080

        # Script tag for Vite client
        scripts.append(f'<script type="module" src="http://localhost:{port}/@vite/client"></script>')

        # Script tag for your main.ts file
        scripts.append(f'<script type="module" src="http://localhost:{port}/src/main.js"></script>')

    return mark_safe('\n'.join(scripts))


@register.simple_tag
def render_vite_assets(entry_name='index.html'):
    if getattr(settings, 'DEV_ENV', True):
        return ''

    manifest_path = os.path.join(settings.BASE_DIR, settings.VITE_APP_STATIC_DIR, '.vite/manifest.json')

    try:
        with open(manifest_path, 'r') as manifest_file:
            manifest_data = json.load(manifest_file)
    except Exception as e:
        # Code to handle other types of exceptions
        print(f"An error occurred: {e}")


    if entry_name in manifest_data:
        entry = manifest_data[entry_name]
        js_file = entry.get('file', '')
        css_files = entry.get('css', [])

        js_tag = f'<script type="module" src="/{settings.VITE_APP_STATIC_DIR}/{js_file}"></script>' if js_file else ''

        css_tags = [f'<link rel="stylesheet" href="/{settings.VITE_APP_STATIC_DIR}/{css_file}">' for css_file in css_files]

        pprint('\n'.join([js_tag] + css_tags))

        return mark_safe('\n'.join([js_tag] + css_tags))

    return ''



    """
    Template tag to render a vite bundle.
    Supposed to only be used in production.
    For development, see other files.
    """

    if not getattr(settings, 'DEV_ENV', True):

        manifest = load_json_from_dist()
        files = manifest.keys()

        imports_files = "".join(
            [
                f'<script type="module" src="{settings.VITE_APP_STATIC_DIR}/{manifest[file]["file"]}"></script>'
                for file in files
                if manifest[file].get("file", "")
            ]
            + [
                f"""<link rel="stylesheet" type="text/css" href="{settings.VITE_APP_STATIC_DIR}/{css}" />"""
                for file in files
                for css in manifest[file].get("css", [])
            ]
        )

        return mark_safe(
            f"""<script type="module" src="{settings.VITE_APP_STATIC_DIR}/{manifest['index.html']['file']}"></script>
            <link rel="stylesheet" type="text/css" href="{settings.VITE_APP_STATIC_DIR}/{manifest['index.html']['css'][0]}" />
            {imports_files}"""
        )
    else :
        return ""