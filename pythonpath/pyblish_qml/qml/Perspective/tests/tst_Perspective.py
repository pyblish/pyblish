from pyblish_qml import app


if __name__ == "__main__":
    app.main(source="tst_Perspective.qml",
             port=6000,
             preload=False,
             debug=True,
             validate=False)
