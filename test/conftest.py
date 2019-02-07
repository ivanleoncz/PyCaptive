import os
import pytest

TESTING_SETTINGS = {
}


@pytest.fixture
def config():
    ''' Returns a fully loaded configuration dict '''
    con = Config(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), '..'
        )
    )

    con.from_object('app.settings')
    con.from_mapping(TESTING_SETTINGS)

    return con


@pytest.fixture
def client():
    ''' makes and returns a testclient for the flask application '''
    from app import app

    app.config.from_mapping(TESTING_SETTINGS)

    return app.test_client()
