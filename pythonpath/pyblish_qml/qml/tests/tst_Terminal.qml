import QtQuick 2.3
import Pyblish 0.1
import ".."


Rectangle {
    width: 300
    height: 300

    color: Theme.alpha("black", 0.8)

    Terminal {
        id: terminal

        anchors.fill: parent

        Component.onCompleted: {
            terminal.echo("Hello, World!")
        }
    }
}