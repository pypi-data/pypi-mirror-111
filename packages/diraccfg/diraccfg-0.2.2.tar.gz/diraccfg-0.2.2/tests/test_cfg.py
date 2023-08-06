import os
import pytest
from diraccfg.cfg import CFG

EXAMPLE_CFG_FILE = os.path.join(os.path.dirname(__file__), 'releases.cfg')
BROKEN_OPEN_CFG_FILE = os.path.join(os.path.dirname(__file__), 'broken_open.cfg')
BROKEN_CLOSE_CFG_FILE = os.path.join(os.path.dirname(__file__), 'broken_close.cfg')


def test_load():
  rels = CFG().loadFromFile(EXAMPLE_CFG_FILE)
  assert rels['Releases']['v6r22']['DIRACOS'] == 'v1r2'  # pylint: disable=unsubscriptable-object


def test_comment():
  c = CFG().loadFromFile(EXAMPLE_CFG_FILE)
  c.getComment('Releases').strip() == 'Here is where the releases go:'


def test_sanity():
  with pytest.raises(ValueError) as excinfo:
    rels = CFG().loadFromFile(BROKEN_OPEN_CFG_FILE)
  assert 'close more section' in str(excinfo)

  with pytest.raises(ValueError) as excinfo:
    rels = CFG().loadFromFile(BROKEN_CLOSE_CFG_FILE)
  assert 'open more section' in str(excinfo)
