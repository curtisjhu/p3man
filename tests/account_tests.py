from click.testing import CliRunner


class AccountTest():
    runner = CliRunner()
    def test_setup(self):
        res = runner.invoke(setup)
        assert result.exit_code == 0
    
    def test_reset(self):
        res = runner.invoke(setup)
        assert result.exit_code == 0
    def test_wipe(self):
        res = runner.invoke(setup)
        assert result.exit_code == 0