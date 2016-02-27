
import QtQuick 2.3

ListView {
    id: tabView

    spacing: 5

    orientation: Qt.Horizontal

    highlightMoveDuration: 400
    clip: true

    snapMode: ListView.SnapOneItem
    interactive: false
}
