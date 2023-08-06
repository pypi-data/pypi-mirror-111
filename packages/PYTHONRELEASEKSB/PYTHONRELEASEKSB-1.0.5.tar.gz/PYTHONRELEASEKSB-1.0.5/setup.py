from setuptools import setup, find_packages

setup(name='PYTHONRELEASEKSB', # 패키지 명

version='1.0.5',

description='Python release test',

author='ksb98',

author_email='qkfka9045@gmail.com',

url='https://eu4ng.tistory.com',

license='MIT', # MIT에서 정한 표준 라이센스 따른다

py_modules=['releasetestksb'], # 패키지에 포함되는 모듈

python_requires='>=3',

install_requires=[], # 패키지 사용을 위해 필요한 추가 설치 패키지

packages=['PYTHONRELEASEKSB'] # 패키지가 들어있는 폴더들

)