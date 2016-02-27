import QtQuick 2.3
import Pyblish 0.1


// CheckBoxes have a status that flashes upon being updated
Rectangle {
    color: "brown"

    width: 500
    height: 300

    Grid {
        anchors.fill: parent
        anchors.margins: 10
        columns: 2
        columnSpacing: 10

        Label { text: "Unchecked" }
        CheckBox {}

        Label { text: "Checked" }
        CheckBox { checked: true }

        Label { text: "Active" }
        CheckBox { active: true }

        Label { text: "Inactive" }
        CheckBox { active: false }

        Label { text: "Default State"}
        CheckBox { status: "default"; checked: true }

        Label { text: "Selected State" }
        CheckBox { status: "selected"; checked: true }

        Label { text: "Success State" }
        CheckBox { status: "success"; checked: true }

        Label { text: "Warning State" }
        CheckBox { status: "warning"; checked: true }

        Label { text: "Error State" }
        CheckBox { status: "error"; checked: true }

    }
}
