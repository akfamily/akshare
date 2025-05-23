import vectorbt as vbt


# ############# Global ############# #

def teardown_module():
    vbt.settings.reset()


# ############# settings.py ############# #

class TestSettings:
    def test_save_and_load(self, tmp_path):
        vbt.settings.set_theme('seaborn')
        vbt.settings.save(tmp_path / "settings")
        new_settings = vbt.settings.load(tmp_path / "settings")
        assert vbt.settings == new_settings
        assert vbt.settings.__dict__ == new_settings.__dict__
