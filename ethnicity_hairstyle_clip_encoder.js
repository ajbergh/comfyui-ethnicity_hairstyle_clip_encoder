/**
 * ================================================================================
 * ComfyUI Extension: Ethnicity & Hairstyle CLIP Encoder
 * --------------------------------------------------------------------------------
 * This JavaScript module registers an extension for ComfyUI that customizes the
 * behavior of the CLIPTextEncodeWithExtras node in order to integrate ethnicity and
 * hairstyle options into the node's UI.
 *
 * Key Features:
 *   - Hooks into the node registration process to modify widget behavior.
 *   - For the "ethnicity" widget:
 *       • Avoids setting a default value so that the Python backend "default" is used.
 *       • Sets a callback to update the application settings when the selection changes.
 *   - For the "hairstyle" widget:
 *       • Similarly avoids forcing a default value.
 *       • Updates the application settings when the selection changes.
 *
 * Usage:
 *   This extension is auto-registered when the application starts. It modifies node
 *   behavior by intercepting the node creation process via the 'beforeRegisterNodeDef'
 *   hook of the app's extension system.
 *
 * ================================================================================
 */

import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "ethnicity_hairstyle_clip_encoder", // Unique name of the extension

    /**
     * This hook is called before the node definition is registered.
     * It allows customization of the node's behavior, widgets, etc.
     *
     * @param {Function} nodeType - The constructor of the node.
     * @param {Object} nodeData - The node's configuration data.
     * @param {Object} app - The main application object.
     */
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Check if the node being registered is the target node.
        if (nodeData.name === "CLIPTextEncodeWithExtras") {
            // Preserve original onNodeCreated (if defined) to maintain default setup.
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            // Override onNodeCreated to insert custom widget callbacks.
            nodeType.prototype.onNodeCreated = function () {
                // Execute the original onNodeCreated functionality.
                const r = onNodeCreated?.apply(this, arguments);

                // ----------------------------------------
                // Ethnicity widget customization
                // ----------------------------------------
                // Find the widget associated with ethnicity selection.
                let ethnicityWidget = this.widgets.find((w) => w.name === "ethnicity");
                // Do not set the widget value here; let the Python backend handle the default.
                // ethnicityWidget.value = ...;  <-- This line is intentionally removed.
                // Define a callback that updates the app settings when the ethnicity is changed.
                ethnicityWidget.callback = () => {
                    app.ui.settings.setSettingValue('EthnicitySelection', ethnicityWidget.value);
                };

                // ----------------------------------------
                // Hairstyle widget customization
                // ----------------------------------------
                // Find the widget associated with hairstyle selection.
                let hairstyleWidget = this.widgets.find((w) => w.name === "hairstyle");
                // Again, do not override the widget's default value.
                // hairstyleWidget.value = ...;  <-- This line is intentionally removed.
                // Set a callback to update the app settings when the hairstyle selection is changed.
                hairstyleWidget.callback = () => {
                    app.ui.settings.setSettingValue('HairstyleSelection', hairstyleWidget.value);
                };

                // ----------------------------------------
                // Expression widget customization
                // ----------------------------------------
                // Find the widget associated with expression selection.
                let expressionWidget = this.widgets.find((w) => w.name === "expression");
                // Again, do not override the widget's default value.
                // expressionWidget.value = ...;  <-- This line is intentionally removed.
                // Set a callback to update the app settings when the expression selection is changed.
                expressionWidgetWidget.callback = () => {
                    app.ui.settings.setSettingValue('ExpressionSelection', expressionWidgetWidget.value);
                };
                // Return the result of the original onNodeCreated handler.
                return r;
            };
        }
    }
});