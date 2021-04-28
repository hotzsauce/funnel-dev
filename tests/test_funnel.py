import unittest
import pandas as pd


from funnelmap.funnel import FunnelMap

good_mapping = {
	'salmon': 'fish',
	'tuna': 'fish',
	'broccoli': 'vegetable',
	'onion': 'vegetable',
	'carrot': 'vegetable',
	'canola': 'oil',
	'olive': 'oil',
	'avocado': 'oil'
}
good_dict = {
	'fish': ['salmon', 'tuna'],
	'vegetable': ('broccoli', 'onion', 'carrot'),
	'oil': {'canola', 'olive', 'avocado'}
}

mix_dict = {
	'fish': ['salmon', 'tuna'],
	'vegetable': ('broccoli', 'onion', 'carrot'),
	'oil': {'canola', 'olive', 'avocado', 'vegetable'}
}
dup_dict = {
	'fish': ['salmon', 'tuna'],
	'vegetable': ('broccoli', 'onion', 'carrot'),
	'fruit': ['olive', 'avocado'],
	'oil': {'canola', 'olive', 'avocado'}
}

class TestFunnel(unittest.TestCase):

	def test_dict_init(self):
		fm = FunnelMap(good_dict)

		self.assertEqual(len(fm.ids), 3)
		self.assertEqual(len(fm.aliases), 8)

	def test_dict_init_id_alias_collision(self):
		with self.assertRaises(ValueError):
			fm = FunnelMap(mix_dict)

	def test_dict_init_duplicate_alias(self):
		with self.assertRaises(KeyError):
			fm = FunnelMap(dup_dict)

	def test_ids_property(self):
		ids = {'fish', 'vegetable', 'oil'}
		fm = FunnelMap(good_dict)
		self.assertEqual(set(fm.ids), ids)

	def test_aliases_property(self):
		aliases = {'salmon', 'tuna', 'broccoli', 'onion', 'carrot',
			'canola', 'olive', 'avocado'}
		fm = FunnelMap(good_dict)
		self.assertEqual(set(fm.aliases), aliases)

	def test_funnel_to_json(self):
		small_dict = {
			'fruit': ['apple', 'grape'],
			'oil': 'olive'
		}
		small_dict_str = (
			'[{"id": "fruit", "aliases": ["apple", "grape"]}, '
			'{"id": "oil", "aliases": ["olive"]}]'
		)
		fm = FunnelMap(small_dict)
		self.assertEqual(fm.to_json(), small_dict_str)

	def test_funnel_setitem(self):
		fm = FunnelMap(good_dict)
		fm['cod'] = 'fish'

		good_maps = good_mapping.copy()
		good_maps['cod'] = 'fish'
		self.assertEqual(fm.__dict__, good_maps)

	def test_funnel_getitem_by_alias(self):
		fm = FunnelMap(good_dict)
		self.assertEqual(fm['salmon'], 'fish')

	def test_funnel_getitem_by_id(self):
		fm = FunnelMap(good_dict)
		self.assertEqual(fm['fish'], 'fish')

	def test_funnel_getitem_bad_key(self):
		fm = FunnelMap(good_dict)
		with self.assertRaises(KeyError):
			bad = fm['not a fish']

	def test_funnel_delitem(self):
		fm = FunnelMap(good_dict)
		del fm['canola']

		good_maps = good_mapping.copy()
		_ = good_maps.pop('canola')
		self.assertEqual(fm.__dict__, good_maps)


if __name__ == '__main__':
	uittest.main()
