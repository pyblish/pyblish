import QtQuick 2.3
import QtQuick.Window 2.2
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.1
import QtGraphicalEffects 1.0

import Library 0.1


ApplicationWindow {
    title: "Pyblish Tray"

    width: 300
    height: 350
    minimumWidth: 250
    minimumHeight: 100

    flags: Qt.Tool | Qt.WindowStaysOnTopHint

    color: Theme.foreground

    /*! \internal */
    readonly property var __tabs: [
        {"name": "Console", "file": "ConsoleTab.qml"},
        {"name": "Virtual Host", "file": "VirtualHostTab.qml"},
        {"name": "History", "file": "HistoryTab.qml"},
        {"name": "Settings", "file": "SettingsTab.qml"},
    ]

    ColumnLayout {
        id: container

        anchors.fill: parent

        scale: headsUp.active ? 0.95 : 1.0

        Behavior on scale {
            NumberAnimation {
                duration: 100 
                easing.type: Easing.OutCubic
            }
        }

        /*!
            The body of the application, loads the various pages
            based on the currently active tab.
        */
        Loader {
            Layout.fillWidth: true
            Layout.fillHeight: true

            source: __tabs[tabBar.currentIndex]["file"]
        }

        /*!
            The primary tabs
        */
        TabBar {
            id: tabBar

            Layout.fillWidth: true

            iconSize: 30

            actions: [
                Action { iconName: "code" },
                Action { iconName: "desktop" },
                Action { iconName: "book"; enabled: false  },
                Action { iconName: "gear"; enabled: false }
            ]

            foreground: Rectangle {
                color: "transparent"
                anchors.fill: parent
                anchors.margins: 3
                // radius: 5
                border.width: 1
                border.color: Theme.highlight
                opacity: isCurrent || containsMouse ? 1 : 0

                Behavior on opacity {
                    NumberAnimation { duration: 100 }
                }
            }

            /*!
                A background color for the TabBar (below)
            */
            background: Rectangle {
                anchors.fill: parent
                color: Theme.background
            }

            /*!
                Button to keep UI visible
            */
            MouseArea {
                property bool toggled: false

                width: 30
                height: 30

                anchors {
                    bottom: parent.bottom
                    right: parent.right
                }

                AwesomeIcon {
                    name: "magnet"
                    anchors.centerIn: parent
                    opacity: parent.toggled ? 1.0 : 0.2

                    Behavior on opacity {
                        NumberAnimation { duration: 100 }
                    }
                }

                onClicked: {
                    toggled = !toggled
                    consoleCtrl.autohideChanged(!toggled)
                }
            }
        }
    }

    /*!
        The heads-up display provides messages about user
        and application events, such as copying the selection.
    */
    HeadsUpDisplay {
        id: headsUp
        anchors.centerIn: parent
        background: Rectangle {
            color: "black"
            opacity: 0.9
            radius: 3
        }
    }

    Connections {
        target: consoleCtrl
        onCopied: headsUp.notify("Copied to clipboard")
        onCleared: headsUp.notify("Selection cleared")
        onAllSelected: headsUp.notify("Everything selected")
    }

    /*!
        Apply theme from application
    */
    Component.onCompleted: {
        Object.keys(applicationTheme).forEach(function(key) {
            if (Theme.hasOwnProperty(key))
                Theme[key] = applicationTheme[key];
        })
    }
}
