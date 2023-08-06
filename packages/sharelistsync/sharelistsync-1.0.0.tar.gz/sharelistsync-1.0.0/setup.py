from distutils.core import setup

setup(
    name='sharelistsync',
    packages=['sharelistsync'],
    version='1.0.0',
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='GNU General Public License v3 (GPLv3)',
    description='A tool to sync sharepoint list with MSSQL database',
    author='Rhubenni Telesco',
    author_email='rhubenni.telesco+pydev@gmail.com',
    url='https://github.com/rhubenni/sharelistsync',
    download_url='https://github.com/rhubenni/sharelistsync/archive/1.0.0.tar.gz',
    keywords=['Office365', 'Sharepoint'],
    install_requires=[
        'shareplum',
        'pymssql'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',      # Define that your audience are developers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9'
    ],
)
