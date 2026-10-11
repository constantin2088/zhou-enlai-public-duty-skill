import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from validate_packet import validate
class PacketTests(unittest.TestCase):
 def test_supported_and_unknown(self):self.assertEqual(validate({'items':[{'id':'a','status':'supported','source':'档案A第2页'},{'id':'b','status':'unknown','next_check':'查原件'}]}),2)
 def test_duplicates(self):
  with self.assertRaises(ValueError):validate({'items':[{'id':'a','status':'inference','source':'用户输入'}]*2})
 def test_unknown_without_plan(self):
  with self.assertRaises(ValueError):validate({'items':[{'id':'a','status':'unknown','source':'材料缺失'}]})
 def test_blank_provenance(self):
  with self.assertRaises(ValueError):validate({'items':[{'id':'a','status':'supported','source':'  '}]})
 def test_empty(self):
  with self.assertRaises(ValueError):validate({'items':[]})
 def test_status_required(self):
  with self.assertRaises(ValueError):validate({'items':[{'id':'a','source':'出处'}]})
if __name__=='__main__':unittest.main()
