/*! QML entry-point
 *
 * This file is loaded from Python and in turn loads
 * the actual application. The application is then loaded
 * in an asynchronous fashion so as to display the window
 * as quickly as possible.
 *
 * "app.qml" is a separate file because we can delay
 * importing the custom QML modules.
 *
 * See app.qml for next step.
 *
*/

import QtQuick 2.3

Rectangle {
    color: Qt.rgba(0.3, 0.3, 0.3)

    Loader {
        id: loader
        anchors.fill: parent
        asynchronous: true
        source: "app.qml"
    }
}
