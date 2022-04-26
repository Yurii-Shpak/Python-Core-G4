from setuptools import setup, find_packages

setup(
    name='personal_helper',
    version='0.0.1',
    description='Personal helper bot that works in 3 modes: contacts book, notes and files sorting in a selected folder.',
    url='https://github.com/Yurii-Shpak/Python-Core-G4/tree/main/personal_helper',
    author='Yurii Shpak',
    author_email='yshpak.gora@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'personal_helper': ['help.txt']},
    py_modules=['clean'],
    entry_points={'console_scripts': [
        'personal-helper = personal_helper.personal_helper:main']}
)
