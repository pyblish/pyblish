import QtQuick 2.3
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.1


ApplicationWindow {
    id: root

    property alias border: applicationBorder.border

    Rectangle {
        id: applicationBorder
        anchors.fill: parent
        color: "transparent"
    }
}