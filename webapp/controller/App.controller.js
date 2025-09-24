sap.ui.define([
    "sap/ui/core/mvc/Controller",
    "sap/m/MessageBox",
    "sap/m/MessageToast"
], function (Controller, MessageBox, MessageToast) {
    "use strict";

    return Controller.extend("photo.organizer.controller.App", {
        onOrganizePress: function () {
            var oFileUploader = this.byId("fileUploader");
            var aFiles = oFileUploader.getFiles();

            if (aFiles.length === 0) {
                MessageToast.show("Please select photos to upload.");
                return;
            }

            var oStrategy = this.byId("strategy").getSelectedItem().getKey();
            var bSyncGoogle = this.byId("sync_google_drive").getSelected();
            var bSyncOneDrive = this.byId("sync_one_drive").getSelected();

            var oFormData = new FormData();
            oFormData.append("strategy", oStrategy);
            oFormData.append("sync_google_drive", bSyncGoogle);
            oFormData.append("sync_one_drive", bSyncOneDrive);

            for (var i = 0; i < aFiles.length; i++) {
                oFormData.append("files[]", aFiles[i]);
            }

            var oXhr = new XMLHttpRequest();
            oXhr.open("POST", "/organize", true);

            oXhr.onload = function () {
                if (oXhr.status === 200) {
                    var oResponse = JSON.parse(oXhr.responseText);
                    var sLogs = oResponse.logs.join("\\n");
                    MessageBox.information("Organization Logs", {
                        details: sLogs
                    });
                } else {
                    MessageBox.error("An error occurred during organization.");
                }
            };

            oXhr.send(oFormData);
        }
    });
});
