from setuptools import find_packages, setup 
from typing import List

HYPEN_E_DOT= '-e .'
def get_requirements (file_path:str) -> List [str]:

    requirements=[]
    with open (file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements = [req.strip() for req in requirements] 

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup (
name='Financial-Crime-Detection-During-Trade-Wars-2025',
version='0.01',
author='Linh',
author_email='linhhuynh996@gmail.com',
packages= find_packages(),
install_requires=get_requirements('requirements.txt')
)

