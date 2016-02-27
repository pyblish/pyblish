import QtQuick 2.0
import Pyblish 0.1


Item {
    id: root

    height: 20
    width: parent.width

    property bool checkState: true
    property string text

    signal clicked

    Label {
        text: root.text
        opacity: ma.containsPress ? 1 :
                 ma.containsMouse ? 0.75 : 0.5
        anchors.verticalCenter: parent.verticalCenter
    }

    MouseArea{
        id: ma
        anchors.fill: parent
        hoverEnabled: true
        onClicked: root.clicked()
    }
}