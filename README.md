# talk is cheap, show me the code!

https://github.com/niklasf/python-chess

https://python-chess.readthedocs.io/

PyQt5中文教程
https://maicss.gitbook.io/pyqt5-chinese-tutoral/

Picovoice
https://www.picovoice.ai/

Wake Word Detection on the Raspberry Pi with Porcupine
https://pimylifeup.com/raspberry-pi-porcupine/  
备注：上述文档创建的.asoundrc会在树莓派重启后被自动删除，貌似和树莓派新版本启用pulseaudio有关，但目前不影响麦克风采集声音！

------------------------------------------------------------------------------------------
--国内镜像库
--通过参数-i https://mirrors.aliyun.com/pypi/simple/ 指定从国内镜像库安装，提高下载和安装速度
------------------------------------------------------------------------------------------

pip3 install -i https://mirrors.aliyun.com/pypi/simple/  python-chess

pip3 install -i https://mirrors.aliyun.com/pypi/simple/ PyAudio

pip3 install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5  

--树莓派安装PyQt5  
sudo apt update  
sudo apt install python3-pyqt5   # for python3  
sudo apt install python3-pyqt5.qtsvg   # for python3  
sudo apt install python-pyqt5    # for python2  
sudo apt install python-pyqt5.qtsvg    # for python2  

pip3 install -i https://mirrors.aliyun.com/pypi/simple/ turtle

pip3 install -i https://mirrors.aliyun.com/pypi/simple/ termcolor

pip3 install -i https://mirrors.aliyun.com/pypi/simple/ serial

pip3 install -i https://mirrors.aliyun.com/pypi/simple/ pyserial

pip3 install -i https://mirrors.aliyun.com/pypi/simple/ pip

pip3 install -i https://mirrors.aliyun.com/pypi/simple/ pygame

离线语音识别方案一 SpeechRecognition + pocketsphinx：  
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ SpeechRecognition  
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ pocketsphinx

离线语音识别方案二 Picovoice：  
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ picovoice  
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ pvporcupine  
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ pvrhino
