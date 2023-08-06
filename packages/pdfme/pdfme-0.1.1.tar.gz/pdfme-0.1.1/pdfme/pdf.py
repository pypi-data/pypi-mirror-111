import copy
from typing import Iterable, Union

from .base import PDFBase
from .fonts import PDFFonts
from .image import PDFImage
from .page import PDFPage
from .utils import (
    create_graphics, get_page_size, get_paragraph_stream,
    parse_margin, parse_style_str, process_style, to_roman
)

Number = Union[int, float]
MarginType = Union[int, float, Iterable, dict]
class PDF:
    def __init__(
        self, page_size: Union[str, Iterable[Number]]='a4',
        portrait: bool=True, margin: MarginType=56.693,
        page_numbering_offset: Number=0, page_numbering_style: str='arabic',
        font_family: str='Helvetica', font_size: Number=11,
        font_color: Number=0.1, text_align: str='l', line_height: Number=1.1
    ):

        self.setup_page(page_size, portrait, margin)
        self.page_numbering_offset = page_numbering_offset
        self.page_numbering_style = page_numbering_style

        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.text_align = text_align
        self.line_height = line_height

        self.formats = {}
        self.context = {}

        self.dests = {}
        self.uris = {}
        self.pages = []
        self.running_sections = []

        self.base = PDFBase()
        self.root = self.base.add({ 'Type': b'/Catalog'})
        self.base.trailer['Root'] = self.root.id

        self.fonts = PDFFonts()
        self.used_fonts = {}
        self.images = {}
        self._add_or_get_font('Helvetica', 'n')

    @property
    def page(self):
        return self.pages[self._page_index]

    @property
    def page_index(self):
        return self._page_index
    @page_index.setter
    def page_index(self, page_index):
        self._page_index = page_index
        self.context['$page'] = self.get_page_number()

    @property
    def width(self):
        return self.page.width

    @property
    def height(self):
        return self.page.height

    def setup_page(self, page_size=None, portrait=None, margin=None):
        if page_size is not None:
            self.page_width, self.page_height = get_page_size(page_size)
        if portrait is not None:
            self.portrait = portrait
        if margin is not None:
            self.margin = parse_margin(margin)

    def add_page(self, page_size=None, portrait=None, margin=None):
        if page_size is not None:
            page_width, page_height = get_page_size(page_size)
        else:
            page_height, page_width = self.page_height, self.page_width

        if (portrait is None and not self.portrait) or portrait == False:
            page_height, page_width = page_width, page_height

        margin_ = copy.deepcopy(self.margin)
        if margin is not None:
            margin_.update(parse_margin(margin))

        page = PDFPage(self.base, page_width, page_height,
            **{'margin_' + side: value for side, value in margin_.items()}
        )

        self.pages.append(page)
        self.page_index = len(self.pages) - 1

        for running_section in self.running_sections:
            self._content(**running_section)
        
        page.go_to_beginning()

    def add_running_section(self, content, width, height, x, y):
        self.running_sections.append(dict(
            content=content, width=width, height=height, x=x, y=y
        ))

    def create_image(self, image):
        return PDFImage(image)

    def add_image(
        self, pdf_image, x=None, y=None, width=None, height=None, move='bottom'
    ):
        if pdf_image.image_name not in self.images:
            image_obj = self.base.add(pdf_image.pdf_obj)
            self.images[pdf_image.image_name] = image_obj.id
        else:
            image_obj = self.base[self.images[pdf_image.image_name]]

        h = pdf_image.height
        w = pdf_image.width

        if width is None and height is None:
            width = self.page.content_width
            height = width * h/w
        elif width is None:
            width = height * w/h
        elif height is None:
            height = width * h/w

        if x is not None:
            self.page.x = x
        if y is not None:
            self.page._y = y

        self.page.add_image(image_obj.id, width, height)

        if move == 'bottom':
            self.page.y += height
        if move == 'next':
            self.page.x += width

    def image(self, image, width=None, height=None, move='bottom'):
        pdf_image = self.create_image(image)
        self.add_image(pdf_image, width=width, height=height, move=move)

    def add_font(self, fontfile, font_family, mode='n'):
        self.fonts.load_font(fontfile, font_family, mode)

    def _add_or_get_font(self, font_family, mode):
        f = (font_family, mode) 
        if f in self.used_fonts:
            return self.used_fonts[f]
        font = self.fonts.get_font(*f)
        font_obj = font.add_font(self.base)
        self.used_fonts[(font_family, mode)] = (font.ref, font_obj.id)
        return font.ref, font_obj.id

    def _used_font(self, font_family, mode):
        f = (font_family, mode)
        font_args = self._add_or_get_font(*f)
        self.page.add_font(*font_args)

    def _default_paragraph_style(
        self, width=None, height=None, text_align=None, line_height=None,
        indent=0
    ):
        return dict(
            width = self.page.width - self.page.margin_right - self.page.x \
                if width is None else width,
            height = self.page.height - self.page.margin_bottom - self.page.y \
                if height is None else height,
            text_align = self.text_align if text_align is None else text_align,
            line_height = self.line_height if line_height is None \
                else line_height,
            indent = indent
        )

    def _init_text(self, content):
        style = {'f': self.font_family, 's': self.font_size, 'c': self.font_color}
        if isinstance(content, str):
            content = {'style': style, '.': [content]}
        elif isinstance(content, (list, tuple)):
            content = {'style': style, '.': content}
        elif isinstance(content, dict):
            style_str = [key[1:] for key in content.keys() if key.startswith('.')]
            if len(style_str) > 0:
                style.update(parse_style_str(style_str[0], self.fonts))
            style.update(process_style(content.get('style'), self))
            content['style'] = style
        return content

    def _position_and_size(self, x=None, y=None, width=None, height=None):
        if x is not None:
            self.page.x = x
        if y is not None:
            self.page.y = y
        if width is None:
            width = self.page.width - self.page.margin_right - self.page.x
        if height is None:
            height = self.page.height - self.page.margin_bottom - self.page.y
        return self.page.x, self.page._y, width, height

    def get_page_number(self):
        page = self.page_index + 1 + self.page_numbering_offset
        return to_roman(page) if self.page_numbering_style == 'roman' else page

    def _create_text(
        self, content, width, height, text_align=None, line_height=None,
        indent=0, list_text=None, list_indent=None, list_style = None
    ):
        par_style = self._default_paragraph_style(
            width, height, text_align, line_height, indent
        )
        par_style.update({
            'list_text': list_text, 'list_indent': list_indent,
            'list_style': list_style
        })
        content = self._init_text(content)
        pdf_text = PDFText(content, fonts=self.fonts, pdf=self, **par_style)
        return pdf_text

    def _add_text(
        self, text_stream, x=None, y=None, width=None, height=None,
        graphics_stream=None, used_fonts=None, ids=None, move='bottom'
    ):
        stream = get_paragraph_stream(x, y, text_stream, graphics_stream)
        self.page.add(stream)

        for font in used_fonts:
            self._used_font(*font)

        for id_, rects in ids.items():
            if len(rects) == 0:
                continue
            if id_.startswith('$label:'):
                d = rects[0]
                x_ref = x + d[0]
                self.dests[id_[7:]] = [
                    self.page.page.id, b'/XYZ', round(x_ref, 3),
                    round(y + d[3], 3), round(x_ref/self.page.width, 3) + 1
                ]
            elif id_.startswith('$ref:'):
                for r in rects:
                    self.page.add_reference(
                        id_[5:],
                        [
                            round(x + r[0], 3), round(y + r[1], 3),
                            round(x + r[2], 3), round(y + r[3], 3)
                        ]
                    )
            elif id_.startswith('$uri:'):
                link = id_[5:]
                if not link in self.uris:
                    uri = self.base.add(
                        {'Type': b'/Action', 'S': b'/URI', 'URI': link}
                    )
                    self.uris[link] = uri.id

                for r in rects:
                    self.page.add_link(
                        self.uris[link],
                        [
                            round(x + r[0], 3), round(y + r[1], 3),
                            round(x + r[2], 3), round(y + r[3], 3)
                        ]
                    )

        if move == 'bottom':
            self.page.y += height
        if move == 'next':
            self.page.x += width

    def _text(
        self, content, x=None, y=None, width=None, height=None, text_align=None,
        line_height=None, indent=0, list_text=None, list_indent=None,
        list_style = None, move='bottom'
    ):
        x, y, width, height = self._position_and_size(x, y, width, height)
        if isinstance(content, PDFText):
            pdf_text = content
            pdf_text.run(x, y, width, height)
        else:
            pdf_text = self._create_text(
                content, width, height, text_align, line_height, indent,
                list_text, list_indent, list_style
            )
            pdf_text.run(x, y)

        self._add_text(move=move, **pdf_text.result)
        return pdf_text

    def text(
        self, content, text_align=None, line_height=None, indent=0,
        list_text=None, list_indent=None, list_style=None
    ):
        pdf_text = self._text(
            content, x=self.page.margin_left, width=self.page.content_width,
            text_align=text_align, line_height=line_height, indent=indent,
            list_text=list_text, list_indent=list_indent, list_style=list_style
        )
        while not pdf_text.finished:
            self.add_page()
            pdf_text = self._text(pdf_text, self.page.content_width,
                self.page.content_height, self.page.margin_left,
                self.page.margin_top
            )

    def _default_content_style(self):
        return dict(
            f=self.font_family, s=self.font_size, c=self.font_color,
            text_align=self.text_align, line_height=self.line_height, indent=0
        )

    def _create_table(
        self, content, width, height, x=None, y=None, widths=None, style=None,
        borders=None, fills=None
    ):
        style_ = self._default_content_style()
        style_.update(process_style(style, self))
        pdf_table = PDFTable(
            content, self.fonts, width, height, x, y,
            widths, style_, borders, fills, self
        )
        return pdf_table

    def _table(
        self, content, width=None, height=None, x=None, y=None, widths=None,
        style=None, borders=None, fills=None, move='bottom'
    ):
        x, y, width, height = self._position_and_size(x, y, width, height)

        if isinstance(content, PDFTable):
            pdf_table = content
            pdf_table.run(x, y, width, height)
        else:
            pdf_table = self._create_table(
                content, width, height, x, y, widths, style, borders, fills
            )
            pdf_table.run()

        self._add_graphics([*pdf_table.fills, *pdf_table.lines])
        self._add_parts(pdf_table.parts)

        if move == 'bottom':
            self.page.y += pdf_table.current_height
        if move == 'next':
            self.page.x += width

        return pdf_table

    def table(
        self, content, widths=None, style=None, borders=None, fills=None
    ):
        pdf_table = self._table(
            content, widths=widths, style=style, borders=borders, fills=fills,
            x=self.page.margin_left, width=self.page.content_width
        )
        while not pdf_table.finished:
            self.add_page()
            pdf_table = self._table(
                pdf_table, self.page.content_width, self.page.content_height,
                self.page.margin_left, self.page.margin_top
            )

    def _create_content(self, content, width=None, height=None, x=None, y=None):
        style = self._default_content_style()
        content = content.copy()
        style.update(process_style(content.get('style'), self))
        content['style'] = style
        pdf_content = PDFContent(content, self.fonts, x, y, width, height, self)
        return pdf_content

    def _content(
        self, content, width=None, height=None, x=None, y=None, move='bottom'
    ):
        x, y, width, height = self._position_and_size(x, y, width, height)

        if isinstance(content, PDFContent):
            pdf_content = content
            pdf_content.run(x, y, width, height)
        else:
            pdf_content = self._create_content(content, width, height, x, y)
            pdf_content.run()

        self._add_graphics([*pdf_content.fills,*pdf_content.lines])
        self._add_parts(pdf_content.parts)

        if move == 'bottom':
            self.page.y += pdf_content.current_height
        if move == 'next':
            self.page.x += width

        return pdf_content

    def content(self, content):
        pdf_content = self._content(
            content, x=self.page.margin_left, width=self.page.content_width
        )
        while not pdf_content.finished:
            self.add_page()
            pdf_content = self._content(pdf_content,
                self.page.content_width, self.page.content_height,
                self.page.margin_left, self.page.margin_top
            )

    def _add_graphics(self, graphics):
        stream = create_graphics(graphics)
        self.page.add(stream)

    def _add_parts(self, parts):
        for part in parts:
            part = part.copy()
            type_ = part.pop('type')
            if type_ == 'paragraph':
                self._add_text(**part)
            elif type_ == 'image':
                self.add_image(**part)

    def _build_pages_tree(self, page_list, first_level = True):
        new_page_list = []
        count = 0
        for page in page_list:
            if first_level:
                page_size = [page.width, page.height]
                page = page.page
                page['MediaBox'] = [0, 0] + page_size

            if count % 6 == 0:
                new_page_list.append(
                    self.base.add({'Type': b'/Pages', 'Kids': [], 'Count': 0})
                )
                count += 1

            last_parent = new_page_list[-1]
            page['Parent'] = last_parent.id
            last_parent['Kids'].append(page.id)
            last_parent['Count'] += 1

        if count == 1:
            self.root['Pages'] = new_page_list[0].id
        else:
            self._build_pages_tree(new_page_list, False)

    def _build_dests_tree(self, keys, vals, first_level=True):
        k = 7
        new_keys = []
        new_vals = []
        i = 0
        length = len(keys)
        obj = None
        count = 0

        while i < length:
            key = keys[i]
            val = vals[i]
            if i % k == 0:
                count += 1
                obj = self.base.add({})
                obj['Limits'] = [key if first_level else val[0], None]
                if first_level: obj['Names'] = []
                else: obj['Kids'] = []

            if first_level:
                obj['Names'].append(key)
                obj['Names'].append(val)
            else:
                obj['Kids'].append(key)

            if (i + 1) % k == 0 or (i + 1) == length:
                obj['Limits'][1] = key if first_level else val[1]
                new_keys.append(obj.id)
                new_vals.append(obj['Limits'])

            i += 1

        if count == 1:
            del obj['Limits']
            if not 'Names' in self.root: self.root['Names'] = {}
            self.root['Names']['Dests'] = obj.id
        else:
            self._build_dests_tree(new_keys, new_vals, False)

    def _build_dests(self):
        dests = list(self.dests.keys())
        if len(dests) == 0:
            return
        dests.sort()
        self._build_dests_tree(dests, [self.dests[k] for k in dests])

    def output(self, buffer):
        if len(self.pages) == 0:
            raise Exception("pdf doesn't have any pages")
        self._build_pages_tree(self.pages)
        self._build_dests()
        self.base.output(buffer)

from .content import Number, PDFContent
from .table import PDFTable
from .text import PDFText
