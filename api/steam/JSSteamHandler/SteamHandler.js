import GlobalOffensive from "globaloffensive";
import { getLoggedInSteamUser } from "./authenticateAtSteam.js";
// https://github.com/DoctorMcKay/node-globaloffensive

export default class CsGoHandler {
    constructor() {
        this._csgo = (async () => {
            const user = await getLoggedInSteamUser();
            const csgo = new GlobalOffensive(user);
            user.gamesPlayed([730]);

            return new Promise(resolve => {
                csgo.on("connectedToGC", () => {
                    resolve(csgo);
                });
            });
        })();
    }

    //TODO: Write a reload user function to reload inventory.
    //TODO: Also add a timestamp everytime we use inventory to make sure its not older than a specific treshold...

    /**
     * Cost intensive. Use with caution!
     * @returns all owned items, including the ones that are in caskets
     */
    async getAllOwnedItemsInCaskets() {
        const caskets = (await this._csgo).inventory.filter(item => item.casket_id == undefined && item.id.length <= 12);

        const allItems = (
            await Promise.all(
                caskets.map(
                    async casket =>
                        new Promise(async resolve => {
                            (await this._csgo).getCasketContents(casket.id, (err, items) => {
                                resolve(items);
                            });
                        })
                )
            )
        ).flat();

        return allItems;
    }

//    async checkIfItemTradeable(assetId) {
//        (await this._csgo).on("inspectItemTimedOut", itemId => {
//            throw new Error("Request inspecting item with Id " + itemId + " timed out");
//        });
//
//        return await (await this._csgo).inspectItem("300033068", assetId);
//    }

    async getAllOwnedItemsInInventory() {
        const items = (await this._csgo).inventory.filter(item => item.casket_id == undefined && item.id.length <= 12);

        return items;
    }

    async moveFromCasket(itemAssetId, casketAssetId) {
        (await this._csgo).removeFromCasket(casketAssetId, itemAssetId);
    }

    async moveToCasket(itemAssetId, casketAssetId) {
        (await this._csgo).addToCasket(casketAssetId, itemAssetId);
    }

    async getCasketContent(assetId) {
            return new Promise(async resolve => {
                        (await this._csgo).getCasketContents(assetId, (err, items) => {
                            resolve(items);
                        });
                    })
    }
}
