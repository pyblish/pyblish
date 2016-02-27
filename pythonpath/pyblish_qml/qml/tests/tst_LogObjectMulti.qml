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

    ListView {
        id: checkBoxes

        anchors.top: edit.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 5

        spacing: 5
        orientation: ListView.Horizontal

        // Use ListModel, as opposed to plain {}
        // due to plain {} not updating properly.
        // 
        // NOTE(marcus): I'd expect a binding to
        // modelData.level to keep the plain {}
        // up to date with changes, but it doesn't.
        model: ListModel {
            id: checkModel

            ListElement {level: "DEBUG"; checked: false}
            ListElement {level: "INFO"; checked: false}
            ListElement {level: "WARNING"; checked: false}
            ListElement {level: "ERROR"; checked: false}
            ListElement {level: "CRITICAL"; checked: false}
        }

        delegate: MouseArea {
            id: checkBox

            width: checkText.paintedWidth + 15
            height: 15

            Text {
                id: checkText
                color: "white"
                text: level
                opacity: checked ? 1.0 : 0.2
            }

            onClicked: {
                // Update visuals
                var item = checkModel.get(index)
                item.checked = !item.checked

                // Colate and transmit currently checked levels
                var data = ""
                for (var i=0; i<checkModel.count; ++i) {
                    if (checkModel.get(i).checked) {
                        data += checkModel.get(i).level + ";"
                    }
                }

                control.updateLevels(data)
            }
        }

        Component.onCompleted: {
            // Check default levels that we've specified in Control
            control.levels.split(";").forEach(function (level) {
                for (var i=0; i<checkModel.count; ++i) {
                    if (checkModel.get(i).level == level) {
                        checkModel.get(i).checked = true;
                    }
                }
            })
        }
    }
    

    Rectangle {
        color: "white"
        radius: 2

        anchors.top: checkBoxes.bottom
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
