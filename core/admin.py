from typing import Optional


def admin_get_preview_image_str(url: Optional[str], size: int = 72) -> str:
    if url is None:
        return f"""<div style="height:{size}px;width:{size}px;background-color: #000;background-repeat: no-repeat;background-position: center;background-size:contain;"></div>"""
    return f"""<div style="height:{size}px;width:{size}px;background-color: #000;background-image: url('{url}');background-repeat: no-repeat;background-position: center;background-size:contain;"></div>"""


def admin_alert_protected_link(url: str, button_title: str, message: str) -> str:
    return f"""<script>
if (admin__AlertOpenLink === undefined) {{
    function admin__AlertOpenLink(message, linkUrl) {{
        const ok = confirm(message);
        if (ok) window.location.href = linkUrl;
    }}
}}
</script>
<button class="button" style="padding:8px; margin: 8px;min-width: 80px;" type="button" onclick="admin__AlertOpenLink('{message}', '{url}');"/>{button_title}</button>"""


def admin_button_link(url: str, button_title: str, target: str = "") -> str:
    return f"""<a class="button" style="padding:8px; margin: 8px; min-width: 80px;" href="{url}" target="{target}"/>{button_title}</a>"""


