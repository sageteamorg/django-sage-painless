import autopep8

class Pep8:
    def fix_pep8(self, file_path):
        """
        fix pep8 (E122, E303, E305, W292, W391)
        """
        options = autopep8.parse_args(
            ['--in-place', '--aggressive', '--select', 'E122,E271,E261,E303,E305,W292,W391', file_path]
        )
        autopep8.fix_file(filename=file_path, options=options)
