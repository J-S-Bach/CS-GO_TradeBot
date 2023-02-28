import GlobalOffensive from "globaloffensive";
import { getLoggedInSteamUser } from "./authenticateAtSteam.js";
// https://github.com/DoctorMcKay/node-globaloffensive

class CsGoHandler {
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

    // //TODO
    // async checkIfItemTradeable(assetId) {
    //     return await (await this._csgo).inspectItem("300033068", assetId);
    // }

    // async getAllOwnedItemsInInventory() {
    //     const items = (await this._csgo).inventory.filter(item => item.casket_id == undefined && item.id.length <= 12);

    //     return (await this._csgo).inspectItem();
    // }

    async moveFromCasket(itemAssetId, casketAssetId) {
        return await this.removeFromCasket(casketAssetId, itemAssetId);
    }

    async moveToCasket(itemAssetId, casketAssetId) {
        return await this.addToCasket(casketAssetId, itemAssetId);
    }
}