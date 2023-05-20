import { EAuthTokenPlatformType, LoginSession, LoginApprover } from "steam-session";
import fs from "fs";
import SteamUser from "steam-user";
import jwt_decode from "jwt-decode";
import dotenv from "dotenv";
dotenv.config({ path: "../../../.env" });

// This code was shamelessly stolen from DoctorMcKays repository under https://github.com/DoctorMcKay/node-steam-session/blob/master/examples/approve-qr.ts . - search here if you want some more information about it!
async function getLoginSessionWithQRCodeApproval() {
    try {
        let approver = new LoginApprover(process.env.STEAM_ACCESSTOKEN, process.env.STEAM_SHAREDSECRET);
        let session = new LoginSession(EAuthTokenPlatformType.SteamClient);

        session.loginTimeout = 120000;

        let startResult = await session.startWithQR();

        session.on("remoteInteraction", () => {
            console.error("A remote interaction was detected.");
        });

        session.on("timeout", () => {
            console.error("This login attempt has timed out.");
        });

        session.on("error", err => {
            console.error(`ERROR: This login attempt has failed! ${err.message}`);
        });

        await approver.approveAuthSession({
            qrChallengeUrl: startResult.qrChallengeUrl,
            approve: true,
        });

        // Now that we've approved the login attempt, we can immediately poll to get our access tokens
        session.forcePoll();

        return new Promise(resolve => {
            session.on("authenticated", () => {
                resolve(session);
            });
        });
    } catch (e) {
        console.error("Creating login session failed with error: ", e.message) 
        throw e
    }
}

const getRefreshTokenFromFS = () => {
    const path = process.cwd() + "/api/steam/JSSteamHandler/RefreshToken.json";

    if (fs.existsSync(path)) {
        const rawData = fs.readFileSync(path, "utf8", (err, data) => {
            if (err) {
                console.error(err);
                return { refreshToken: undefined };
            }
        });
        return rawData ? JSON.parse(rawData) : rawData;
    } else {
        fs.writeFileSync(process.cwd() + "/api/steam/JSSteamHandler/RefreshToken.json", "");
        return { refreshToken: undefined };
    }
};

const setRefreshTokenToFS = data => {
    fs.writeFileSync(process.cwd() + "/api/steam/JSSteamHandler/RefreshToken.json", JSON.stringify(data), err => {
        if (err) {
            console.error(err);
        }
    });
};

const checkIfValidToken = token => !!token && new Date(jwt_decode(token).exp * 1000) > Date.now();

const getLoggedInSteamUser = () =>
    new Promise((resolve, reject) => {
        let user = new SteamUser();
        let { refreshToken } = getRefreshTokenFromFS();

        const logOnUserAndReturn = refreshToken => {
            user.logOn({ refreshToken });

            const interval = setInterval(function () {
                if (user.publicIP != undefined) {
                    clearInterval(interval);
                    resolve(user);
                }
            }, 200);

            setTimeout(() => {
                reject("Attempt to login User timed out.");
            }, 30000);
        };


        if (!checkIfValidToken(refreshToken)) {
            console.error("Detected invalid Refresh Token. Trying to regenerate one.");
            getLoginSessionWithQRCodeApproval().then(session => {
                setRefreshTokenToFS({ refreshToken: session.refreshToken });
                logOnUserAndReturn(session.refreshToken);
            });
        } else {
            logOnUserAndReturn(refreshToken);
        }
    });

export { getLoginSessionWithQRCodeApproval, getLoggedInSteamUser };
