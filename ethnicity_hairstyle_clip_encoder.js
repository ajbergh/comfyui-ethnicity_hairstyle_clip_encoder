import { app } from "../../scripts/app.js";

app.registerExtension({
	name: "ethnicity_hairstyle_clip_encoder",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "CLIPTextEncodeWithExtras") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated?.apply(this, arguments);

                // Ethnicity
                let ethnicityWidget = this.widgets.find((w) => w.name === "ethnicity");
                // DON'T set the value here. Let the Python "default" handle it.
                // ethnicityWidget.value = ...;  <-- REMOVE THIS LINE
                ethnicityWidget.callback = () => {
                    app.ui.settings.setSettingValue('EthnicitySelection', ethnicityWidget.value);
                }

                // Hairstyle
                let hairstyleWidget = this.widgets.find((w) => w.name === "hairstyle");
                // DON'T set the value here. Let the Python "default" handle it.
                // hairstyleWidget.value = ...;  <-- REMOVE THIS LINE
                hairstyleWidget.callback = () => {
                    app.ui.settings.setSettingValue('HairstyleSelection', hairstyleWidget.value);
                }
                return r;
            }
        }
    }
});