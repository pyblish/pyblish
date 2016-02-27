set packages=pyblish-base ^
             pyblish-hiero ^
             pyblish-houdini ^
             pyblish-integration ^
             pyblish-maya ^
             pyblish-nuke ^
             pyblish-qml ^
             pyblish-rpc ^
             pyblish-standalone ^
             pyblish-tray
c:\python27\python.exe dist.py %CD%\pythonpath "%packages%" --clean