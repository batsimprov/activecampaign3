from setuptools import setup, find_packages

setup(
        author='Ana Nelson',
        author_email='ana@ananelson.com',
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Topic :: Office/Business :: Groupware",
            ],
        description='ActiveCampaign v3 API Wrapper',
        install_requires = [
            'dateparser',
            'inflection',
            'pyyaml',
            'requests',
            ],
        name='activecampaign3',
        url='https://github.com/batsimprov/activecampaign3',
        packages=find_packages(),
        version='0.0.2'
    )
