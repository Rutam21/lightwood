from lightwood.api.high_level import json_ai_from_problem, code_from_json_ai, predictor_from_code
from lightwood.api.types import JsonAI, ProblemDefinition
import unittest
from mindsdb_datasources import FileDS
import os
import shutil


test_err_message = 'This ! Is ! A ! Testing ! Error !'


def create_custom_module():
    mdir = os.path.expanduser('~/lightwood_modules')

    try:
        shutil.rmtree(mdir)
    except Exception:
        pass

    os.mkdir(mdir)
    with open(os.path.join(mdir, 'custom_cleaners.py'), 'w') as fp:
        fp.write(f'def throwing_cleaner(): raise Exception("{test_err_message}")')


class TestBasic(unittest.TestCase):
    def test_0_add_throwing_cleaner(self):
        create_custom_module()

        # Create base json ai
        df = FileDS('tests/data/hdi.csv').df.iloc[0:400]
        json_ai = json_ai_from_problem(df, ProblemDefinition.from_dict({'target': 'Development Index', 'time_aim': 20}))

        # modify it
        json_ai_dump = json_ai.to_dict()
        json_ai_dump['cleaner'] = {
            'module': 'custom_cleaners.throwing_cleaner',
            'args': {}
        }
        print(json_ai_dump)

        json_ai = JsonAI.from_dict(json_ai_dump)

        # create a predictor from it
        code = code_from_json_ai(json_ai)
        predictor = predictor_from_code(code)
        try:
            predictor.learn(df)
        except Exception as e:
            assert str(e) == test_err_message
            return

        raise Exception('Predictor did not contain modified function!')
