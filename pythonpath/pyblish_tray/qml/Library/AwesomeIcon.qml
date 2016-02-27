import QtQuick 2.3

import "awesome.js" as Awesome


/*!
    \qmltype AwesomeIcon

    \inqmlmodule Library 0.1

    \brief An Icon from the Font Awesome library.
    http://fortawesome.github.io/Font-Awesome/icons/

    Example:

    \qml
    import QtQuick 2.3
    import Library 0.1

    Item {
        AwesomeIcon {
            name: "close"
            anchors.centerIn: parent
        }
    }
*/
Item {
    id: root

    /*!
        Name of the icon, browse available names here:
        http://fortawesome.github.io/Font-Awesome/icons/
    */
    property string name

    /*!
        Optional color of the icon. If none is provided, the
        color is light grey.
    */
    property alias color: text.color

    /*!
        Optional size of the icon, in pixels. Defaults to 16 px.
    */
    property int size: 16

    width: text.width
    height: text.height

    FontLoader {
        id: fontAwesome
        source: Qt.resolvedUrl("fonts/fontawesome/FontAwesome.otf")
    }

    Text {
        id: text

        anchors.centerIn: parent

        property string name: root.name.match(/.*-rotate/) !== null ? root.name.substring(0, root.name.length - 7) : root.name

        text: Awesome.map.hasOwnProperty(name) ? Awesome.map[name] : ""

        color: "#CCC"

        font.family: fontAwesome.name
        font.weight: Font.Light
        font.pixelSize: root.size
    }
}
