import QtQuick 2.0
import Pyblish.Graphs 0.1


BaseGroupDelegate {
    item: Timeline {
        Component.onCompleted: {
            main_data = modelData.data
        }
    }
}