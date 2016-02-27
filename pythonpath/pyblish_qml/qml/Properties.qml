import QtQuick 2.3
import Pyblish 0.1


Item {
    id: properties

    property var itemData: {}

    property var model: {
        var sourceData,
            data = []

        var sourceData = itemData.data
        
        Object.keys(sourceData).forEach(function (key) {
            data.push({"value": key, "column": 0})
            data.push({"value": sourceData[key], "column": 1})
        })

        return data
    }

    ActionBar {
        id: header

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right

        actions: [
            Action {
                iconName: "button-back"
                onTriggered: stack.pop()
            },

            Action {
                name: itemData.name
            }
        ]

        width: properties.width

        elevation: 1
    }

    View {
        id: body

        elevation: -1

        anchors.top: header.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom

        anchors.margins: 5

        ListView {
            id: content

            spacing: 10

            anchors.fill: parent
            anchors.margins: 10

            model: VisualItemModel {
                Label {
                    id: headline

                    style: "headline"

                    text: itemData.name
                }

                TextArea {
                    id: description
                    
                    // TODO(marcus): Make a better indent
                    x: 20
                    
                    text: itemData.doc != null ? itemData.doc : "No description"
                }

                Label {
                    style: "title"

                    text: "Data"
                }

                Grid {
                    columns: 2
                    columnSpacing: 20
                    rowSpacing: 2

                    x: 20

                    Repeater {
                        id: repeater

                        delegate: property

                        model: properties.model
                    }
                }
            }
        }
    }

    Component {
        id: property

        Loader {
            id: loader

            property var value: modelData.value

            visible: loader.status == Loader.Ready

            Component.onCompleted: {
                if (modelData.column == 0) {
                    loader.sourceComponent = labelProperty

                } else {
                    loader.sourceComponent = textProperty
                }
            }
        }
    }

    Component {
        id: labelProperty

        Label {
            id: label

            font.weight: Font.DemiBold

            color: "gray"

            text: value
        }
    }

    Component {
        id: textProperty

        Label {
            id: label

            wrapMode: Text.WordWrap

            anchors.verticalCenter: parent.verticalCenter
            
            text: typeof value == "string" ? value : 
                  typeof value != "undefined" ? JSON.stringify(value) :
                  "No value"
        }
    }
}
