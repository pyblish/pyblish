import QtQuick 2.3
import Pyblish 0.1


TextEdit {
    property string style: "body1"

    property color backgroundColor: "transparent"

    property var fontStyles: {
        "display4": {
            "size": 112,
            "font": "light"
        },

        "display3": {
            "size": 56,
            "font": "regular"
        },

        "display2": {
            "size": 45,
            "font": "regular"
        },

        "display1": {
            "size": 34,
            "font": "regular"
        },

        "headline": {
            "size": 24,
            "font": "regular"
        },

        "title": {
            "size": 20,
            "font": "medium"
        },

        "subheading": {
            "size": 16,
            "size_desktop": 15,
            "font": "regular"
        },

        "body2": {
            "size": 14,
            "size_desktop": 13,
            "font": "medium"
        },

        "body1": {
            "size": 14,
            "size_desktop": 13,
            "font": "regular"
        },

        "menu": {
            "size": 14,
            "size_desktop": 13,
            "font": "medium"
        },

        "button": {
            "size": 14,
            "font": "medium"
        },

        "caption": {
            "size": 12,
            "font": "regular"
        }
    }

    property real sizeMult: .75

    property var fontInfo: fontStyles[style]

    font.pixelSize: fontInfo.size * sizeMult
    font.family: "Open Sans"
    font.weight: {
        var weight = fontInfo.font

        if (weight == "medium") {
            return Font.DemiBold
        } else if (weight == "regular") {
            return Font.Normal
        } else if (weight == "light") {
            return Font.Light
        }
    }

    font.capitalization: style == "button" ? Font.AllUppercase : Font.MixedCase

    color: Theme.dark.textColor

    selectByMouse: true
    selectionColor: Theme.alpha(color, 0.5)
    selectedTextColor: Qt.darker(color, 2)
    selectByMouse: true
    selectByKeyboard: true

    Rectangle {
        id: background
        color: backgroundColor
        anchors.fill: parent
    }

    Component.onCompleted: {
        if (typeof fontInfo == "undefined")
            print("WARNING: style \"%1\" was not found".arg(style))
    }
}