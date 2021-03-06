import unittest
import pandas as pd
import numpy as np
from pandas.compat import StringIO
from six import itervalues

from webviz_plotly import FilteredPlotly


class MockElement(FilteredPlotly):
    def process_data(self, frame):
        self.frame = frame
        return [
            {
                'name': column,
                'y': frame[column].tolist()
            } for column in frame.columns]


class TestFilteredPlotly(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame(
            {
                'data1': [1, 2],
                'data2': [3, 4]
            }
        )
        self.test_csv = StringIO("""
index,data1,data2
0,1,3
1,2,4""")

    def testFilterName(self):
        filtered = MockElement(self.data, check_box=True)
        self.assertTrue(
                all('name' in data['labels']
                    for data in filtered['data']))

    def testReadCSV(self):
        filtered = MockElement(self.data, check_box=True)
        filtered_csv = MockElement(self.test_csv, check_box=True)
        self.assertEqual(
                filtered['data'],
                filtered_csv['data']
        )

    def testFilterColumn(self):
        filtered = MockElement(self.data, check_box_columns=['data2'])
        self.assertTrue(
                all('data2' in data['labels']
                    for data in filtered['data']))

    def testJsDep(self):
        filtered = MockElement(self.data, check_box_columns=['data2'])
        self.assertTrue(any(
            'filtered_plotly.js'
            in file for file in filtered.get_js_dep()))

    def testDateIndex(self):
        dates = [
            pd.Timestamp('2012-05-01'),
            pd.Timestamp('2012-05-02'),
            pd.Timestamp('2012-05-03')
        ]
        ts = pd.DataFrame({'column': np.random.randn(3)}, index=dates)
        filtered = MockElement(ts)
        self.assertEqual(filtered.frame.index.dtype, 'object')
        for i, (index, row) in enumerate(filtered.frame.iterrows()):
            self.assertEqual(dates[i].strftime('%Y-%m-%d'), index)

    def testNonStringLabels(self):
        filtered = MockElement(self.data, dropdown_columns=['data2'])
        filters = filtered['dropdown_filters']
        self.assertTrue(all(all(isinstance(label, str)
                        for label in labels)
                        for labels in itervalues(filters)))


if __name__ == '__main__':
    unittest.main()
