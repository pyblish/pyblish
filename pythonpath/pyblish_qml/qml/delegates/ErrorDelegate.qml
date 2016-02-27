import QtQuick 2.3
import Pyblish 0.1


BaseDelegate {
    id: root

    expandable: true

    body: Row {
        id: content

        spacing: 10

        width: parent.width

        Icon {
            id: icon
            name: "error-red-16x16"
            anchors.verticalCenter: parent.verticalCenter
        }

        Column {
            id: body

            spacing: 10

            width: root.width -
                   icon.width -
                   content.spacing -
                   root.toggle.width -
                   10

            property bool hasLongMessage: object.message.indexOf("\n") != -1 ? true : false
            property string shortMessage: object.message.split("\n")[0]
            property string longMessage: object.message

            Label {
                text: root.expanded ? body.longMessage : body.shortMessage
                maximumLineCount: root.expanded ? 99999 : 1

                color: Qt.lighter("red", 1.5)

                elide: Text.ElideRight
                wrapMode: root.expanded ? Text.WordWrap : Text.NoWrap

                width: parent.width

                onLinkActivated: Qt.openUrlExternally(link)

                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.NoButton // we don't want to eat clicks on the Text
                    cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
                }
            }

            Column {
                visible: root.expanded

                Repeater {

                    model: [
                        {
                            "key": "Instance",
                            "value": object.instance || "Context"
                        },
                        {
                            "key": "Filename",
                            "value": object.fname
                        },
                        {
                            "key": "Line Number",
                            "value": object.line_number
                        },
                        {
                            "key": "Function",
                            "value": object.func
                        },
                        {
                            "key": "Exception",
                            "value": object.exc
                        }
                    ]

                    Row {
                        spacing: 5
                        opacity: 0.5

                        Label {
                            text: modelData.key
                            backgroundColor: Theme.alpha("white", 0.1)
                        }

                        Label {
                            text: modelData.value  || ""
                        }
                    }
                }
            }
        }
    }
}
