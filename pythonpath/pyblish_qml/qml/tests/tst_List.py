import os
from pyblish_qml import app

tests_path = os.path.dirname(__file__)
qml_path = os.path.dirname(tests_path)
app_path = os.path.join(qml_path, "temp.qml")


if __name__ == "__main__":
    app.main(source=app_path,
             port=6000,
             preload=False,
             debug=True,
             validate=False)
