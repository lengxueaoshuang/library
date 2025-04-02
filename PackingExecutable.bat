@echo off
REM 打包可执行文件
echo "打包exe文件中......"
pyinstaller -F -w -i ./library.ico ./main.py
echo "打包完成"