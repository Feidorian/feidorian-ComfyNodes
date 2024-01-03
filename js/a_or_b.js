import { app } from "../../scripts/app.js";
import { $el } from "../../scripts/ui.js";

const REF = "Feidorian_AOrB"

app.registerExtension({
    name: REF,

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeType.comfyClass == REF) {
            const orig_nodeOnConnectInput = nodeType.prototype.onConnectInput;
            nodeType.prototype.onConnectInput = function (targetSlot, type, output, originNode, originSlot) {
                if(targetSlot < 2){
                const currSlot = this.inputs[targetSlot]
                const siblingSlot = this.inputs[targetSlot == 0? 1 : 0]
                const outputSlot = this.outputs[0]
                currSlot.type = type
                if(siblingSlot.type != type){
                    this.disconnectInput(targetSlot == 0? 1 : 0)
                }
                siblingSlot.type = type

                if(outputSlot.type != type){
                    this.disconnectOutput(0)
                }
                outputSlot.type = type
            }
            orig_nodeOnConnectInput?.apply(this, arguments)
            }

            const orig_nodeConnectionsChange = nodeType.prototype.onConnectionsChange;

            nodeType.prototype.onConnectionsChange = function (side, slot, connect, link_info, output) {
                orig_nodeConnectionsChange?.apply(this, arguments);
                const inputSlot1 = this.inputs[0]
                const inputSlot2 = this.inputs[1]
                const outputSlot1 = this.outputs[0]

                if(inputSlot1.link == null && inputSlot2.link == null){
                    this.disconnectInput(0)
                    this.disconnectInput(1)
                    this.disconnectOutput(0)
                    inputSlot1.type = inputSlot2.type = outputSlot1.type = "*"
                }
             }
        }
    },
})
