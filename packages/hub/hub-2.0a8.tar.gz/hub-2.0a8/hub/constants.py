BYTE_PADDING = b"\0"

# number of bytes per unit
B = 1
KB = 1000 * B
MB = 1000 * KB
GB = 1000 * MB

DEFAULT_HTYPE = "generic"
UNCOMPRESSED = "uncompressed"
DEFAULT_SAMPLE_COMPRESSION = UNCOMPRESSED
DEFAULT_CHUNK_COMPRESSION = UNCOMPRESSED  # TODO: make lz4

SUPPORTED_COMPRESSIONS = ["png", "jpeg", UNCOMPRESSED]

# If `True`  compression format has to be the same between samples in the same tensor.
# If `False` compression format can   be different between samples in the same tensor.
USE_UNIFORM_COMPRESSION_PER_SAMPLE = True

SUPPORTED_MODES = ["r", "a"]
CHUNK_MAX_SIZE = (
    32 * MB
)  # chunks won't ever be bigger than this  # TODO: make custom for user
DEFAULT_CHUNK_MIN_TARGET = 16 * MB  # some chunks might be smaller than this

MIN_FIRST_CACHE_SIZE = 32 * MB
MIN_SECOND_CACHE_SIZE = 160 * MB

# without MB multiplication, meant for the Dataset API that takes cache size in MBs
DEFAULT_MEMORY_CACHE_SIZE = 256
DEFAULT_LOCAL_CACHE_SIZE = 0

CHUNKS_FOLDER = "chunks"
DATASET_META_FILENAME = "dataset_meta.json"
TENSOR_META_FILENAME = "tensor_meta.json"
INDEX_META_FILENAME = "index_meta.json"
META_ENCODING = "utf8"

PYTEST_MEMORY_PROVIDER_BASE_ROOT = "hub_pytest"
PYTEST_LOCAL_PROVIDER_BASE_ROOT = "/tmp/hub_pytest/"  # TODO: may fail for windows
PYTEST_S3_PROVIDER_BASE_ROOT = "s3://hub-2.0-tests/"
