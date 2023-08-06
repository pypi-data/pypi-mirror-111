import datetime
import unittest
from typing import Union
from pathlib import Path

import pandas
import pandas as pd
from pandas.util.testing import assert_frame_equal

from hein_utilities.temporal_data import TemporalData


class TestTemporalData(unittest.TestCase):
    def test_temporal_data(self) -> None:
        save_path: Union[str, Path] = Path.cwd().joinpath('test temporal data')
        datetime_format: str = '%Y_%m_%d_%H_%M_%S_%f'
        td = TemporalData(save_path=save_path,
                          datetime_format=datetime_format)
        # test adding data
        td1 = {
            td.time_heading: '2020_01_01_00_00_00_000000',
            'some data': 1,
        }
        td.add_data(data=td1)
        td_2 = {'some data': 2}
        td.add_data(data=td_2, t=10, units=TemporalData.UNIT_MINUTES)
        td_3 = {'some data': 3}
        td.add_data(data=td_3, t=24, units=TemporalData.UNIT_HOURS)
        expected_data = pd.DataFrame(columns=['Time (%Y_%m_%d_%H_%M_%S_%f)', 'Time (s)', 'Time (min)', 'Time (hour)', 'some data'])
        expected_data = expected_data.append({'Time (%Y_%m_%d_%H_%M_%S_%f)': '2020_01_01_00_00_00_000000',
                                              'Time (s)': 0,
                                              'Time (min)': 0,
                                              'Time (hour)': 0,
                                              'some data': 1.0,
                                              }, ignore_index=True)
        expected_data = expected_data.append({'Time (%Y_%m_%d_%H_%M_%S_%f)': '2020_01_01_00_10_00_000000',
                                              'Time (s)': 600,
                                              'Time (min)': 10,
                                              'Time (hour)': 0.167,
                                              'some data': 2.0,
                                              }, ignore_index=True)
        expected_data = expected_data.append({'Time (%Y_%m_%d_%H_%M_%S_%f)': '2020_01_02_00_10_00_000000',
                                              'Time (s)': 87000,
                                              'Time (min)': 1450,
                                              'Time (hour)': 24.167,
                                              'some data': 3.0,
                                              }, ignore_index=True)
        assert_frame_equal(td.data, expected_data)

        # test getting a subset of data
        expected_subset_1 = expected_data.head(2)
        subset_1 = td.subset_data_rows(start_index=1, end_index=3)
        assert_frame_equal(subset_1, expected_subset_1)

        expected_subset_2 = expected_data.head(2)
        subset_2 = td.subset_data_rows(start_time=0, end_time=3, units=TemporalData.UNIT_HOURS)
        assert_frame_equal(subset_2, expected_subset_2)

    def test_str_to_datetime(self) -> None:
        dt_format = '%Y_%m_%d_%H_%M_%S_%f'
        t1 = '2011_11_11_11_11_11_111111'
        t2 = '2012_12_12_12_12_12_121212'
        expected_t1 = datetime.datetime(year=2011, month=11, day=11, hour=11, minute=11, second=11, microsecond=111111)
        expected_t2 = datetime.datetime(year=2012, month=12, day=12, hour=12, minute=12, second=12, microsecond=121212)
        expected_t1_and_t2 = [expected_t1, expected_t2]
        dt1 = TemporalData.str_to_datetime(t1, datetime_format=dt_format)
        dt1and2 = TemporalData.str_to_datetime(*(t1, t2), datetime_format=dt_format)
        self.assertEqual(dt1, expected_t1)
        self.assertEqual(dt1and2, expected_t1_and_t2)

    def test_relative_datetime(self):
        dt_format = '%Y_%m_%d_%H_%M_%S_%f'
        t1 = TemporalData.str_to_datetime('2020_01_01_00_00_00_000000', datetime_format=dt_format)
        t2 = TemporalData.str_to_datetime('2020_01_01_00_00_00_300000', datetime_format=dt_format)
        t3 = TemporalData.str_to_datetime('2020_01_01_00_00_03_000000', datetime_format=dt_format)
        t4 = TemporalData.str_to_datetime('2020_01_01_00_03_00_000000', datetime_format=dt_format)
        t5 = TemporalData.str_to_datetime('2020_01_01_03_00_00_000000', datetime_format=dt_format)
        rounding = 3
        dts_s = TemporalData.relative_datetime(*[t1, t2, t3, t4, t5], units=TemporalData.UNIT_SECONDS, rounding=rounding)
        dts_min = TemporalData.relative_datetime(*[t1, t2, t3, t4, t5], units=TemporalData.UNIT_MINUTES, rounding=rounding)
        dts_hour = TemporalData.relative_datetime(*[t1, t2, t3, t4, t5], units=TemporalData.UNIT_HOURS, rounding=rounding)
        expected_dts_s = [0.0, 0.3, 3.0, 180.0, 10800.0]
        expected_dts_min = [0.0, 0.005, 0.050, 3.0, 180.0]
        expected_dts_hour = [0.0, 0.0, 0.001, 0.050, 3.0]
        self.assertEqual(dts_s, expected_dts_s)
        self.assertEqual(dts_min, expected_dts_min)
        self.assertEqual(dts_hour, expected_dts_hour)

    def test_add_relative_time_to_csv(self):
        CSV_PATH = r'test demo temporal data.csv'
        csv_data = {
            'Time (yyyyMMddHHmmss)': ['20210401070746', '20210401070800', '20210401070815',
                                     '20210401070829', '20210401070843', '20210401070858', '20210401070912',
                                     '20210401070927', '20210401070941', '20210401070956', '20210401071010',
                                     '20210401071024'],
            'Turbidity': ['52.61348159', '52.65106009', '52.6004606', '52.56263325', '52.63664627',
                          '52.59418378', '52.61994455', '52.5776011', '52.66189332', '52.65043247',
                          '52.63817873', '52.56977555'],
        }
        df = pd.DataFrame(data=csv_data)
        df.to_csv(CSV_PATH, index=False)

        OUTPUT_CSV_PATH = r'test demo temporal data with relative times.csv'
        TIME_COL_HEADING = 'Time (yyyyMMddHHmmss)'
        TIME_FORMAT = "%Y%m%d%H%M%S"

        data = pandas.read_csv(CSV_PATH)
        data_column_headings = data.columns.values.tolist()
        s_column_in_data = TemporalData.time_s_column_heading in data_column_headings
        min_column_in_data = TemporalData.time_min_column_heading in data_column_headings
        hour_column_in_data = TemporalData.time_hour_column_heading in data_column_headings
        self.assertFalse(s_column_in_data)
        self.assertFalse(min_column_in_data)
        self.assertFalse(hour_column_in_data)

        data = TemporalData.add_relative_time_to_csv(CSV_PATH, TIME_COL_HEADING, TIME_FORMAT, OUTPUT_CSV_PATH)
        data_column_headings = data.columns.values.tolist()

        self.assertTrue(Path(OUTPUT_CSV_PATH).exists())

        s_column_in_data = TemporalData.time_s_column_heading in data_column_headings
        min_column_in_data = TemporalData.time_min_column_heading in data_column_headings
        hour_column_in_data = TemporalData.time_hour_column_heading in data_column_headings
        self.assertTrue(s_column_in_data)
        self.assertTrue(min_column_in_data)
        self.assertTrue(hour_column_in_data)
        read_data = pandas.read_csv(OUTPUT_CSV_PATH)

        assert_frame_equal(data, read_data)

        Path(CSV_PATH).unlink()
        Path(OUTPUT_CSV_PATH).unlink()

