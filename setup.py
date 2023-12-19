from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('C:\\src\\CSVValidator\\main.py', base=base, target_name = 'CSVValidator')
]

setup(name='CSVValidator',
      version = '1.0',
      description = 'Validate CSV Entries for First Name, Last Name and E-mail and Ensures E-mail is real and validated.',
      options = {'build_exe': build_options},
      executables = executables)
