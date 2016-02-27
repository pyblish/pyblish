import QtQuick 2.3


QtObject {
    id: action

    property string name

    property string iconName
    property real iconSize: 14
    
    property string tooltip

    property bool visible: true

    property bool enabled: true

    signal triggered(var caller)
}