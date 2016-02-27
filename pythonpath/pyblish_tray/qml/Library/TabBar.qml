import QtQuick 2.3
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.3

/*!
    \qmltype TabBar

    \inqmlmodule Library 0.1

    \brief A series of tabs, one per Action

    Example:

    \qml
    import QtQuick 2.3
    import Library 0.1

    Item {
        Loader {
            id: loader
            source: {
                0: "File1.qml",
                1: "File2.qml"
            }[tabBar.currentIndex]
        }

        TabBar {
            id: tabBar
            
            actions: [
                Action { iconName: "close" }
                Action { iconName: "hand-o-up" }
            ]

            anchors.fill: parent

            delegate: Text {
                height: 20
                text: modelData
            }
        }
    }
*/
Item {
    id: root

    /*!
        Source actions to display as tabs
    */
    property list<Action> actions

    property Component foreground
    property alias background: loader.sourceComponent

    /*!
        The current tab as an integer
    */
    property int currentIndex: 0

    /*!
        Optional size of a tab's icon
    */
    property int iconSize: 30

    implicitHeight: iconSize

    Loader {
        id: loader
        anchors.fill: parent
    }

    RowLayout {
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        spacing: 0

        Repeater {
            id: repeater
            model: actions

            delegate: MouseArea {
                id: mousearea

                property var action: modelData

                width: iconSize
                height: iconSize
                hoverEnabled: true
                enabled: action.enabled
                
                Loader {
                    id: loader

                    readonly property int isCurrent: currentIndex == index
                    readonly property bool containsMouse: mousearea.containsMouse

                    anchors.fill: parent
                    sourceComponent: root.foreground
                }

                AwesomeIcon {
                    anchors.centerIn: parent
                    name: action.iconName
                    size: iconSize / 2
                    color: currentIndex === index ? "white" : "gray"
                }

                onPressed: {
                    action.trigger(mouse)
                    root.currentIndex = index
                }
            }
        }
    }
}