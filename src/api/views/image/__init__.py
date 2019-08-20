import sanic

from .upload import ID
from .download_url import DownloadURL
from .search import Search
from .tags import Tags

def setup_routes(app: sanic.Sanic, prefix: str = '') -> None:
    prefix = prefix.rstrip('/')
    app.add_route(ID.as_view(), f'{prefix}/upload')
    app.add_route(DownloadURL.as_view(), f'{prefix}/download_url/<image_id:string>')
    app.add_route(Search.as_view(), f'{prefix}/search')

