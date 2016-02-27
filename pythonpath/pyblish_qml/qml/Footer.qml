import QtQuick 2.3
import Pyblish 0.1


View {
    id: footer

    property alias message: __message
    
    // 0 = Default; 1 = Publishing; 2 = Finished
    property int mode: 0
    property bool paused: false

    signal publish
    signal validate
    signal pause
    signal stop
    signal reset
    signal save

    width: 200
    height: 40

    Message {
        id: __message
        anchors.verticalCenter: parent.verticalCenter
    }

    Row {
        id: row

        anchors {
            right: parent.right
            top: parent.top
            bottom: parent.bottom
            margins: 5
        }

        spacing: 3

        AwesomeButton {
            elevation: 1

            size: 25
            iconSize: 14

            tooltip: visible ? "Stop" : ""

            name: "stop"
            visible: mode === 1 ? true : false
            onClicked: footer.stop()
        }

        AwesomeButton {
            elevation: 1
            size: 25
            iconSize: 14

            tooltip: visible ? "Reset" : ""

            name: "refresh"
            visible: mode == 0 || mode == 2 ? true : false
            onClicked: footer.reset()
        }

        AwesomeButton {
            elevation: 1

            size: 25
            iconSize: 14

            tooltip: visible ? "Validate" : ""

            name: "flask"
            visible: mode === 0 ? true : false
            onClicked: footer.validate()
        }

        AwesomeButton {
            elevation: 1
            size: 25
            iconSize: 14

            name: "play"

            tooltip: visible ? "Publish" : ""

            onClicked: footer.publish()

            visible: mode == 0 ? true : false

        }
    }
}