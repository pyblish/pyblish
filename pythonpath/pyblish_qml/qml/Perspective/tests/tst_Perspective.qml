import QtQuick 2.3
import Pyblish 0.1
import ".." as Perspective


Loader {
    id: loader

    Connections {
        target: app

        onInitialised: {
            var item = app.itemModel.item(1)
            setup(item)
            setSource("../Page.qml", {"item": item})
        }
    }

    function setup(item) {
        app.recordProxy.clear_inclusion()
        app.recordProxy.add_inclusion("type", "record")
        app.recordProxy.add_inclusion("type", item.type)
        app.recordProxy.add_inclusion(item.itemType, item.name)

        app.errorProxy.clear_inclusion()
        app.errorProxy.add_inclusion("type", "error")
        app.errorProxy.add_inclusion("type", item.type)
        app.errorProxy.add_inclusion(item.itemType, item.name)
    }
}
