import QtQuick 2.3
import Pyblish 0.1


BaseDelegate {
    id: root

    body: Row {
        id: content

        spacing: 10
        anchors.verticalCenter: parent.verticalCenter

        AwesomeIcon {
            id: toggle

            size: 16
            width: 16

            name: "info"
        }

        Label {
            id: label
            text: object.message

            elide: Text.ElideRight
            
            width: content.width - toggle.width - content.spacing
        }
    }
}