import QtQuick 2.3


Item {
    height: 300
    width: 300

    Rectangle {
        color: "brown"
        anchors.centerIn: parent
        width: 100
        height: 100

        radius: 10

        // This DOES NOT cause children to be clipped
        // Though I'd expect it to.
        clip: true

        Rectangle {
            color: "purple"
            height: parent.height
            width: 30
        }
    }
}