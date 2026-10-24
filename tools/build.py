#!/usr/bin/env python3
"""Deterministic RED4 archive + Open77 preload, using the recorded source segments.

Format reference: WolvenKit.RED4/Archive/IO/ArchiveWriter.cs. Buffers remain in
original KARK encoding; the entity header is stored uncompressed. No proprietary
compressor, game install, platform executable or network access is needed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RESERVED = {'recreation.tent', 'recreation.sleeping_bag', 'recreation.gym_equipment'}


def fnv(name):
    value = 0xcbf29ce484222325
    for byte in name.lower().encode('ascii'):
        value = ((value ^ byte) * 0x100000001b3) & 0xffffffffffffffff
    return value


def crc64(data):
    value = 0xffffffffffffffff
    for byte in data:
        value ^= byte
        for _ in range(8):
            value = (value >> 1) ^ (0xc96c5795d7870f42 if value & 1 else 0)
    return value ^ 0xffffffffffffffff


def checked(path, digest):
    path = (ROOT / path).resolve()
    if not path.is_relative_to(ROOT) or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise ValueError('source checksum/path mismatch: ' + str(path))
    return path.read_bytes()


def archive(manifest):
    hosts = sorted(manifest['hosts'], key=lambda row: fnv(row['depot']))
    allowed = {'cyberm\\entities\\props\\open77_prop_' + alias.replace('.', '_') + suffix + '.ent'
               for alias in RESERVED for suffix in ('', '_attached')}
    allowed |= {'opx\\pool\\ball_%02d.ent' % i for i in range(1,16)}
    if {row['depot'] for row in hosts} != allowed or len(hosts) != 21:
        raise ValueError('only six legacy recreation hosts and fifteen namespaced ball hosts may be packaged')
    names = b''.join(row['depot'].encode('ascii') + b'\0' for row in hosts)
    footer = struct.pack('<5I', 0x4c585253, 1, len(names), len(names), len(hosts)) + names
    data = bytearray(bytes(172) + footer)
    entries, segments = [], []
    for row in hosts:
        content = checked(row['path'], row['sha256'])
        if not content.startswith(b'CR2W'):
            raise ValueError('not a cooked entity: ' + row['path'])
        first, offset = len(segments), 0
        for part in row['segments']:
            piece = content[offset:offset+part['disk']]
            if len(piece) != part['disk']:
                raise ValueError('truncated entity buffer')
            segments.append((len(data), part['disk'], part['memory']))
            data.extend(piece)
            offset += part['disk']
        if offset != len(content):
            raise ValueError('unrecorded entity bytes')
        entries.append(struct.pack('<QQIIIII20s', fnv(row['depot']), 0, row['flags'],
                                   first, len(segments), 0, 0, hashlib.sha1(content).digest()))
    data.extend(bytes((-len(data)) % 4096))
    index_position = len(data)
    table = struct.pack('<III', len(entries), len(segments), 0) + b''.join(entries)
    table += b''.join(struct.pack('<QII', *segment) for segment in segments)
    index = struct.pack('<IIQ', 8, len(table)+8, crc64(table)) + table
    data.extend(index)
    data.extend(bytes((-len(data)) % 4096))
    header = struct.pack('<IIQIQIQI', 0x52414452, 12, index_position, len(index), 0, 0, len(data), len(footer))
    data[:len(header)] = header
    return bytes(data)


def build(output=None):
    manifest = json.loads((ROOT/'asset-manifest.json').read_text())
    entries = {'archive/pc/mod/0_opx_pool_hosts.archive': archive(manifest)}
    for row in manifest['cleanup']:
        name = row['package']
        if not name.startswith('archive/pc/mod/') or '..' in Path(name).parts or not name.endswith('.xl'):
            raise ValueError('invalid cleanup package path')
        if name in entries:
            raise ValueError('duplicate preload path')
        entries[name] = checked(row['path'], row['sha256'])
    output = Path(output) if output else ROOT/'dist/opx_pool_assets.zip'
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for name, content in sorted(entries.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, content, compresslevel=9)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    args = parser.parse_args()
    path = build(args.output)
    print(path.name, path.stat().st_size, 'bytes', hashlib.sha256(path.read_bytes()).hexdigest())
