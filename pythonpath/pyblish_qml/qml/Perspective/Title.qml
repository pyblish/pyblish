import QtQuick 2.3
import QtQuick.Layouts 1.1
import Pyblish 0.1


RowLayout {
    height: 40
    spacing: 20

    property string name

    Label {
        text: name
        style: "title"
        font.weight: Font.Bold
        Layout.alignment: Qt.AlignVCenter
    }

    Rectangle {
        color: "brown"
        width: 100
        height: 20
        Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
    }

    Spacer {
        Layout.fillWidth: true
    }

    AwesomeIcon {
        name: "ellipsis-h"
        Layout.alignment: Qt.AlignBottom
    }
}