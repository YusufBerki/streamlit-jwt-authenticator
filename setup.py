from distutils.core import setup
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name='streamlit-jwt-authenticator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['streamlit_jwt_authenticator'],
    version='0.0.2',
    license='Apache-2.0',
    description='An authentication module to add JWT authentication via API for Streamlit applications',
    author='Yusuf Berki YAZICIOĞLU',
    author_email='mail@yusufberki.net',
    url='https://github.com/YusufBerki/streamlit-jwt-authenticator',
    keywords=['streamlit', 'jwt', 'authentication'],
    install_requires=[
        'streamlit',
        'extra-streamlit-components',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Database :: Front-Ends',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Widget Sets',
        "License :: OSI Approved :: Apache Software License",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
