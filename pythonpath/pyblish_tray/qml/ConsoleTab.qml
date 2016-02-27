import QtQuick 2.3
import QtQuick.Controls 1.1
import QtGraphicalEffects 1.0

import Library 0.1

MouseArea {
    id: root

    hoverEnabled: true

    Action {
        shortcut: "Ctrl+C"
        tooltip: "Copy selected text to clipboard"
        onTriggered: consoleCtrl.copy()
    }

    Action {
        shortcut: "Ctrl+D"
        tooltip: "Clear selection"
        onTriggered: consoleCtrl.clear()
    }

    Action {
        shortcut: "Ctrl+A"
        tooltip: "Select all"
        onTriggered: consoleCtrl.selectAll()
    }

    ListView {
        id: view

        interactive: false

        anchors.fill: parent

        model: consoleCtrl.model

        /*!
            Animate the transition when positioning
            the view at the end.
        */
        function animatePositionViewAtEnd() {
            anim.stop()

            var pos = view.contentY;

            // Get final position
            view.positionViewAtEnd();

            var destPos = view.contentY;
            
            // Initialise the animation
            anim.from = pos;
            anim.to = destPos;
            anim.restart()
        }

        /*!
            The animation used during the animated
            positioning of the view.
        */
        NumberAnimation {
            id: anim
            target: view
            property: "contentY"
            easing.type: Easing.OutCubic
            duration: 200
        }

        delegate: Item {
            width: ListView.view.width
            height: 15

            /*!
                Wrap and pad text, so as to not stick
                too close to the edge of the parent surface.
            */
            Item {
                anchors.fill: parent
                anchors {
                    leftMargin: 5
                    rightMargin: 5
                }

                /*!
                    Selection highlighting
                */
                Rectangle {
                    anchors.fill: text
                    color: Qt.darker(Theme.highlight, 2)
                    visible: selected
                }

                /*!
                    Primary text
                */
                Text {
                    id: text
                    color: selected ? "#fff" : "#ddd"
                    text: line
                    font.family: Theme.font
                    font.pixelSize: 11
                    lineHeightMode: Text.FixedHeight
                    lineHeight: parent.height
                }
            }
        }

        /*!
            The signal is emitted *before* the item is actually
            drawn meaning we must delay scrolling a bit.
        */
        Timer {
            id: positionTimer
            interval: 1
            running: false
            repeat: false
            onTriggered: view.animatePositionViewAtEnd()
        }

        /*!
            Ensure the last item is always visible
        */
        Connections {
            target: consoleCtrl.model
            onRowsInserted: scrollbar.active ? null : positionTimer.start()
        }
    }

    Selection {
        anchors.fill: parent

        listview: view
        shape: Rectangle {
            color: Theme.alpha(Theme.highlight, 0.3)
            border.width: 1
            border.color: Qt.lighter(Theme.highlight, 1.7)
        }
        
        onSelectionStarted: consoleCtrl.selectionStarted(startIndex, endIndex)
        onSelectionChanged: consoleCtrl.selectionChanged(startIndex, endIndex)
        onSelectionEnded: consoleCtrl.selectionEnded(startIndex, endIndex)
    }

    Scrollbar {
        id: scrollbar

        anchors {
            right: parent.right
            top: parent.top
            bottom: parent.bottom
        }

        width: root.mouseX > root.width - 50 ? 25 : 10
        opacity: root.containsMouse ? 1 : 0

        Behavior on width {
            NumberAnimation {
                duration: 200
                easing.type: Easing.OutCubic
            }
        }

        Behavior on opacity {
            NumberAnimation { duration: 200 }
        }

        flickable: view
        alwaysVisible: true

        foreground: Rectangle {
            anchors.fill: parent
            anchors.margins: 2
            color: "transparent"
            radius: 10
            border.width: 1
            border.color: Theme.highlight

            Text {
                anchors.top: parent.top
                anchors.topMargin: 3
                anchors.horizontalCenter: parent.horizontalCenter
                height: 20
                text: Math.min(99, parseInt(scrollbar.currentRatio * 100, 10))
                color: Theme.highlight
                font.pixelSize: 9
                opacity: parent.width >= 18 ? 1 : 0

                Behavior on opacity {
                    NumberAnimation { duration: 40 }
                }
            }
        }
    }

    Component.onCompleted: view.positionViewAtEnd()
}