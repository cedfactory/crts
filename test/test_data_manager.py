import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from manage_data import data_manager

class TestData_Manager:

    def test_data_manager_read_csl_file(self):
        # action
        df = data_manager.get_df("./test/data/csl_sample.csv")

        # expectations
        df.to_csv("./test/generated/test_data_manager_read_csl_file.csv")
        df_generated = pd.read_csv("./test/generated/test_data_manager_read_csl_file.csv")
        df_ref = pd.read_csv("./test/references/test_data_manager_read_csl_file.csv")
        assert_frame_equal(df_generated, df_ref)