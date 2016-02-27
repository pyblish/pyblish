import QtQuick 2.0
import Pyblish 0.1


Item {
    id: view

    z: 2

    clip: true

    /*!
       Optional tooltip to be displayed when
       hovering this component
     */
    property string tooltip
    property Item __tooltip
    property bool doubleClickEnabled: false

    signal clicked(var mouse)
    signal doubleClicked(var mouse)

    property int startSize: circular ? width/5 : width/3
    property int middleSize: circular ? width * 3/4 : width - 10
    property int endSize: circular ? centered ? width: width * 3
                                   : width * 1.5

    property Item currentCircle
    property color color: Theme.alpha("white", 0.1)

    property bool circular: false
    property bool centered: false

    /*!

      Distinguish between clicks and double clicks

    */
    Timer {
        id: doubleClickTimer

        interval: view.doubleClickEnabled ? 200 : 0

        repeat: false

        property var mouse

        onTriggered: view.clicked(mouse)
    }

    MouseArea {
        id: mouseArea

        anchors.fill: parent

        hoverEnabled: enabled

        onPressed: createTapCircle(mouse.x, mouse.y)
        onCanceled: currentCircle.removeCircle();

        onReleased: {
            currentCircle.removeCircle();

            if (doubleClickTimer.running) {
                view.doubleClicked(mouse)
                doubleClickTimer.stop()
                return
            }

            doubleClickTimer.mouse = mouse
            doubleClickTimer.start()
        }

        onEntered: {
            if (view.tooltip) {
                var root = Utils.findRoot(view)

                var local_pos = view.mapToItem(root, 0, 0)

                var tooltip = Tooltip.create(view.tooltip, root, {})
                tooltip.z = 10
                tooltip.x = local_pos.x - (tooltip.width - 13) + (view.width / 2)
                tooltip.y = local_pos.y - tooltip.height - 7

                view.__tooltip = tooltip
                view.__tooltip.show()
            }
        }
        onExited: {
            if (view.__tooltip) {
                view.__tooltip.hide()
            }
        }
    }

    function createTapCircle(x, y) {
        if (!currentCircle)
            currentCircle = tapCircle.createObject(
                view, {
                       "circleX": centered ? width/2 : x,
                       "circleY": centered ? height/2 : y
                   });
    }

    Rectangle {
        id: hover

        z: 2

        anchors.fill: parent
        
        color: Theme.alpha("white", 0.05)
        
        visible: mouseArea.containsMouse
    }

    Component {
        id: tapCircle

        Item {
            id: circleItem

            anchors.fill: parent

            function removeCircle() {
                if (fillAnimation.running) {
                    fillAnimation.stop()

                    slowCloseAnimation.start()

                    circleItem.destroy(400);
                    currentCircle = null;
                } else {
                    circleItem.destroy(400);
                    closeAnimation.start();
                    currentCircle = null;
                }
            }

            property real circleX
            property real circleY

            property bool closed

            Item {
                id: circleParent
                anchors.fill: parent
                visible: !circular

                Rectangle {
                    id: circleRectangle

                    x: circleItem.circleX - width/2
                    y: circleItem.circleY - height/2

                    property double size

                    width: size
                    height: size
                    radius: size/2

                    opacity: 0
                    color: view.color

                    SequentialAnimation {
                        id: fillAnimation
                        running: true

                        ParallelAnimation {

                            NumberAnimation {
                                target: circleRectangle; property: "size"; duration: 400;
                                from: startSize; to: middleSize; easing.type: Easing.InOutQuad
                            }

                            NumberAnimation {
                                target: circleRectangle; property: "opacity"; duration: 200;
                                from: 0; to: 1; easing.type: Easing.InOutQuad
                            }
                        }
                    }

                    ParallelAnimation {
                        id: closeAnimation

                        NumberAnimation {
                            target: circleRectangle; property: "size"; duration: 400;
                            to: endSize; easing.type: Easing.InOutQuad
                        }

                        NumberAnimation {
                            target: circleRectangle; property: "opacity"; duration: 400;
                            from: 1; to: 0; easing.type: Easing.InOutQuad
                        }
                    }

                    ParallelAnimation {
                        id: slowCloseAnimation

                        SequentialAnimation {

                            NumberAnimation {
                                target: circleRectangle; property: "opacity"; duration: 150;
                                from: 0; to: 1; easing.type: Easing.InOutQuad
                            }

                            NumberAnimation {
                                target: circleRectangle; property: "opacity"; duration: 250;
                                from: 1; to: 0; easing.type: Easing.InOutQuad
                            }
                        }

                        NumberAnimation {
                            target: circleRectangle; property: "size"; duration: 400;
                            to: endSize; easing.type: Easing.InOutQuad
                        }
                    }
                }
            }
        }
    }
}
