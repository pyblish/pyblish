import QtQuick 2.3
import QtQuick.Layouts 1.1

import Pyblish 0.1
import Pyblish.ListItems 0.1


MouseArea {
    id: root

    hoverEnabled: true

    property string text: "default"

    property bool active: true
    property bool available: true
    property bool checked: false
    property string type: "action"
    property string icon: ""

    property int margins: 5

    acceptedButtons: type === "action" ? Qt.LeftButton : Qt.NoButton

    /*
        The default look of the action
    */
    RowLayout {
        visible: type === "action"

        anchors.fill: parent

        AwesomeIcon {
            Layout.fillHeight: true
            width: 30
            name: icon
            opacity: 0.5
        }

        Label {
            id: label
            opacity: (active && available) ? 1.0 : 0.5
            text: root.text

            Layout.fillWidth: true
            anchors.verticalCenter: parent.verticalCenter
            font.strikeout: !available
            elide: Text.ElideRight
        }
    }

    /*
        For actions used as a Category
    */
    Label {
        id: __category

        x: 5

        visible: type === "category"
        opacity: 0.5

        anchors.verticalCenter: parent.verticalCenter
        text: root.text
    }

    /*
        For actions used as a Separator
    */
    Rectangle {
        visible: type === "separator"
        color: "black"
        opacity: 0.1
        height: 1
        anchors.verticalCenter: parent.verticalCenter
        anchors {
            left: parent.left
            right: parent.right
        }
    }

    Rectangle {
        id: __hover
        color: "white"
        opacity: 0.1
        visible: type === "action" && containsMouse

        anchors.fill: parent
        anchors.margins: 1
    }
}