import QtQuick 2.3
import Pyblish 0.1
import Pyblish.ListItems 0.1 as ListItem


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

                Label {
                    text: object.name
                    width: column.width
                }
            }
        }
    }
}
