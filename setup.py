from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

import glob


directives = {'linetrace': False, 'language_level': 3}

ext_modules = [
    Extension('savefolder-api', [filename for filename in glob.iglob('src/**/*.py', recursive=True)])
]

setup(
    name='SaveFolderAPI',
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize(ext_modules, compiler_directives=directives),
)
