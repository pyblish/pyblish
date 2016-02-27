import QtQuick 2.3
import QtQuick.Controls 1.3 as Controls
import QtQuick.Controls.Styles 1.3 as ControlStyle
import Pyblish 0.1
import "Delegates.js" as Delegates


Column {
    Item {
        width: parent.width
        height: parent.height - filter.height

        Rectangle {
            id: gutter

            color: Qt.darker(Theme.backgroundColor, 2)

            width: icon.width

            anchors.top: parent.top
            anchors.bottom: parent.bottom

            Icon {
                id: icon
                name: "button-expand"
                visible: false
            }
        }

        ListView {
            id: listView

            anchors.fill: parent

            clip: true

            boundsBehavior: Flickable.StopAtBounds

            model: app.resultProxy

            delegate: Loader {
                width: ListView.view.width
                sourceComponent: Delegates.components[object.type]
            }
        }
    }


    Rectangle {
        id: filter

        color: Qt.darker(Theme.backgroundColor, 2)

        width: parent.width
        height: 30

        Row {
            anchors.fill: parent

            Controls.TextField {
                height: parent.height
                width: parent.width - toolBar.width

                placeholderText: "Filter.."

                style: ControlStyle.TextFieldStyle {
                    background: Rectangle { color: "transparent" }
                    textColor: "white"
                    placeholderTextColor: Qt.darker(textColor, 1.5)
                }

                onTextChanged: app.resultProxy.setFilterFixedString(text)
            }

            Row {
                id: toolBar

                height: parent.height

                spacing: 5

                Repeater {
                    model: [
                        {
                            name: "DEBUG",
                            color: Qt.lighter("steelblue", 1.3),
                            icon: "log-debug-16x16",
                            toggled: false
                        },
                        {
                            name: "INFO",
                            color: Qt.lighter("steelblue", 1.5),
                            icon: "log-info-16x16",
                            toggled: true
                        },
                        {
                            name: "WARNING",
                            color: Qt.lighter("red", 1.6),
                            icon: "log-warning-16x16",
                            toggled: true
                        },
                        {
                            name: "ERROR",
                            color: Qt.lighter("red", 1.4),
                            icon: "log-error-16x16",
                            toggled: true
                        },
                        {
                            name: "CRITICAL",
                            color: Qt.lighter("red", 1.2),
                            icon: "log-critical-16x16",
                            toggled: true
                        }
                    ]

                    Button {
                        width: 16
                        height: 16

                        tooltip: toggled ? "Hide " + modelData.name : "Show " + modelData.name

                        property bool toggled: modelData.toggled

                        anchors.verticalCenter: parent.verticalCenter

                        icon: modelData.icon

                        opacity: toggled ? 1 : 0.2

                        onClicked: {
                            this.toggled = !this.toggled
                            app.exclude("result",
                                        this.toggled ? "remove" : "add",
                                        "levelname",
                                        modelData.name)
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: app.resultModel
        onAdded: listView.positionViewAtEnd()
    }
}
