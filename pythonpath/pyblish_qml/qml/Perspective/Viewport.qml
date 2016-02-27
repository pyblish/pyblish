import QtQuick 2.3
import Pyblish 0.1
import "../Delegates.js" as Delegates


Item {
    property QtObject item
    property alias scrollbar: scrollbar

    Flickable {
        id: body

        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.right: scrollbar.left

        anchors.leftMargin: 7
        anchors.rightMargin: 7

        clip: true

        contentHeight: _body.height
        boundsBehavior: Flickable.StopAtBounds
        flickableDirection: Flickable.VerticalFlick

        Column {
            id: _body

            Repeater {
                model: [
                    {
                        type: "spacer",
                        load: true,
                    },
                    {
                        type: "path",
                        name: "Path",
                        closed: true,
                        item: root.item,
                        load: item.itemType == "plugin"
                    },
                    {
                        type: "documentation",
                        name: "Documentation",
                        closed: true,
                        item: root.item,
                        load: item.itemType == "plugin"
                    },
                    {
                        type: "results",
                        name: "Errors",
                        closed: false,
                        model: app.errorProxy,
                        load: true
                    },
                    {
                        type: "results",
                        name: "Records",
                        closed: false,
                        model: app.recordProxy,
                        load: true,
                    },
                    // {
                    //     type: "timeline",
                    //     name: "Timeline",
                    //     closed: false,
                    //     load: true,
                    //     data: function () {
                            /*!
                                Serialise model to data compatible with Timeline
                                NOTE(marcus): Have Timeline adapt to the interface
                                    of the model, instead of doing it this way. It
                                    might yield better performance and withstand
                                    greater changes during refactoring work.
                            */
                    //         var data = [];

                    //         for (var i = 0; i < app.itemProxy.rowCount(); i++) {
                    //             data.push({
                    //                 "name": app.itemProxy.item(i).name,
                    //                 "duration": app.itemProxy.item(i).duration,
                    //             })
                    //         }

                    //         return data;
                    //     }()
                    // },
                    // {
                    //     type: "items",
                    //     name: "Plug-ins",
                    //     closed: false,
                    //     model: app.itemProxy,
                    //     load: item.itemType == "instance",
                    // },
                    // {
                    //     type: "items",
                    //     name: "Instances",
                    //     closed: false,
                    //     model: app.itemProxy,
                    //     load: item.itemType == "plugin",
                    // },
                    {
                        type: "spacer",
                        load: true,
                    },
                ]

                Loader {
                    width: body.width
                    sourceComponent: modelData.load ? Delegates.components[modelData.type] : null
                }
            }
        }
    }

    Scrollbar {
        id: scrollbar

        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.margins: 2
        anchors.rightMargin: 1

        width: visible ? 15 : 0

        flickable: body
    }
}
