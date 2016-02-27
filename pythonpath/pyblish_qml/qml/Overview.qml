import QtQuick 2.3
import Pyblish 0.1
import Pyblish.ListItems 0.1


Item {
    id: overview

    MouseArea {
        id: pluginMouse
        anchors.fill: parent
        hoverEnabled: true
    }

    property string __lastPlugin

    signal instanceEntered(int index)
    signal pluginEntered(int index)

    states: [
        State {
            name: "publishing"
        },

        State {
            name: "finished"
        },

        State {
            name: "initialising"
        },

        State {
            name: "stopping"
        }
    ]

    function setMessage(message) {
        footer.message.text = message
        footer.message.animation.restart()
        footer.message.animation.start()
    }

    TabBar {
        id: tabBar

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right

        tabs: [
            {
                text: "",
                icon: "logo-white"
            },
            "Terminal"
        ]
    }

    View {
        id: tabView

        anchors.top: tabBar.bottom
        anchors.bottom: footer.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: tabView.margins
        anchors.bottomMargin: 0

        width: parent.width - 10

        elevation: -1

        Row {
            visible: tabBar.currentIndex == 0

            anchors.fill: parent
            anchors.margins: parent.margins

            List {
                model: app.instanceProxy

                width: Math.floor(parent.width / 2.0)  // To keep checkbox border from collapsing
                height: parent.height

                section.property: "object.family"
                section.delegate: SectionItem {
                    text: section

                    onClicked: {
                        checkState = !checkState
                        app.toggleSection(checkState, text)
                    }
                }

                onActionTriggered: {
                    if (action.name == "repair")
                        app.repairInstance(index)
                    else if (action.name == "enter")
                        overview.instanceEntered(index)
                }

                onItemToggled: app.toggleInstance(index)
            }

            List {
                id: pluginList

                model: app.pluginProxy

                width: Math.floor(parent.width / 2.0)
                height: parent.height

                section.property: "object.verb"
                section.delegate: SectionItem {
                    text: section

                    onClicked: {
                        checkState = !checkState
                        app.toggleSection(checkState, text)
                    }
                }

                onActionTriggered: {
                    if (action.name == "repair")
                        app.repairPlugin(index)
                    else if (action.name == "enter")
                        overview.pluginEntered(index)
                }

                onItemToggled: app.togglePlugin(index)
                onItemRightClicked: {
                    var actions = app.getPluginActions(index)

                    if (actions.length === 0)
                        return

                    function show() {
                        return Utils.showContextMenu(
                            overview,           // Parent
                            actions,            // Children
                            pluginMouse.mouseX, // X Position
                            pluginMouse.mouseY) // Y Position
                    }

                    if (Global.currentContextMenu !== null) {
                            function callback() {
                                Global.currentContextMenu.beingHidden.disconnect(callback)
                                Global.currentContextMenu = show()
                          }

                          Global.currentContextMenu.beingHidden.connect(callback)
                          Global.currentContextMenu.hide()

                    } else {
                        Global.currentContextMenu = show()
                    }
                }

                Connections {
                    target: Global.currentContextMenu
                    onToggled: app.runPluginAction(JSON.stringify(data))
                }
            }
        }

        Terminal {
            id: terminal

            anchors.fill: parent
            anchors.margins: 2

            visible: tabBar.currentIndex == 1
        }
    }


    Footer {
        id: footer

        visible: overview.state != "initialising"

        mode: overview.state == "publishing" ? 1 : overview.state == "finished" ? 2 : 0

        width: parent.width
        anchors.bottom: parent.bottom

        onPublish: app.publish()
        onValidate: app.validate()
        onReset: app.reset()
        onStop: app.stop()
        onSave: app.save()
    }

    Connections {
        target: app

        onError: setMessage(message)
        onInfo: setMessage(message)

        onStateChanged: {
            if (state == "ready") {
                overview.state = ""
                setMessage("Ready")
            }

            if (state == "initialising") {
                overview.state = "initialising"
                setMessage("Initialising..")
            }

            if (state == "publishing") {
                overview.state = "publishing"
                setMessage("Publishing..")
            }

            if (state == "finished") {
                overview.state = "finished"
                setMessage("Finished..")
            }

            if (state == "stopping") {
                setMessage("Stopping..")
            }

            if (state == "stopped") {
                overview.state = "finished"
                setMessage("Stopped")
            }

            if (state == "dirty") {
                setMessage("Dirty..")
            }

            if (state == "acting") {
                setMessage("Acting")
                overview.state = "publishing"
            }
        }
    }
}
