/*
 * Example of composite items with bindings
 *
 * In this example, an external item is used and populated
 * within a ListView. The composed component is then bound to
 * by referencing it's internal loader.
 *
*/

import QtQuick 2.3


ListView {
    id: root

    width: 300
    height: 200

    model: ["orange", "steelblue", "pink", "turquoise"]

    spacing: 5

    delegate: CompositeItemBinding {
        id: composite

        width: root.width

        height: expanded ? bodyItem.height : 30

        body: Rectangle {
            height: modelData == "orange" ? 40 :
                    modelData == "pink" ? 100 : 200

            color: modelData
        }
    }
}