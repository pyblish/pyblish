import QtQuick 2.3


Image {
    id: icon

    property string name: ""
    property int size

    source: {
        if (name == "")
            return ""

        return Qt.resolvedUrl("icons/%1.png".arg(name))
    }

    width: size || sourceSize.Width
    height: size || sourceSize.Height

    mipmap: true
}