from setuptools import setup, find_packages

deps = [
    'click==7.1.2',
    'python-engineio==4.1.0',
    'python-socketio==5.2.1',
    'requests==2.25.1',
    'urllib3==1.26.4',
    'websocket-client==0.58.0',
]

setup(
    name='wayscript-cli',
    version='0.2.0',
    python_requires='>=3.6',
    author='wayscript',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['main'],
    install_requires=deps,
    entry_points='''
        [console_scripts]
        wayscript=main:cli
    ''',
)