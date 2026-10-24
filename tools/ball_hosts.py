"""Derive namespaced ball hosts from the supplied, working recreation template.

The decoded compiledData is an import-by-path RedPackage. Only its one vanilla
mesh reference changes, at equal length. Other cooked components/buffers remain
unchanged. The modified buffer is stored uncompressed; CR2W buffer offsets,
sizes, per-buffer CRC32, buffer-table CRC32 and header CRC32 are rebuilt.
Format: WolvenKit.RED4/Archive/IO/CR2WWriter.File.cs (CalculateHeaderCRC32).
"""
from pathlib import Path
import hashlib
import json
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'assets/hosts/cyberm/entities/props/open77_prop_recreation_sleeping_bag.ent'
COMPONENTS = 'assets/templates/object-components.bin'
MESH = 'base\\environment\\decoration\\recreation\\sports\\ball\\ball_{}_billiard.mesh'

def derive(source, components, letter):
    if letter not in 'cdefghijklmnopq':
        raise ValueError('not a full-rack object ball')
    header = bytearray(source[:struct.unpack_from('<I', source, 24)[0]])
    table, count = struct.unpack_from('<II', header, 40+5*12)
    if count != 3 or source[:4] != b'CR2W':
        raise ValueError('unexpected donor buffer layout')
    old_mesh, new_mesh = MESH.format('m').encode(), MESH.format(letter).encode()
    if components.count(old_mesh) != 1 or len(old_mesh) != len(new_mesh):
        raise ValueError('unexpected compiledData mesh binding')
    parts, segments, offset = [], [{'disk':len(header), 'memory':len(header)}], len(header)
    for index in range(count):
        flags, slot, old_offset, disk, memory, crc = struct.unpack_from('<6I', header, table+index*24)
        data = source[old_offset:old_offset+disk]
        if len(data) != disk or zlib.crc32(data) != crc:
            raise ValueError('corrupt donor buffer')
        if index == 0:
            if len(components) != memory:
                raise ValueError('decoded compiledData size mismatch')
            data = components.replace(old_mesh, new_mesh)
        struct.pack_into('<6I', header, table+index*24, flags, slot, offset, len(data), memory, zlib.crc32(data))
        parts.append(data); segments.append({'disk':len(data), 'memory':memory}); offset += len(data)
    struct.pack_into('<I', header, 28, offset)
    struct.pack_into('<I', header, 40+5*12+8, zlib.crc32(header[table:table+count*24]))
    struct.pack_into('<I', header, 32, 0xdeadbeef)
    struct.pack_into('<I', header, 32, zlib.crc32(header[:160]))
    return bytes(header)+b''.join(parts), segments

def generate():
    manifest = json.loads((ROOT/'asset-manifest.json').read_text())
    source, components = (ROOT/SOURCE).read_bytes(), (ROOT/COMPONENTS).read_bytes()
    recorded = manifest['ballHostSource']
    for data,key in [(source,'donorSha256'),(components,'compiledDataSha256')]:
        if hashlib.sha256(data).hexdigest() != recorded[key]:
            raise ValueError('recorded source checksum mismatch')
    rows = []
    for number,letter in enumerate('cdefghijklmnopq',1):
        content,segments = derive(source,components,letter)
        depot = 'open77\\assets\\opx_infinity\\pool\\ball_%02d.ent' % number
        path = ROOT/'assets/hosts'/depot.replace('\\','/')
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content)
        rows.append({'depot':depot, 'path':str(path.relative_to(ROOT)), 'sourceDepot':recorded['sourceDepot'],
                     'sha256':hashlib.sha256(content).hexdigest(), 'flags':2, 'segments':segments,
                     'mesh':MESH.format(letter)})
    manifest['hosts'] = [row for row in manifest['hosts'] if not row['depot'].startswith(('opx\\pool\\','open77\\assets\\opx_infinity\\pool\\'))]+rows
    (ROOT/'asset-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__ == '__main__':
    generate()
