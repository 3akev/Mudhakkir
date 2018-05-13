from unittest.mock import MagicMock


def get_mock_coro(return_value=None):
    async def mock_coro(*args, **kwargs):
        return return_value

    return MagicMock(wraps=mock_coro)
