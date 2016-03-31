import QtQuick 2.3
import QtQuick.Layouts 1.0
import Pyblish 0.1
import "../Delegates.js" as Delegates


Item {
    id: root

    property QtObject item

    ActionBar {
        id: actionBar

        width: parent.width
        height: 45

        actions: [
            Action {
                iconName: "button-back"
                onTriggered: stack.pop()
            },
            Action {
                name: "Perspective"
            }
        ]

        elevation: 1
    }

    View {
        elevation: 1

        anchors {
            left: parent.left
            top: actionBar.bottom
            right: parent.right
            bottom: parent.bottom
            topMargin: -1
        }

        View {
            anchors.fill: parent
            anchors.margins: margins

            elevation: -1

            AwesomeIcon {
                name: "circle-o-notch-rotate"
                anchors.centerIn: parent
                opacity: body.status == Loader.Ready ? 0.0 : 1.0
                visible: opacity > 0
            }

            Loader {
                id: body

                asynchronous: true

                anchors {
                    top: header.bottom
                    bottom: parent.bottom
                    left: parent.left
                    right: parent.right
                    bottomMargin: 2
                }

                source: "Viewport.qml"
            }

            Header {
                id: header

                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right

                    leftMargin: 10
                    rightMargin: 10
                }

                Spacer {
                    height: 10
                }

                // Title {
                //     name: item.name
                //     width: parent.width
                // }

                Gadget {
                    title: item.label || item.name
                    subheading: item.familiesConcatenated
                    duration: item.duration
                    finishedAt: item.finishedAt
                    hasError: item.hasError
                    source: item.module || ""
                    itemType: item.itemType
                    amountFailed: item.amountFailed
                    amountPassed: item.amountPassed

                    width: parent.width
                }

                Spacer {
                    height: 10
                }
            }

            Rectangle {
                id: shadow
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: header.bottom
                anchors.leftMargin: 2
                anchors.rightMargin: 2

                height: 5

                gradient: Gradient {
                    GradientStop { position: 0.0; color: Theme.alpha("black", 0.3) }
                    GradientStop { position: 1.0; color: "transparent" }
                }
            }
        }
    }

    Binding {
        target: body.item
        property: "item"
        value: root.item
    }

}
