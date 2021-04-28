import unittest
import pathlib

from funnelmap.reading import read_json, read_csv


class TestRead(unittest.TestCase):

	example_dir = pathlib.Path(__file__).parent / 'examples'

	def test_read_json(self):
		json_name = 'around.json'
		json_path = self.example_dir / json_name
		fm = read_json(json_path)

		self.assertEqual(len(fm.ids), 4)
		self.assertEqual(len(fm.aliases), 15)

	def test_read_json_duplicate_ids(self):
		json_name = 'around_dup_id.json'
		json_path = self.example_dir / json_name

		with self.assertRaises(KeyError):
			fm = read_json(json_path)

	def test_read_json_incorrect_keys(self):
		json_name = 'around_bad_id.json'
		json_path = self.example_dir / json_name

		with self.assertRaises(OSError):
			fm = read_json(json_path)

	def test_read_csv(self):
		csv_name = 'around.csv'
		csv_path = self.example_dir / csv_name
		fm = read_csv(csv_path)

		self.assertEqual(len(fm.ids), 4)
		self.assertEqual(len(fm.aliases), 15)

	def test_read_csv_duplicate_ids(self):
		csv_name = 'around_dup_id.csv'
		csv_path = self.example_dir / csv_name

		with self.assertRaises(KeyError):
			fm = read_csv(csv_path)

	def test_read_csv_bad_id_index(self):
		csv_name = 'around.csv'
		csv_path = self.example_dir / csv_name

		with self.assertRaises(TypeError):
			fm = read_csv(csv_path, id_index='funnelmap')




if __name__ == '__main__':
	unittest.main()
