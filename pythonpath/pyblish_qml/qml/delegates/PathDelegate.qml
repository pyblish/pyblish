import QtQuick 2.3
import Pyblish 0.1


BaseGroupDelegate {
    item: Item {
        height: textArea.paintedHeight + 20

        TextArea {
            id: textArea

            anchors.fill: parent
            anchors.margins: 10
            text: modelData.item.path || "No documentation"
        }
    }
}
