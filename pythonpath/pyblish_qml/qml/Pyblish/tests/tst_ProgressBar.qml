import QtQuick 2.3
import Pyblish 0.1

Ink {
    width: 500
    height: 200

    ProgressBar {
        id: progressBar

        anchors.fill: parent
        anchors.margins: 10

        progress: 0
    }

    onClicked: {
        print(progressBar.progress)
        if (progressBar.progress >= 0.99)
            progressBar.progress = 0
        else
            progressBar.progress += 0.1
    }
}