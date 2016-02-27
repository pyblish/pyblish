import QtQuick 2.0
import Pyblish 0.1

import "awesome.js" as Awesome


Item {
    id: widget

    property string name
    property bool rotate: widget.name.match(/.*-rotate/) !== null

    property alias color: text.color
    property int size: 16

    property bool shadow: false

    property var icons: Awesome.map

    property alias weight: text.font.weight

    width: text.width
    height: text.height

    FontLoader { id: fontAwesome; source: Qt.resolvedUrl("fonts/fontawesome/FontAwesome.otf") }

    Text {
        id: text
        anchors.centerIn: parent

        property string name: widget.name.match(/.*-rotate/) !== null ? widget.name.substring(0, widget.name.length - 7) : widget.name

        font.family: fontAwesome.name
        font.weight: Font.Light
        text: widget.icons.hasOwnProperty(name) ? widget.icons[name] : ""
        color: Theme.dark.iconColor
        style: shadow ? Text.Raised : Text.Normal
        styleColor: Qt.rgba(0,0,0,0.5)
        font.pixelSize: widget.size

        Behavior on color {
            ColorAnimation { duration: 200 }
        }

        NumberAnimation on rotation {
            running: widget.rotate
            from: 0
            to: 360
            loops: Animation.Infinite
            duration: 1100
        }
    }
}
