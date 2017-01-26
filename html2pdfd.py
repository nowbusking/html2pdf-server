#!/usr/bin/env python3
import argparse
import io
import json

from wand.color import Color
from wand.image import Image
from waitress import serve
from weasyprint import HTML
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

__all__ = 'app',


SUPPORTED_TYPES = {
    'application/pdf': lambda html, buffer: html.write_pdf(buffer),
    'image/png': lambda html, buffer: html.write_png(buffer),
    'image/jpeg': lambda html, buffer: render_to_jpeg(html, buffer),
}

MAX_HTML_SIZE = 1024 * 1024 * 50  # 50MiB


def render_to_jpeg(html: HTML, buffer: io.BytesIO):
    png_buffer = io.BytesIO()
    html.write_png(png_buffer)
    png_buffer.seek(0)
    with Image(file=png_buffer) as image:
        image.background_color = Color('#fff')
        image.alpha_channel = 'remove'
        image.format = 'jpeg'
        image.save(file=buffer)


@Request.application
def app(request: Request) -> Response:
    if request.path != '/':
        return Response(
            json.dumps({
                'error': 'not-found',
                'message': "page not found; there's only one path: /"
            }),
            status=404
        )
    elif request.method.upper() != 'POST':
        return Response(
            json.dumps({
                'error': 'method-not-allowed',
                'message': 'only POST method is allowed'
            }),
            status=405
        )
    elif request.mimetype not in {'text/html', 'application/xhtml+xml'}:
        return Response(
            json.dumps({
                'error': 'bad-request',
                'message': 'content has to be HTML'
            }),
            status=400
        )
    supported_types = sorted(SUPPORTED_TYPES)
    matched = request.accept_mimetypes.best_match(supported_types,
                                                  default='application/pdf')
    if not matched:
        return Response(
            json.dumps({
                'error': 'not-acceptable',
                'message': 'unsupported type; the list of supported '
                           'types: ' + ', '.join(SUPPORTED_TYPES)
            }),
            status=406
        )
    html = HTML(string=request.get_data(as_text=True))
    pdf_buffer = io.BytesIO()
    SUPPORTED_TYPES[matched](html, pdf_buffer)
    pdf_buffer.seek(0)
    return Response(pdf_buffer, mimetype=matched)


def main():
    parser = argparse.ArgumentParser(
        description='HTTP server that renders HTML to PDF'
    )
    parser.add_argument('--host', '-H',
                        default='0.0.0.0', help='host to listen [%(default)s]')
    parser.add_argument('--port', '-p',
                        type=int, default=8080,
                        help='port to listen [%(default)s]')
    parser.add_argument('--pong-path',
                        help='pong path to respond to to ping (e.g. /pong/)')
    parser.add_argument('--debug', '-d',
                        action='store_true', help='debug mode')
    args = parser.parse_args()
    pong_path = args.pong_path
    if pong_path is None:
        wsgi_app = app
    else:
        if not pong_path.startswith('/'):
            parser.error('--pong-path value must start with a slash (/)')
            return

        @Request.application
        def wsgi_app(request: Request):
            if request.path == pong_path:
                return Response('true', mimetype='application/json')
            return app
    if args.debug:
        run_simple(args.host, args.port, wsgi_app,
                   use_debugger=True, use_reloader=True)
    else:
        serve(wsgi_app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
