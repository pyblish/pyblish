import QtQuick 2.0
import QtQuick.Controls 1.0
import QtGraphicalEffects 1.0

Rectangle {
    width: 480
    height: 640

    ListView {
        id: flickable
        anchors.fill: parent

        model: 100
        delegate: Text {
            font.pixelSize: 50
            text: "Hello " + index
        }
    }

    Rectangle {
        anchors.fill: fastBlur
        color: "white"
    }

    FastBlur {
        id: fastBlur

        height: 124

        width: parent.width
        radius: 60
        opacity: 1

        source: ShaderEffectSource {
            sourceItem: flickable
            sourceRect: Qt.rect(0, 0, fastBlur.width, fastBlur.height)
        }
    }
}