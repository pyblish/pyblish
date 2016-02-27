import QtQuick 2.3
import QtQuick.Layouts 1.1

import Pyblish 0.1
import Pyblish.ListItems 0.1 as ListItem


MouseArea {
    id: root

    signal beingHidden
    signal toggled(var data)

    /*!
        Fill parent with an invisible layer separating
        the overall application from the currently active
        context menu.
    */
    anchors.fill: parent

    property var children
    property Item logicalParent

    property int menuX: 0
    property int menuY: 0

    property int restWidth: 150
    property int restHeight: children.length * 25

    function show() { currentMenuOpenAnimation.start() }
    function hide() { currentMenuCloseAnimation.start() }

    onPressed: hide()

    View {
        id: backdrop

        property var window: Utils.findRoot(this)

        x: Math.min(menuX, window.width - restWidth)
        y: Math.min(menuY, window.height - restHeight)

        elevation: 1

        width: restWidth
        height: restHeight

        color: "#333"

        ListView {
            id: menuList
            anchors.fill: parent

            model: root.children
            interactive: false

            delegate: ListItem.ContextMenuItem {
                text: modelData.label
                active: modelData.active
                icon: modelData.icon
                available: modelData.__error__ ? false : true
                type: modelData.__type__
                height: 25
                width: parent.width

                onPressed: {
                    if (type !== "action") {
                        return
                    }
                    else if (active && available) {
                        toggled(modelData)
                        hide()
                    } else if (!available) {
                        app.info(modelData.__error__)
                        app.info("There is a problem with this Action, see terminal.")
                    } else {
                        app.info("Action not active.")
                    }
                }
            }
        }
    }

    PropertyAnimation {
        id: currentMenuOpenAnimation
        properties: "opacity"
        target: backdrop
        from: 0
        to: 1
        duration: 300
        easing.type: Easing.OutBack
    }

    PropertyAnimation {
        id: currentMenuCloseAnimation
        properties: "opacity"
        target: backdrop
        from: 1
        to: 0
        duration: 50
        onStopped: {
            root.visible = false
            root.destroy()
            root.beingHidden()
        }
    }
}