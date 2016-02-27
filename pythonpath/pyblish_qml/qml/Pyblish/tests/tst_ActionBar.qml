import Pyblish 0.1


ActionBar {

    actions: [

        Action {
            iconName: "button-back"
            onTriggered: print("Triggered!")
        },
        Action {
            iconName: "button-close"
            onTriggered: print("Button back triggered!")
        }
    ]
}
