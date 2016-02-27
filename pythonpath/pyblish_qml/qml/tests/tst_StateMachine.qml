import QtQuick 2.3
import QtQml.StateMachine 1.0


Rectangle {
    id: window

    width: 400
    height: 500

    color: editing.active ? "brown" :
           processing.active ? "purple" : "limegreen"

    property var items: ["John", "Philip", "Kyle", "Lucas"]

    Behavior on color {
        ColorAnimation {
            duration: 100
        }
    }

    Timer {
        id: processor

        signal stopped

        interval: 500

        running: processing.active

        property int index: 0

        onTriggered: {
            if (index < window.items.length - 1) {
                index += 1
                start()
            } else {
                index = 0
                stopped()
            }
        }
    }

    Column {
        anchors.centerIn: parent

        spacing: 5

        ListView {
            id: list

            width: 300
            height: 300

            focus: true

            spacing: 5
            interactive: false

            currentIndex: processor.index

            model: window.items
            delegate: MouseArea {

                width: parent.width
                height: 50

                hoverEnabled: true

                Rectangle {
                    id: fill

                    anchors.fill: parent
                    color: "white"
                    opacity: containsMouse ? 0.2 : 0.1
                }

                Text {
                    anchors.centerIn: parent
                    color: "white"
                    text: modelData
                }
            }

            highlight: Item {
                Rectangle {
                    color: "steelblue"
                    height: parent.height
                    width: parent.width
                    visible: processor.running
                }
            }
        }

        Row {
            spacing: 2

            MouseArea {
                id: button

                width: parent.width / 2
                height: 30

                Rectangle {
                    anchors.fill: parent
                    color: Qt.darker("steelblue", 1.2)
                }

                Text {
                    color: "white"
                    anchors.centerIn: parent
                    text: editing.active ? "Process" :
                          processing.active ? "Processing.." : "Reset"
                }
            }

            MouseArea {
                id: quitButton

                width: 100
                height: 30

                Rectangle {
                    anchors.fill: parent
                    color: Qt.darker("steelblue", 1.2)
                }

                Text {
                    color: "white"
                    anchors.centerIn: parent
                    text: "Quit"
                }
            }
        }
    }

    StateMachine {
        initialState: runningState

        running: true

        State {
            id: runningState

            initialState: editing

            SignalTransition {
                targetState: quitState
                signal: quitButton.clicked
            }
        
            State {
                id: editing

                SignalTransition {
                    targetState: processing
                    signal: button.clicked
                }
            }

            State {
                id: processing

                SignalTransition {
                    targetState: processing
                    signal: processor.triggered
                }

                SignalTransition {
                    targetState: editing
                    signal: processor.stopped
                }
            }

            State {
                id: summary

                SignalTransition {
                    targetState: editing
                    signal: button.clicked
                }
            }

        }

        FinalState {
            id: quitState
        }

        onFinished: {
            Qt.quit()
        }

    }
}