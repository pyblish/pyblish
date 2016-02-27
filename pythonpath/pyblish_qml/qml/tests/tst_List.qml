import QtQuick 2.3
import Pyblish 0.1
import ".."


Rectangle {
    width: 200
    height: 300
    color: Theme.alpha("black", 0.8)

    List {
        id: list

        anchors.fill: parent
        anchors.margins: 10

        Component.onCompleted: {
            if (typeof app === "undefined") {
                list.model = Qt.createQmlObject("import QtQuick 2.3; ListModel {}", list);
                list.section.property = "family";

                for (var i = 0; i < 10; i++) {
                    list.model.append({
                        "name": "item " + (i + 1),
                        "isToggled": true,
                        "isSelected": false,
                        "family": "napoleon",
                        "currentProgress": 0,
                        "isProcessing": true,
                        "isCompatible": true,
                        "active": true,
                        "hasError": false,
                        "optional": true
                    })
                }
            }
        }
    }
}