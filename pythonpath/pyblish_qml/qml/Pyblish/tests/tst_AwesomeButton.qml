import QtQuick 2.3
import Pyblish 0.1

Rectangle {
    width: 300
    height: 600

    color: "brown"

    ListView {
        anchors.fill: parent

        model: ["power-off",
                "music",
                "th-large",
                "wrench",
                "arrow-right",
                "angle-right",
                "angle-double-right"]

        delegate: AwesomeButton {
            name: modelData
            size: 12
        }
    }
}
