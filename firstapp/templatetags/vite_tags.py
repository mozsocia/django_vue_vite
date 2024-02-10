
from django import template
from django.conf import settings

from pathlib import Path
import json
from django import template
from django.utils.safestring import mark_safe

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




def load_json_from_dist(json_filename="manifest.json"):
    manifest_file_path = Path(str(settings.BASE_DIR), "static", "viteapp/.vite", json_filename)
    if not manifest_file_path.exists():
        raise Exception(f"Vite manifest file not found on path: {str(manifest_file_path)}")
    else:
        with open(manifest_file_path, "r") as manifest_file:
            try:
                manifest = json.load(manifest_file)
            except Exception:
                raise Exception(f"Vite manifest file invalid. Maybe your {str(manifest_file_path)} file is empty?")
            else:
                return manifest


@register.simple_tag
def render_vite_bundle():
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