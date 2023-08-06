#!/usr/bin/env python3
import argparse
import asyncio
import io
import json
import logging
import os
import pathlib
import shlex
from subprocess import CalledProcessError

import uharfbuzz as hb

from east_asian_spacing.font import Font
import east_asian_spacing.log_utils as log_utils

logger = logging.getLogger('shaper')


def show_dump_images():
    ShaperBase._dump_images = True


class GlyphData(object):
    def __init__(self, glyph_id, cluster_index, advance, offset):
        self.glyph_id = glyph_id
        self.cluster_index = cluster_index
        self.advance = advance
        self.offset = offset

    def __eq__(self, other):
        return (self.glyph_id == other.glyph_id
                and self.cluster_index == other.cluster_index
                and self.advance == other.advance
                and self.offset == other.offset)

    def __str__(self):
        text = getattr(self, 'text', None)
        text = f't:"{text}",' if text else ''
        return (f'{{{text}'
                f'g:{self.glyph_id},'
                f'a:{self.advance},'
                f'o:{self.offset},'
                f'c:{self.cluster_index}}}')


class ShapeResult(object):
    def __init__(self, glyphs=tuple()):
        self._glyphs = glyphs

    def __eq__(self, other):
        return self._glyphs == other._glyphs

    def __len__(self):
        return len(self._glyphs)

    def __iter__(self):
        return self._glyphs.__iter__()

    def __getitem__(self, item):
        return self._glyphs[item]

    def filter(self, predicate):
        self._glyphs = filter(predicate, self._glyphs)

    def freeze(self):
        """Freeze the internal generator as a tuple.
        Once frozen, it can iterate multiple times."""
        self._glyphs = tuple(self._glyphs)

    @property
    def glyph_ids(self):
        glyph_ids = (g.glyph_id for g in self._glyphs)
        # Filter out ".notdef" glyphs. Glyph 0 must be assigned to a .notdef glyph.
        # https://docs.microsoft.com/en-us/typography/opentype/spec/recom#glyph-0-the-notdef-glyph
        glyph_ids = filter(lambda glyph_id: glyph_id, glyph_ids)
        return glyph_ids

    def set_text(self, text):
        self.freeze()
        if len(self._glyphs) == 0:
            return
        last = self._glyphs[0]
        for glyph in self._glyphs[1:]:
            last.text = text[last.cluster_index:glyph.cluster_index]
            last = glyph
        last.text = text[last.cluster_index:]

    def __str__(self):
        self.freeze()  # Make sure it is still iterable.
        return f'[{",".join(str(g) for g in self._glyphs)}]'


class ShaperBase(object):
    def __init__(self, font, language=None, script=None, features=None):
        assert isinstance(font.path, pathlib.Path)
        self.font = font
        self.language = language
        self.script = script
        self.features = features

    @property
    def features_dict(self):
        if not self.features:
            return None
        features_dict = dict()
        for feature in self.features:
            features_dict[feature] = True
        return features_dict

    async def compute_fullwidth_advance(self):
        """Computes the advance of a "fullwidth" glyph heuristically
        by measuring a few representative glyphs."""
        text = '四园水城'  # Sample characters used in CJKV.
        result = await self.shape(text)
        result.filter(lambda g: g.glyph_id)
        advances = set(g.advance for g in result)
        logger.debug('fullwidth_advance=%s for "%s"', advances, self.font)
        if len(advances) == 1:
            advance = next(iter(advances))
            return advance
        return None

    @staticmethod
    async def ensure_fullwidth_advance(font):
        """Ensures that the `Font.fullwidth_advance` is set."""
        if font.fullwidth_advance:
            return True
        shaper = Shaper(font, features=['vert'] if font.is_vertical else None)
        advance = await shaper.compute_fullwidth_advance()
        if advance:
            font.fullwidth_advance = advance
            return True
        logger.info('No fullwidth advance for "%s"', font)
        return False

    def log_result(self, result, text):
        if logger.getEffectiveLevel() <= logging.DEBUG:
            result.set_text(text)
            logger.debug('result=%s', result)

    _dump_images = False
    _shapers = None


class UHarfBuzzShaper(ShaperBase):
    async def shape(self, text):
        if not text:
            return ShapeResult()
        buffer = hb.Buffer()
        buffer.add_str(text)
        font = self.font
        features = self.features_dict
        if font.is_vertical:
            buffer.direction = 'ttb'
            assert features and features['vert']
        else:
            buffer.direction = 'ltr'
            assert not features or not features.get('vert')
        if self.language:
            buffer.language = f'x-hbot{self.language}'
            # buffer.set_language_from_ot_tag(self.language)
        if self.script:
            buffer.script = self.script
            # buffer.set_script_from_ot_tag(self.script)
        logger.debug('%s lang=%s script=%s features=%s',
                     ' '.join(f'U+{ord(ch):04X}' for ch in text),
                     self.language, self.script, features)
        # logger.debug('lang=%s, script=%s, features=%s', buffer.language,
        #              buffer.script, features)
        if log_utils._log_shaper_logs:
            buffer.set_message_func(
                lambda message: logger.debug('uharfbuzz: %s', message))
        # buffer.cluster_level = hb.BufferClusterLevel.DEFAULT
        # buffer.guess_segment_properties()
        hb.shape(font.hbfont, buffer, features, self._shapers)
        infos = buffer.glyph_infos
        positions = buffer.glyph_positions
        assert len(infos) == len(positions)
        if font.is_vertical:
            glyphs = (GlyphData(info.codepoint, info.cluster, -pos.y_advance,
                                -pos.y_offset)
                      for info, pos in zip(infos, positions))
        else:
            glyphs = (GlyphData(info.codepoint, info.cluster, pos.x_advance,
                                pos.x_offset)
                      for info, pos in zip(infos, positions))
        result = ShapeResult(glyphs)
        self.log_result(result, text)
        return result


class HbShapeShaper(ShaperBase):
    async def shape(self, text):
        if not text:
            return ShapeResult()
        hb_shape = HbShapeShaper._hb_shape_path or 'hb-shape'
        args = [hb_shape, '--output-format=json', '--no-glyph-names']
        self.append_hb_args(text, args)
        if log_utils._log_shaper_logs:
            args.append('--trace')
        logger.debug('subprocess.run: %s', shlex.join(args))
        proc = await asyncio.create_subprocess_exec(
            *args, stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        if proc.returncode:
            raise CalledProcessError(proc.returncode, hb_shape, stdout, stderr)
        with io.StringIO(stdout.decode('utf-8')) as file:
            for line in file:
                if log_utils._log_shaper_logs:
                    logger.debug('hb-shape: %s', line.rstrip())
                if line.startswith('['):
                    glyphs = json.loads(line)
        logger.debug('glyphs = %s', glyphs)
        if self._dump_images:
            await self.dump(text)

        font = self.font
        is_vertical = font.is_vertical
        if is_vertical:
            glyphs = (GlyphData(g["g"], g["cl"], -g["ay"], -g["dy"])
                      for g in glyphs)
        else:
            glyphs = (GlyphData(g["g"], g["cl"], g["ax"], g["dx"])
                      for g in glyphs)
        result = ShapeResult(glyphs)
        self.log_result(result, text)
        return result

    async def dump(self, text):
        args = ['hb-view', '--font-size=128']
        # Add '|' so that the height of `hb-view` dump becomes consistent.
        text = f'|{text}|'
        self.append_hb_args(text, args)
        proc = await asyncio.create_subprocess_exec(*args)
        await proc.wait()

    def append_hb_args(self, text, args):
        font = self.font
        args.append(f'--font-file={font.path}')
        if font.font_index is not None:
            args.append(f'--face-index={font.font_index}')
        if self.language:
            args.append(f'--language=x-hbot{self.language}')
        if self.script:
            args.append(f'--script={self.script}')
        if font.is_vertical:
            args.append('--direction=ttb')
        if self.features:
            args.append(f'--features={",".join(self.features)}')
        if self._shapers:
            args.append(f'--shapers={",".join(self._shapers)}')
        unicodes = (ord(c) for c in text)
        unicodes_as_hex_string = ','.join(hex(c) for c in unicodes)
        args.append(f'--unicodes={unicodes_as_hex_string}')

    _hb_shape_path = None


def _init_shaper():
    global Shaper
    shaper = os.environ.get('SHAPER')
    if not shaper:
        Shaper = UHarfBuzzShaper
        return
    shapers = shaper.split(',')
    if len(shapers) >= 2:
        ShaperBase._shapers = shapers[1:]
        logger.debug('Using shapers %s', ShaperBase._shapers)
    shaper = shapers[0]
    if not shaper or shaper == 'uharfbuzz':
        Shaper = UHarfBuzzShaper
        return
    logger.debug('Using HbShapeShaper "%s"', shaper)
    HbShapeShaper._hb_shape_path = shaper
    Shaper = HbShapeShaper


_init_shaper()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("font_path")
    parser.add_argument("-f", "--feature")
    parser.add_argument("-i", "--index", type=int, default=0)
    parser.add_argument("text")
    parser.add_argument("-l", "--language")
    parser.add_argument("-s", "--script")
    parser.add_argument("--vertical", dest="is_vertical", action="store_true")
    parser.add_argument("-v",
                        "--verbose",
                        help="increase output verbosity",
                        action="count",
                        default=0)
    args = parser.parse_args()
    show_dump_images()
    log_utils.init_logging(args.verbose)
    _init_shaper()  # Re-initialize to show logging.
    font = Font.load(args.font_path)
    if font.is_collection:
        font = font.fonts_in_collection[args.index]
    if args.is_vertical:
        font = font.vertical_font
    features = args.feature.split(',') if args.feature else None
    shaper = Shaper(font,
                    language=args.language,
                    script=args.script,
                    features=features)
    print(f'fullwidth={await shaper.compute_fullwidth_advance()}, '
          f'upem={font.units_per_em}')
    result = await shaper.shape(args.text)
    result.set_text(args.text)
    print('glyphs=', '\n        '.join(str(g) for g in result))


if __name__ == '__main__':
    asyncio.run(main())
