from typing import List, Union, Dict
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

UNIT_SECONDS = 'seconds'
UNIT_MINUTES = 'minutes'
UNIT_HOURS = 'hours'


def cast_path(path: Union[str, Path]) -> Path:
    """if the path is not of type Path, cast and return it as a Path"""
    if type(path) != Path:
        path = Path(path)
    return path


class TemporalData:
    UNIT_SECONDS = UNIT_SECONDS
    UNIT_MINUTES = UNIT_MINUTES
    UNIT_HOURS = UNIT_HOURS

    time_s_column_heading = 'Time (s)'
    time_min_column_heading = 'Time (min)'
    time_hour_column_heading = 'Time (hour)'

    def __init__(self,
                 save_path: Union[str, Path] = Path.cwd().joinpath('temporal data'),
                 datetime_format: str = '%Y_%m_%d_%H_%M_%S_%f',
                 ):
        """
        Class for working with time based data. For adding data into a TemporalData instance, the column heading for
        the absolute time column must be in the format 'Time (self.datetime_format)'. Where the datetime_format is
        the provided format of how the data points are formatted

        There are also static methods for working with time based data.

        :param Path, str, save_path: path to save a CSV file of the data. .csv does not need to be included in the path
        :param str, datetime_format: how the times associated with each data point is are formatted
        """
        self._datetime_format = datetime_format
        self._data = pd.DataFrame(columns=[self.time_heading,
                                           self.time_s_column_heading,
                                           self.time_min_column_heading,
                                           self.time_hour_column_heading])
        save_path = cast_path(save_path)
        if save_path.is_dir():
            save_path = save_path.joinpath('temporal data')
        self.save_path: Path = save_path

    @property
    def columns(self) -> List[str]:
        return self.data.columns.values.tolist()

    @property
    def data(self) -> pd.DataFrame:
        """The time based data of interest; it is a Pandas dataframe"""
        return self._data

    @data.setter
    def data(self,
             value: pd.DataFrame):
        self._data = value

    @property
    def datetime_format(self) -> str:
        """The format that the times are recorded for the time column"""
        return self._datetime_format

    # todo add a way so that when the datetime format is changed, all previous measurements datetime format are also
    #  changed
    # @datetime_format.setter
    # def datetime_format(self,
    #                     value: str):
    #     self._datetime_format = value

    @property
    def save_path(self) -> Path:
        """Path to where to save files related to an instance of this class"""
        return self._save_path

    @save_path.setter
    def save_path(self,
                  value: Union[str, Path],
                  ):
        value = cast_path(value)
        name = value.name
        if name[-4:] == '.csv':
            value = value.with_name(f'{name[:-4]}')
        self._save_path = value

    @property
    def csv_path(self) -> Path:
        """Path to where to save a csv file for an instance of this class"""
        name = self.save_path.name
        return self.save_path.with_name(f'{name}.csv')

    @property
    def time_heading(self) -> str:
        """The heading name for the time column must be 'Time (self.datetime_format)'"""
        return f'Time ({self.datetime_format})'

    def save_csv(self, file_path: Union[Path, str] = None) -> None:
        """
        Save a csv file of all the data for an instance. If no path is provided, use the default save path for the
        instance. If a Permission error is encountered (e.g. if the file is already open), don't raise an error but
        just except it

        :param file_path: optional path to save the csv file at
        """
        if file_path is None:
            file_path = self.csv_path
        file_path = cast_path(file_path)
        try:
            self.data.to_csv(file_path, sep=',', index=False, mode='w')
        except PermissionError as e:
            print(f'failed to save {self.csv_path.absolute()}')

    def head(self,
             n: int,
             column: str = None) -> Union[pd.DataFrame, pd.Series]:
        """
        Return the first n rows of data

        :param n:
        :param column: str, column name
        :return:
        """
        data = self.data.head(n)
        if column is not None:
            data = data[column]
        return data

    def tail(self,
             n: int,
             column: str = None) -> Union[pd.DataFrame, pd.Series]:
        """
        Return the last n rows of data

        :param n:
        :param column: str, column name
        :return:
        """
        data = self.data.tail(n)
        if column is not None:
            data = data[column]
        return data

    def drop_tail(self,
                  n,
                  ):
        """Drop the last n rows of data"""
        self.data.drop(self.data.tail(n).index, inplace=True)

    def subset_data_rows(self,
                         start_index: int = None,
                         end_index: int = None,
                         start_time: float = None,
                         end_time: float = None,
                         units: Union[UNIT_SECONDS, UNIT_MINUTES, UNIT_HOURS] = None,
                         ) -> pd.DataFrame:
        """
        Get a subset of all the data based on rows. Either based on start_index and end_index, the index of the rows
        to extract, OR based on the start and end times with the provided units. Get from the start (inclusive) to
        the end index or time (exclusive) a.k.a from the start row up to but not including the end row. 1-index based.

        :param start_index: first index of the row of data to get, 1 based index, inclusive
        :param end_index: last index of the row of data to get, 1 based index, exclusive
        :param start_time: first time to get the data with units as provided by the units parameter, inclusive
        :param end_time:  last time to get the data with units as provided by the units parameter, excluding
        :param units: time units of data to extract; one of UNIT_SECONDS, UNIT_MINUTES, UNIT_HOURS
        :return:
        """
        if start_time is not None and end_time is not None and units is not None:
            if start_index is not None or end_index is not None:
                raise Exception('Must provide start_index and end_index OR start_time, end_time, and units')

        if start_index is not None and end_index is not None:
            if start_time is not None or end_time is not None or units is not None:
                raise Exception('Must provide start_index and end_index OR start_time, end_time, and units')

        if start_time is not None and end_time is not None and units is not None:
            # get subset by time
            # get the index of the first row where the time based on the units is equal to or greater than start_time
            if units == TemporalData.UNIT_SECONDS:
                units = self.time_s_column_heading
            elif units == TemporalData.UNIT_MINUTES:
                units = self.time_min_column_heading
            elif units == TemporalData.UNIT_HOURS:
                units = self.time_hour_column_heading
            else:
                raise ValueError(f'units parameter must be one of {self.UNIT_SECONDS}, {self.UNIT_MINUTES}, '
                                 f'or {self.UNIT_HOURS}')
            start_zero_based_index = self.data.index[self.data[units] >= start_time][0]
            # get the index of the of the first row where the time based on the units is past the end time
            end_zero_based_index = self.data.index[self.data[units] > end_time][0]
        else:
            # get subset by index
            start_zero_based_index = start_index - 1
            end_zero_based_index = end_index - 1
        subset = self.data.iloc[start_zero_based_index: end_zero_based_index]
        return subset

    def add_data(self,
                 data: Dict,
                 t: Union[None, str, datetime, int, float] = None,
                 units: Union[UNIT_SECONDS, UNIT_MINUTES, UNIT_HOURS] = None,
                 rounding: int = 3,
                 ):
        """
        Add data to the data property at a specific time point. Either the time point for the data is in the data
        dictionary for a key that is identical to this object's time_heading property, or t must be passed in (None
        is also a valid value for t)

        If t is None, then the time is the current time
        If t is a string, use that as it is; note that it should be in the same datetime format as this object's
        datetime_format property
        If t is given as a datetime object, it is formatted into a string based on the object's datetime_format property
        If t is a float, then units must be given. In this case, t is the number of units since the previous time
        point. The other time columns will be calculated accordingly. If this data will be the first row in
        the object's data property (if it is the first piece of data added), then the current time is used as the
        time point although

        :param dict, data: dictionary to be added into this object's data property (a Pandas dataframe)
        :param t: datetime or string formatted datetime or float
        :param units: if t is a float, units is the units for the time since the last time point
        :param rounding: how many decimal places to round the relative time (s, min, hour) columns to
        :return:
        """
        n_rows = len(self.data)
        last_row_index = n_rows - 1
        first_row = self.head(1)
        last_row = self.tail(1)
        # add time to the data to be added dictionary
        if type(t) == float or type(t) == int:
            if units is None:
                raise ValueError('If a relative time (float value) is given, units must be too')
            if n_rows == 0:
                data[self.time_heading] = TemporalData.now_string(self.datetime_format)
            else:
                last_time: str = last_row[self.time_heading][last_row_index]
                last_time: datetime = TemporalData.str_to_datetime(last_time, datetime_format=self.datetime_format)
                if units == self.UNIT_SECONDS:
                    s_since_last_time = t
                elif units == self.UNIT_MINUTES:
                    s_since_last_time = t * 60.0
                elif units == self.UNIT_HOURS:
                    s_since_last_time = t * 3600.0
                else:
                    raise ValueError('Units value not valid')
                data[self.time_heading] = (last_time + timedelta(seconds=s_since_last_time)).strftime(self.datetime_format)
        if self.time_heading not in data:
            if t is None:
                t = TemporalData.now_string(self.datetime_format)
            if type(t) is not str:
                t = t.strftime(self.datetime_format)
            data[self.time_heading] = t

        # at this point the data to be added should have a key that is identical to this object's time_heading
        # property and next is to figure out the values for the seconds, minutes, and hours columns
        if n_rows == 0:
            data[self.time_s_column_heading] = 0
            data[self.time_min_column_heading] = 0
            data[self.time_hour_column_heading] = 0
        else:
            first_time: str = first_row[self.time_heading][0]
            first_time: datetime = TemporalData.str_to_datetime(first_time, datetime_format=self.datetime_format)
            last_time: str = last_row[self.time_heading][last_row_index]
            data_time: str = data[self.time_heading]
            if last_time == data_time:
                return  # dont allow adding duplicate data for identical time
            data_time: datetime = TemporalData.str_to_datetime(data_time, datetime_format=self.datetime_format)
            times = [first_time, data_time]
            relative_s = TemporalData.relative_datetime(*times, units=UNIT_SECONDS, rounding=rounding)
            relative_min = TemporalData.relative_datetime(*times, units=UNIT_MINUTES, rounding=rounding)
            relative_hour = TemporalData.relative_datetime(*times, units=UNIT_HOURS, rounding=rounding)
            data[self.time_s_column_heading] = relative_s
            data[self.time_min_column_heading] = relative_min
            data[self.time_hour_column_heading] = relative_hour

        self.data = self.data.append(data, ignore_index=True)

    @staticmethod
    def now_string(string_format) -> str:
        """
        Get the current time from datetime.now() formatted as as a string according to the string_format property
        :return:
        """
        return datetime.now().strftime(string_format)

    @staticmethod
    def str_to_datetime(*string_values: str,
                        datetime_format: str = None,
                        ) -> Union[datetime, List[datetime]]:
        """
        Convert a list of string values, back into datetime objects with a specific format; in this case, the string has
        to have been a datetime object that was converted into a string with the datetime_format that is passed in this
        function.

        Main use has previously been when files where timestamped, and when the file names need to be converted back
        into datetime objects in order to do calculations

        :param string_values: one or more (a list) of strings that can be converted into datetime objects
        :param str, datetime_format: a string to represent the datetime format the string should be converted into; it
            should also have been the format that the strings already are in
        :return:
        """
        if len(string_values) == 1:
            # cast the string values to string, just in case it was passed in as an int or something else
            return datetime.strptime(str(string_values[0]), datetime_format)
        else:
            # cast the string values to string, just in case it was passed in as an int or something else
            return [datetime.strptime(str(value), datetime_format) for value in string_values]

    @staticmethod
    def relative_datetime(*datetime_objects: datetime,
                          units: Union[UNIT_SECONDS, UNIT_MINUTES, UNIT_HOURS] = UNIT_SECONDS,
                          rounding: int = None,
                          ) -> Union[float, List[float]]:
        """
        Convert an array of datetime objects that are absolute times, and return an array where all the times in the
        array are relative to the first time in the array. The relativity can be in seconds, minutes, or hours.
        If only one time is given, return 0.
        If two times are given, return a single float that is the time difference between the two value
        If more than two times are given, the list returned has the same length as the input

        :param datetime_objects: a list of datetime objects
        :param units: one of UNIT_SECONDS, UNIT_MINUTES, or UNIT_HOURS
        :param int, rounding: the number of decimal places to round to
        :return:
        """
        if units not in [UNIT_SECONDS, UNIT_MINUTES, UNIT_HOURS]:
            raise ValueError('units passed in is not valid')

        # takes a list of datetime objects, and makes all the values relative to the first object in the list

        if len(datetime_objects) == 1:
            return 0

        # make an array of timedelta objects where each value is the difference between the actual time relative to
        # the first time point
        array_of_datetime_timedelta = [datetime_value - datetime_objects[0] for datetime_value in
                                       datetime_objects]

        # convert the relative timedeltas to floats, where the float number is the number of seconds since the first
        # time point
        array_of_relative_x_in_seconds = [array_of_datetime_timedelta[index].total_seconds() for index
                                          in range(len(array_of_datetime_timedelta))]

        if units == UNIT_SECONDS:
            array_of_relative_datetime_objects = array_of_relative_x_in_seconds
        elif units == UNIT_MINUTES:
            array_of_relative_x_in_minutes = [array_of_relative_x_in_seconds[index] / 60.0 for index in
                                              range(len(array_of_relative_x_in_seconds))]
            array_of_relative_datetime_objects = array_of_relative_x_in_minutes
        elif units == UNIT_HOURS:
            array_of_relative_x_in_hours = [array_of_relative_x_in_seconds[index] / 3600.0 for index in
                                            range(len(array_of_relative_x_in_seconds))]
            array_of_relative_datetime_objects = array_of_relative_x_in_hours
        else:
            raise ValueError(f'units provided must be one of {UNIT_SECONDS}, {UNIT_MINUTES}, or {UNIT_HOURS} but was '
                             f'given {units}')

        if rounding is not None:
            array_of_relative_datetime_objects = [round(datetime_obj, rounding) for datetime_obj in
                                                  array_of_relative_datetime_objects]

        if len(array_of_relative_datetime_objects) == 2:
            return array_of_relative_datetime_objects[1]
        else:
            return array_of_relative_datetime_objects

    @staticmethod
    def add_relative_time_to_df(df: pd.DataFrame,
                                time_column_heading: str,
                                datetime_format: str,
                                rounding: int = 3) -> pd.DataFrame:
        """
        For a pandas data frame for timestamped data, knowing the column heading for the time column, add 3 more columns
        to the dataframe for relative time in s, min, and hour in to the dataframe. The format of the time in the time
        column must also be passed as datetime_format

        :param df: pandas dataframe. One of the columns must represent time
        :param time_column_heading: column heading for the time column
        :param datetime_format: format for the time in the time column
        :param rounding: how many decimal places to round the relative time (s, min, hour) columns to
        :return:
        """
        # get the times based on the time column
        times: List[str] = df[time_column_heading].tolist()
        # convert times to datetime.datetime type
        times: List[datetime] = TemporalData.str_to_datetime(*times, datetime_format=datetime_format)
        # get the relative times
        relative_s = TemporalData.relative_datetime(*times, units=TemporalData.UNIT_SECONDS, rounding=rounding)
        relative_min = TemporalData.relative_datetime(*times, units=TemporalData.UNIT_MINUTES, rounding=rounding)
        relative_hour = TemporalData.relative_datetime(*times, units=TemporalData.UNIT_HOURS, rounding=rounding)
        # insert the relative times as columns to the right of the original time column
        time_column_index = df.columns.get_loc(time_column_heading)
        insert_location = time_column_index + 1
        df.insert(loc=insert_location, column=TemporalData.time_hour_column_heading, value=relative_hour)
        df.insert(loc=insert_location, column=TemporalData.time_min_column_heading, value=relative_min)
        df.insert(loc=insert_location, column=TemporalData.time_s_column_heading, value=relative_s)
        return df

    @staticmethod
    def add_relative_time_to_csv(csv_path: Union[Path, str],
                                 time_column_heading: str,
                                 datetime_format: str,
                                 output_csv_path: Union[Path, str] = None,
                                 ) -> pd.DataFrame:
        """
        For a csv, knowing the column heading for the time column, add 3 more columns in the csv for relative time in s,
        min, and hour in to the csv. The format of the time in the time column must also be passed as datetime_format

        Example usage:
            CSV_PATH = r'data.csv'
            OUTPUT_CSV_PATH = r'data with relative times.csv'
            TIME_COL_HEADING = 'Time (%Y_%m_%d_%H_%M_%S)'
            TIME_FORMAT = "%Y_%m_%d_%H_%M_%S"
            add_relative_time_to_csv(CSV_PATH, TIME_COL_HEADING, TIME_FORMAT, OUTPUT_CSV_PATH)

        :param csv_path: path to a csv file
        :param time_column_heading: column heading for the time column
        :param datetime_format: format for the time in the time column
        :param output_csv_path: optional new path to save the output csv with the additional time columns to
        :return: pandas dataframe of the original data with 3 new columns with the relative times with units seconds,
            minutes, and hours
        """
        csv_path = cast_path(csv_path)
        if output_csv_path is None:
            output_csv_path = csv_path
        output_csv_path = cast_path(output_csv_path)

        # get the data
        data: pd.DataFrame = pd.read_csv(str(csv_path))
        # add relative times to the data
        data = TemporalData.add_relative_time_to_df(df=data, time_column_heading=time_column_heading,
                                                    datetime_format=datetime_format)
        # save csv
        try:
            data.to_csv(str(output_csv_path), sep=',', index=False, mode='w')
        except PermissionError as e:
            print(f'failed to save {output_csv_path.absolute()}')
        return data
