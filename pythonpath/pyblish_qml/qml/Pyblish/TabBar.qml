import QtQuick 2.3
import Pyblish 0.1


View {
    id: tabBar

    height: 45

    elevation: 1

    property var tabs: []
    property int currentIndex: 0

    Row {
        spacing: -2
        anchors.fill: parent

        Repeater {
            id: repeater
            model: tabBar.tabs
            delegate: tab
        }
    }

    Component {
        id: tab

        View {
            width: 40 + row.width
            height: tabBar.height

            elevation: 1

            function selected() {
                return index == tabBar.currentIndex
            }

            Ink {
                anchors.fill: parent

                onClicked: {
                    tabBar.currentIndex = index
                }
            }

            Row {
                id: row

                anchors.centerIn: parent

                spacing: 10

                Icon {
                    anchors.verticalCenter: parent.verticalCenter
                    name: modelData.hasOwnProperty("icon") ? modelData.icon : ""
                    visible: name != ""
                }

                Label {
                    id: label
                    text: modelData.hasOwnProperty("text") ? modelData.text : modelData
                    anchors.verticalCenter: parent.verticalCenter
                }
            }

            Rectangle {
                id: underline

                anchors.left: parent.left
                anchors.right: parent.right
                anchors.margins: 2

                height: selected() ? 2 : 0
                
                y: parent.height - height - 1

                color: Theme.primaryColor

                Behavior on height {
                    NumberAnimation {
                        duration: 100
                    }
                }
            }
        }
    }
}