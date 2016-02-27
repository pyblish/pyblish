import QtQuick 2.3
import Pyblish 0.1


BaseDelegate {
    id: root

    property string shortMessage: object.message.split("\n")[0]
    property string longMessage: object.message

    expandable: true

    property var levels: {
        "DEBUG":  {
            "color": Qt.lighter("steelblue", 1.3),
            "icon": "log-debug-16x16"
        },
        "INFO": {
            "color": Qt.lighter("steelblue", 1.5),
            "icon": "log-info-16x16"
        },
        "WARNING": {
            "color": Qt.lighter("red", 1.6),
            "icon": "log-warning-16x16"
        },
        "ERROR": {
            "color": Qt.lighter("red", 1.4),
            "icon": "log-error-16x16"
        },
        "CRITICAL": {
            "color": Qt.lighter("red", 1.2),
            "icon": "log-critical-16x16"
        }
    }

    color: levels[object.levelname].color

    body: Row {
        property alias icon: mask.name

        spacing: 10

        Icon {
            id: mask
            name: levels[object.levelname].icon
        }

        Column {
            spacing: 10

            Label {
                id: messageLabel

                text: expanded ? longMessage : shortMessage
                elide: Text.ElideRight
                wrapMode: expanded ? Text.WordWrap : Text.NoWrap

                width: root.width -
                       mask.paintedWidth -
                       spacing -
                       root.toggle.width -
                       10
               onLinkActivated: Qt.openUrlExternally(link)

               MouseArea {
                   anchors.fill: parent
                   acceptedButtons: Qt.NoButton // we don't want to eat clicks on the Text
                   cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
               }
            }

            Column {
                visible: expanded

                Repeater {

                    model: [
                        {
                            "key": "Instance",
                            "value": object.instance || "Context"
                        },
                        {
                            "key": "Levelname",
                            "value": object.levelname
                        },
                        {
                            "key": "Object",
                            "value": object.name
                        },
                        {
                            "key": "Filename",
                            "value": object.filename
                        },
                        {
                            "key": "Path",
                            "value": object.pathname
                        },
                        {
                            "key": "Line number",
                            "value": object.lineno
                        },
                        {
                            "key": "Function name",
                            "value": object.funcName
                        },
                        {
                            "key": "Thread",
                            "value": object.threadName
                        },
                        {
                            "key": "Milliseconds",
                            "value": object.msecs
                        },
                    ]

                    Row {
                        spacing: 5
                        opacity: 0.5

                        Label {
                            text: modelData.key
                            backgroundColor: Theme.alpha("white", 0.1)
                        }

                        Label {
                            text: typeof modelData.value != "object" ? modelData.value : JSON.stringify(modelData.value)
                        }
                    }
                }
            }
        }
    }
}
