import QtQuick 2.3
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3


Rectangle {
    width: 300
    height: 300
    color: "brown"

    Row {
        id: edit

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right

        anchors.margins: 10

        TextField {
            width: parent.width - combo.width

            placeholderText: "Filter.."

            onTextChanged: qmodel.setFilterFixedString(text)
        }

        ComboBox {
            id: combo
            width: 80
            model: ["msg", "levelname"]

            onCurrentIndexChanged: {
                var index = [270, 274]
                qmodel.filterRole = index[currentIndex]
            }
        }
    }

    Rectangle {
        color: "white"
        radius: 2

        anchors.top: edit.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 10
        anchors.topMargin: 20

        ListView {
            id: listView

            clip: true

            model: qmodel

            anchors.fill: parent
            anchors.margins: 5

            delegate: itemDelegate
        }
    }

    Component {
        id: itemDelegate

        MouseArea {
            id: delegate

            width: ListView.view.width
            height: content.height + 10

            clip: true
            hoverEnabled: true

            property color levelColor: levelno < 30 ? "steelblue" : "red"

            Rectangle {
                anchors.fill: parent
                color: delegate.levelColor
                opacity: delegate.containsMouse ? 0.1 : 0

            }
            
            Row {
                id: content

                width: parent.width
                spacing: 5

                anchors.verticalCenter: parent.verticalCenter

                clip: true

                Rectangle {
                    id: level
                    height: levelText.paintedHeight + 6
                    width: levelText.paintedWidth + 6

                    color: Qt.lighter(delegate.levelColor, 1.8)

                    Text {
                        id: levelText
                        text: levelname
                        color: delegate.levelColor
                        anchors.fill: parent
                        anchors.margins: 2
                    }
                }

                Text {
                    text: msg
                    elide: Text.ElideRight
                    width: delegate.width - level.width
                    anchors.verticalCenter: parent.verticalCenter
                }
            }
        }
    }
}
