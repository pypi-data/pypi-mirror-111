import sys
from unittest.mock import patch  # noqa: E402

sys.path.append("../semya")
from semya import Semya


class MockAbout(object):
    ascii_gytrash_logo = "test_package"
    __title__ = "test_package"
    __description__ = "test_package"
    __url__ = f"https://github.com/user/test_package"
    __version__ = "test_package_version"
    __author__ = "test_package_author"
    __author_email__ = "test_package_author_email"
    __license__ = "test_package_license"
    __copyright__ = "test_package_copyright"


class MockPackage(object):
    __about__ = MockAbout()


@patch("importlib.import_module", return_value=MockPackage())
def test_init_semya(mock_import_module, mock_package_name):
    seed = Semya(
        package_name=mock_package_name,
    )

    assert seed.package_name == mock_package_name
    assert seed.include_package_data is False  # noqa
    assert seed.project_source_url == f"https://github.com/user/{mock_package_name}"
    assert seed.python_version == ">=3.7"
    assert seed.zip_safe is False  # noqa

    mock_import_module.assert_called_with(mock_package_name)
