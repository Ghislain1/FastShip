import os

from app.core.config import Settings


class TestSettings:
    def test_default_database_url(self):
        # Reload Settings to get fresh instance without env override
        os.environ.pop("DATABASE_URL", None)
        settings = Settings()
        assert (
            settings.DATABASE_URL
            == "postgresql+asyncpg://postgres:fastship123@localhost:5432/fastship"
        )

    def test_default_superuser(self):
        settings = Settings()
        assert settings.FIRST_SUPERUSER == "admin@admin.de"

    def test_default_superuser_password(self):
        settings = Settings()
        assert settings.FIRST_SUPERUSER_PASSWORD == "admin"

    def test_default_superuser_name(self):
        settings = Settings()
        assert settings.FIRST_SUPERUSER_NAME == "Admin"

    def test_email_test_user(self):
        settings = Settings()
        assert settings.EMAIL_TEST_USER == "test@example.com"

    def test_authjwt_secret_key(self):
        settings = Settings()
        assert (
            settings.authjwt_secret_key
            == "b223e6d3a9a3ec3f00c38f7ad5f9344c22fde8f11edb85caf41623d8f27de345"
        )

    def test_authjwt_algorithm(self):
        settings = Settings()
        assert settings.authjwt_algorithm == "HS256"

    def test_authjwt_access_token_expires(self):
        settings = Settings()
        assert settings.authjwt_access_token_expires == 100

    def test_settings_instance(self):
        from app.core.config import settings

        assert isinstance(settings, Settings)

    def test_model_config_env_file(self):
        settings = Settings()
        assert settings.model_config["env_file"] == "../.env"

    def test_model_config_env_ignore_empty(self):
        settings = Settings()
        assert settings.model_config["env_ignore_empty"] is True

    def test_model_config_extra_ignore(self):
        settings = Settings()
        assert settings.model_config["extra"] == "ignore"

    def test_model_config_is_settings_config_dict(self):
        settings = Settings()
        assert isinstance(settings.model_config, dict)
