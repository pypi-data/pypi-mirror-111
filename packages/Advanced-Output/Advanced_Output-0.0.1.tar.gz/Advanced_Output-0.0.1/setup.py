import setuptools



setuptools.setup(
    name="Advanced_Output", # Replace with your own username  #自定义封装模块名与文件夹名相同
    version="0.0.1", #版本号，下次修改后再提交的话只需要修改当前的版本号就可以了
    author="翟嘉琳", #作者
    author_email="1905655735@qq.com", #邮箱
    description="Python高级输出", #描述
    long_description='Python高级输出，可以：播放音乐，显示图片，模拟线段运行', #描述
    long_description_content_type="text/markdown", #markdown
    url="https://github.com/JudyInRedHat/Advanced_Output", #github地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  #支持python版本
)
