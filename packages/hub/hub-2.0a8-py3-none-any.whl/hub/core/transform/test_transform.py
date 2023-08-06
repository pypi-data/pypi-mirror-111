from hub.util.exceptions import MemoryDatasetNotSupportedError
import pytest
from hub.core.storage.memory import MemoryProvider
from hub.util.remove_cache import remove_memory_cache
from hub.api.dataset import Dataset
from hub import transform  # type: ignore
import numpy as np
from hub.core.tests.common import parametrize_all_dataset_storages
from click.testing import CliRunner


def fn1(i, mul=1, copy=1):
    d = {}
    d["image"] = np.ones((337, 200)) * i * mul
    d["label"] = np.ones((1,)) * i * mul
    return d if copy == 1 else [d] * copy


def fn2(sample, mul=1, copy=1):
    d = {"image": sample["image"] * mul, "label": sample["label"] * mul}
    return d if copy == 1 else [d] * copy


def fn3(i, mul=1, copy=1):
    d = {}
    d["image"] = np.ones((1310, 2087)) * i * mul
    d["label"] = np.ones((13,)) * i * mul
    return d if copy == 1 else [d] * copy


@parametrize_all_dataset_storages
def test_single_transform_hub_dataset(ds):
    with CliRunner().isolated_filesystem():
        with Dataset("./test/transform_hub_in_generic") as data_in:
            data_in.create_tensor("image")
            data_in.create_tensor("label")
            for i in range(1, 100):
                data_in.image.append(i * np.ones((i, i)))
                data_in.label.append(i * np.ones((1,)))
        data_in = Dataset("./test/transform_hub_in_generic")
        ds_out = ds
        ds_out.create_tensor("image")
        ds_out.create_tensor("label")
        transform(
            data_in, fn2, ds_out, pipeline_kwargs={"copy": 1, "mul": 2}, workers=5
        )
        assert len(ds_out) == 99
        for index in range(1, 100):
            np.testing.assert_array_equal(
                ds_out[index - 1].image.numpy(), 2 * index * np.ones((index, index))
            )
            np.testing.assert_array_equal(
                ds_out[index - 1].label.numpy(), 2 * index * np.ones((1,))
            )

        assert ds_out.image.shape_interval.lower == (99, 1, 1)
        assert ds_out.image.shape_interval.upper == (99, 99, 99)


@parametrize_all_dataset_storages
def test_single_transform_hub_dataset_htypes(ds):
    with CliRunner().isolated_filesystem():
        with Dataset("./test/transform_hub_in_htypes") as data_in:
            data_in.create_tensor("image", htype="image")
            data_in.create_tensor("label", htype="class_label")
            for i in range(1, 100):
                data_in.image.append(i * np.ones((i, i), dtype="uint8"))
                data_in.label.append(i * np.ones((1,), dtype="int32"))
        data_in = Dataset("./test/transform_hub_in_htypes")
        ds_out = ds
        ds_out.create_tensor("image")
        ds_out.create_tensor("label")
        transform(
            data_in, fn2, ds_out, pipeline_kwargs={"copy": 1, "mul": 2}, workers=5
        )
        assert len(ds_out) == 99
        for index in range(1, 100):
            np.testing.assert_array_equal(
                ds_out[index - 1].image.numpy(), 2 * index * np.ones((index, index))
            )
            np.testing.assert_array_equal(
                ds_out[index - 1].label.numpy(), 2 * index * np.ones((1,))
            )

        assert ds_out.image.shape_interval.lower == (99, 1, 1)
        assert ds_out.image.shape_interval.upper == (99, 99, 99)


@parametrize_all_dataset_storages
def test_chain_transform_list_small(ds):
    ls = [i for i in range(100)]
    ds_out = ds
    ds_out.create_tensor("image")
    ds_out.create_tensor("label")
    transform(
        ls,
        [fn1, fn2],
        ds_out,
        workers=1,
        pipeline_kwargs=[{"mul": 5, "copy": 2}, {"mul": 3, "copy": 3}],
    )
    assert len(ds_out) == 600
    for i in range(100):
        for index in range(6 * i, 6 * i + 6):
            np.testing.assert_array_equal(
                ds_out[index].image.numpy(), 15 * i * np.ones((337, 200))
            )
            np.testing.assert_array_equal(
                ds_out[index].label.numpy(), 15 * i * np.ones((1,))
            )


@parametrize_all_dataset_storages
def test_chain_transform_list_big(ds):
    ls = [i for i in range(2)]
    ds_out = ds
    ds_out.create_tensor("image")
    ds_out.create_tensor("label")
    transform(
        ls,
        [fn3, fn2],
        ds_out,
        workers=3,
        pipeline_kwargs=[{"mul": 5, "copy": 2}, {"mul": 3, "copy": 2}],
    )
    assert len(ds_out) == 8
    for i in range(2):
        for index in range(4 * i, 4 * i + 4):
            np.testing.assert_array_equal(
                ds_out[index].image.numpy(), 15 * i * np.ones((1310, 2087))
            )
            np.testing.assert_array_equal(
                ds_out[index].label.numpy(), 15 * i * np.ones((13,))
            )


@parametrize_all_dataset_storages
def test_chain_transform_list_small_processed(ds):
    ls = list(range(100))
    ds_out = ds
    ds_out.create_tensor("image")
    ds_out.create_tensor("label")
    if isinstance(remove_memory_cache(ds.storage), MemoryProvider):
        with pytest.raises(MemoryDatasetNotSupportedError):
            transform(ls, fn1, ds_out, scheduler="processed")
        return

    transform(
        ls,
        [fn1, fn2],
        ds_out,
        workers=3,
        pipeline_kwargs=[{"mul": 5, "copy": 2}, {"mul": 3, "copy": 3}],
        scheduler="processed",
    )
    assert len(ds_out) == 600
    for i in range(100):
        for index in range(6 * i, 6 * i + 6):
            np.testing.assert_array_equal(
                ds_out[index].image.numpy(), 15 * i * np.ones((337, 200))
            )
            np.testing.assert_array_equal(
                ds_out[index].label.numpy(), 15 * i * np.ones((1,))
            )
