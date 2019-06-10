# pylint: disable=redefined-outer-name
from datetime import date
from unittest import mock
from sqlalchemy.orm import sessionmaker, clear_mappers
import pytest
from allocation import bootstrap, commands, views


@pytest.fixture
def sqlite_bus(in_memory_sqlite_db):
    yield bootstrap.bootstrap(
        session_factory=sessionmaker(bind=in_memory_sqlite_db),
        send_mail=mock.Mock(),
        publish=mock.Mock(),
    )
    clear_mappers()


def test_allocations_view(sqlite_bus):
    sqlite_bus.handle([
        commands.CreateBatch('b1', 'sku1', 50, None),
        commands.CreateBatch('b2', 'sku2', 50, date.today()),
        commands.Allocate('o1', 'sku1', 20),
        commands.Allocate('o1', 'sku2', 20),
    ])

    assert views.allocations('o1', sqlite_bus.uow) == [
        {'sku': 'sku1', 'batchref': 'b1'},
        {'sku': 'sku2', 'batchref': 'b2'},
    ]


def test_deallocation(sqlite_bus):
    sqlite_bus.handle([
        commands.CreateBatch('b1', 'sku1', 50, None),
        commands.CreateBatch('b2', 'sku1', 50, date.today()),
        commands.Allocate('o1', 'sku1', 40),
        commands.ChangeBatchQuantity('b1', 10)
    ])

    assert views.allocations('o1', sqlite_bus.uow) == [
        {'sku': 'sku1', 'batchref': 'b2'},
    ]