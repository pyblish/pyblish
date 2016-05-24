import QtQuick 2.3
import Pyblish 0.1


BaseDelegate {
    body: Row {
        id: delegate

        spacing: 5

        Icon {
            id: icon
            name: "logo-small"
            size: 16
        }

        Column {
            id: content

            spacing: 2

            Label {
                text: "pyblish-base " + object.pyblishServerVersion
                style: "title"
                elide: Text.ElideRight
            }

            Repeater {
                model: [
                {
                    "key": "Python",
                    "value": object.pythonVersion.split(" ")[0]
                },
                {
                    "key": "pyblish-rpc",
                    "value": object.pyblishRPCVersion
                },
                {
                    "key": "pyblish-qml",
                    "value": object.pyblishQmlVersion
                },
                {
                    "key": "Port",
                    "value": object.port
                },
                {
                    "key": "User",
                    "value": object.user
                },
                {
                    "key": "Host",
                    "value": object.host
                },
                {
                    "key": "Connected",
                    "value": Date(Date.parse(object.connectTime))
                }]

                Row {
                    spacing: 5
                    width: delegate.width - delegate.spacing - icon.width

                    Label {
                        id: _key
                        style: "body2"
                        text: modelData.key
                        backgroundColor: Theme.alpha("white", 0.1)
                    }

                    Label {
                        text: modelData.value
                        elide: Text.ElideRight
                        width: parent.width - _key.width
                    }
                }
            }
        }
    }
}