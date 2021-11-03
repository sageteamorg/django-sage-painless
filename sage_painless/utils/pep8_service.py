"""
django-sage-painless - Pep8 Class

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
import autopep8


class Pep8:
    @classmethod
    def fix_pep8(cls, file_path):
        """
        fix pep8 (E122,E271,E231,E261,E225,E303,E302,E305,E501,W292,W391)
        """
        options = autopep8.parse_args(
            ['--in-place', '--aggressive', '--select', 'E122,E271,E231,E261,E225,E303,E302,E305,E501,W292,W391', file_path]
        )
        autopep8.fix_file(filename=file_path, options=options)
