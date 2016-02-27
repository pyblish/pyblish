import QtQuick 2.0

pragma Singleton

Object {
    property color background: "#111"
    property color foreground: "#333"
    property color highlight: "#ccc"
    property color textColor: "#ddd"
    property string font: "Lato"
    property string boldFont: "Lato Black"

    function alpha(color, alpha) {
        // Make sure we have a real color object to work with
        // (versus a string like "#ccc")
        var realColor = Qt.darker(color, 1)

        realColor.a = alpha

        return realColor
    }

    FontLoader { source: Qt.resolvedUrl("fonts/lato/Lato-Regular.ttf") }  // Lato
    FontLoader { source: Qt.resolvedUrl("fonts/lato/Lato-Black.ttf") }  // Lato Black
    FontLoader { source: Qt.resolvedUrl("fonts/ocraextended.ttf") }  // OCR A Extended
}