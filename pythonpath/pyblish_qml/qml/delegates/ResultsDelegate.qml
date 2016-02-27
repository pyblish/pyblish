import QtQuick 2.3
import "../Delegates.js" as Delegates


BaseGroupDelegate {

    item: Item {
        height: column.height + 20

        Column {
            id: column

            width: parent.width
            anchors.verticalCenter: parent.verticalCenter

            spacing: 3

            Repeater {
                model: modelData.model

                Loader {
                    width: column.width
                    sourceComponent: Delegates.components[object.type]
                }
            }
        }
    }
}