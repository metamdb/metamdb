import multiprocessing
import os
import subprocess
from typing import List

ALLOWED_EXTENSIONS = {'.rxn': 'AAM', '.mol': 'MET'}


class Images(object):
    """Images class for the generation of images from chemical files."""
    def __init__(self, input_path: str, output_path: str) -> None:
        """Initialize the Images class with input and output paths.

        Arguments:
            input_path: Path to the chemical file directory.
            output_path: Path to the image directory.
        """
        self.input_path = input_path
        self.output_path = output_path

    def get_files(self, path: str, override) -> List[str]:
        """Get sorted reaction_file names from path.

        Arguments:
            path: Path to chemical file directory.

        Returns:
            List[str]: List of sorted path strings.
        """
        files = []

        for file_name in sorted(os.listdir(path)):
            name, ext = os.path.splitext(file_name)

            if ext in ALLOWED_EXTENSIONS:
                img = name + '.svg'

                if override or img not in os.listdir(self.output_path):
                    files.append(file_name)

        return files

    def generate_images(self, override=False) -> None:
        """Generate images from chemical files."""
        pool = self.setup_multiprocessing()
        files = self.get_files(self.input_path, override)

        process = pool.map_async(self.convert, files)
        process.wait()

    def setup_multiprocessing(self) -> multiprocessing.Pool:
        """Set up pool for multiprocessing.

        Returns:
            multiprocessing.Pool: Pool for multiprocessing.
        """
        count = multiprocessing.cpu_count()
        return multiprocessing.Pool(processes=count)

    def convert(self, file_name: str) -> subprocess.CompletedProcess:
        """Generate images from chemical files.

        Arguments:
            file_name: String of chemical file name to convert.

        Returns:
            subprocess.CompletedProcess: Completed subprocess object.
        """
        name, ext = os.path.splitext(file_name)
        input_path = '{0}/{1}'.format(self.input_path, file_name)
        output_path = '{0}/{1}.svg'.format(self.output_path,
                                           name.split('_sym')[0])
        print(input_path, output_path)

        query = [
            'molconvert', 'svg:amap,scale80,Q100,transbg', input_path, '-o',
            output_path
        ]

        return subprocess.call(query, shell=False)
