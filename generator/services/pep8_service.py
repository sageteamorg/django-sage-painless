import subprocess


class Pep8:
    def fix_pep8(self, file_path):
        """
        fix pep8
        """
        subprocess.run(
            [
                'autopep8',
                '--in-place',
                '--aggressive',
                '--aggressive',
                file_path
            ]
        )
