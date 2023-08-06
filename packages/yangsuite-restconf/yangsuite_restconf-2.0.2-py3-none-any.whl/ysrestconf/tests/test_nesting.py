import os
import unittest
import shutil
import tempfile

from ysfilemanager import YSYangSet
from ysyangtree import YSYangModels, YSContext
from yangsuite.paths import set_base_path


class TestNestedGroups(unittest.TestCase):
    """Test API generation with several nested groups."""

    testdir = os.path.join(os.path.dirname(__file__), 'data')

    @classmethod
    def setUpClass(cls):
        set_base_path(cls.testdir)
        cls.ys = YSYangSet.load("testrest", "testnesting")
        cls.ctx = YSContext(cls.ys, modulenames=['test-deep-nesting'])
        cls.ym = YSYangModels(cls.ctx, ['test-deep-nesting'])
        cls.psy = cls.ym.yangs['test-deep-nesting']

    def setUp(self):
        """Function called before starting test execution."""
        self.tmpdir = tempfile.mkdtemp()
        self.maxDiff = None

    def tearDown(self):
        """Remove the test directory."""
        shutil.rmtree(self.tmpdir)

    def test_nested_group(self):
        """Generate APIs for a group nested 3 levels."""
        print('TODO: add nested group tests')
