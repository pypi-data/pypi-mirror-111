# Builtin modules
import unittest
from typing import Any
from tempfile import TemporaryFile
# Local modules
from . import *
# Program
class FSPackerTest(unittest.TestCase):
	data:Any
	@classmethod
	def setUpClass(self) -> None:
		self.data = (
			None,
			True,
			False,
			0,
			-1,
			1,
			1<<256,
			0.0,
			0.1,
			-0.1,
			"",
			"test",
			"Ő",
			b'\xf0\xa4\xad\xa2'.decode(),
			b"",
			b"\x00",
			b"\x00FF00",
			tuple(),
			dict(),
			{"data":"ok"},
			{1:1},
			{(1,2,3):1},
		)
		return None
	def test_dumpsAndLoads(self) -> None:
		d:Any
		for d in self.data:
			self.assertEqual(loads(dumps( d )), d)
		self.assertTupleEqual(loads(dumps( (self.data, self.data)) ), (self.data, self.data))
		self.assertTupleEqual(loads(dumps( [self.data, self.data] )), (self.data, self.data))
		self.assertDictEqual(loads(dumps( {"data":self.data} )), {"data":self.data})
		return None
	def test_dumpAndLoad(self) -> None:
		with TemporaryFile() as fi:
			dump(self.data, fi)
			fi.seek(0)
			self.assertEqual(load(fi), self.data)
		return None
	def test_raises(self) -> None:
		d:bytes = dumps(self.data)
		with self.assertRaises(OutOfData):
			loads(d[:-1])
		with self.assertRaises(UnsupportedVersion):
			loads(b"\xff" + d[1:])
		d = dumps([0]*1024)
		with self.assertRaises(MaxOPProtection):
			loads(d, maxOPSize=512)
		d = dumps(list(range(1024)))
		with self.assertRaises(MaxDictProtection):
			loads(d, maxDictSize=512)

unittest.main(verbosity=2)