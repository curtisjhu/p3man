from click.testing import CliRunner


class AccountTest():
    runner = CliRunner()
    def test_setup(self):
        res = runner.invoke(setup)
    
    def test_reset(self):
        pass
    def test_wipe(self):
        pass