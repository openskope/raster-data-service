import os
import pytest

@pytest.fixture(scope='session')
def dataset_directory(tmpdir_factory):
    '''Return the temporary directory for storing dataset files.'''
    return tmpdir_factory.mktemp('dataset_directory')

@pytest.fixture(scope='session')
def test_dataset_filename(dataset_directory):
    '''Return a function that builds a test data file name from the provided test file name.'''
    def build(test_file_path, extension='.tif'):
        test_file_base = os.path.basename(test_file_path).split('.')[-2]
        return os.path.join(str(dataset_directory), os.path.basename(test_file_base) + extension)
    return build
