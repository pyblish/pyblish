import QtQuick 2.0

pragma Singleton

Object {
    id: global

    /*!
      Track the currently opened context menu
    */
    property QtObject currentContextMenu
}