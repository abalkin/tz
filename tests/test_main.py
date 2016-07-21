# -*- coding: utf-8 -*-
import pytest

from tz import metadata
from tz.main import main


class TestMain(object):
    @pytest.mark.parametrize('helparg', ['-h', '--help'])
    def test_help(self, helparg, capsys):
        with pytest.raises(SystemExit) as exc_info:
            main(['progname', helparg])
        out, err = capsys.readouterr()
        # Should have printed some sort of usage message. We don't
        # need to explicitly test the content of the message.
        assert 'usage' in out
        # Should have used the program name from the argument
        # vector.
        assert 'progname' in out
        # Should exit with zero return code.
        assert exc_info.value.code == 0

    @pytest.mark.parametrize('versionarg', ['-V', '--version'])
    def test_version(self, versionarg, capsys):
        with pytest.raises(SystemExit) as exc_info:
            main(['progname', versionarg])
        out, err = capsys.readouterr()
        # Should print out version.
        assert out == '{0} {1}\n'.format(metadata.project, metadata.version)
        # Should exit with zero return code.
        assert exc_info.value.code == 0
