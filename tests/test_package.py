import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build', ROOT/'tools/build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class PackageTests(unittest.TestCase):
    def test_secured_loader_uses_signed_index(self):
        manifest = (ROOT/'open77.lua').read_text()
        self.assertNotIn('dependency "archivexl', manifest)
        example = json.loads((ROOT/'server-config.example.json').read_text())
        self.assertIs(example['requiredMods']['unsecured'], False)
        self.assertNotIn('archivexl', example['resources']['load'])
        self.assertEqual(example['requiredMods']['packages'], [{'id': 'archivexl', 'minVersion': '1.27.1'}])

    def test_crc_known_vector(self):
        self.assertEqual(build.crc64(b'123456789'), 0x995dc9bbdf1939fa)

    def test_rebuild_matches_committed_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = build.build(Path(tmp)/'assets.zip')
            self.assertEqual(output.read_bytes(), (ROOT/'dist/opx_pool_assets.zip').read_bytes())

    def test_archive_index_segments_and_reserved_paths(self):
        manifest = json.loads((ROOT/'asset-manifest.json').read_text())
        with zipfile.ZipFile(ROOT/'dist/opx_pool_assets.zip') as bundle:
            data = bundle.read('archive/pc/mod/0_opx_pool_hosts.archive')
        magic,version,index,size,_,_,total,footer_length = struct.unpack_from('<IIQIQIQI', data)
        self.assertEqual((magic,version,total), (0x52414452,12,len(data)))
        first,table_size,crc = struct.unpack_from('<IIQ',data,index)
        self.assertEqual((first,table_size), (8,size-8))
        self.assertEqual(build.crc64(data[index+16:index+size]),crc)
        _,_,unpacked,packed,count = struct.unpack_from('<5I',data,172)
        self.assertEqual(unpacked,packed)
        names=data[192:192+packed].rstrip(b'\0').decode('ascii').split('\0')
        self.assertEqual(count,6)
        rows={build.fnv(row['depot']):row for row in manifest['hosts']}
        self.assertEqual(set(names),{row['depot'] for row in rows.values()})
        entries,segments,deps=struct.unpack_from('<III',data,index+16)
        self.assertEqual((entries,segments,deps),(6,24,0))
        segment_start=index+28+entries*56
        for number in range(entries):
            h,_,flags,start,end,_,_=struct.unpack_from('<QQIIIII',data,index+28+number*56)
            row=rows[h]; parts=[]
            for i in range(start,end):
                offset,disk,memory=struct.unpack_from('<QII',data,segment_start+i*16)
                self.assertEqual((disk,memory),(row['segments'][i-start]['disk'],row['segments'][i-start]['memory']))
                self.assertLessEqual(offset+disk,index)
                parts.append(data[offset:offset+disk])
            source=(ROOT/row['path']).read_bytes()
            self.assertEqual(b''.join(parts),source)
            self.assertEqual(hashlib.sha256(source).hexdigest(),row['sha256'])
            self.assertEqual(flags,row['flags'])

    def test_preload_is_inert_complete_and_has_no_legacy_overrides(self):
        manifest=json.loads((ROOT/'asset-manifest.json').read_text())
        with zipfile.ZipFile(ROOT/'dist/opx_pool_assets.zip') as bundle:
            names=bundle.namelist()
            self.assertEqual(len(names),11)
            self.assertEqual(len(names),len(set(names)))
            for name in names:
                self.assertTrue(name.startswith('archive/pc/mod/'))
                self.assertNotIn('\\',name)
                self.assertNotIn('..',Path(name).parts)
                self.assertTrue(name.endswith(('.archive','.xl')))
            for row in manifest['cleanup']:
                self.assertEqual(hashlib.sha256(bundle.read(row['package'])).hexdigest(),row['sha256'])
        self.assertEqual(set(manifest['models'].values()),build.RESERVED)
        for row in manifest['hosts']:
            self.assertNotIn('_food_',row['depot'])
            self.assertNotIn('_medical_',row['depot'])
            self.assertNotIn('_military_',row['depot'])


if __name__=='__main__':
    unittest.main()
