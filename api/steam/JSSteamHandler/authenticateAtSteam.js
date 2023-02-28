import { EAuthTokenPlatformType, LoginSession, LoginApprover } from "steam-session";
import fs from "fs";
import SteamUser from "steam-user";
import jwt_decode from "jwt-decode";
import dotenv from "dotenv";
dotenv.config({ path: "../../../.env" });

// This code was shamelessly stolen from DoctorMcKays repository under https://github.com/DoctorMcKay/node-steam-session/blob/master/examples/approve-qr.ts . - search here if you want some more information about it!
async function getLoginSessionWithQRCodeApproval() {
    let approver = new LoginApprover(process.env.STEAM_ACCESSTOKEN, process.env.STEAM_SHAREDSECRET);
    let session = new LoginSession(EAuthTokenPlatformType.SteamClient);

    session.loginTimeout = 120000;

    let startResult = await session.startWithQR();

    session.on("remoteInteraction", () => {
        console.log("A remote interaction was detected.");
    });

    session.on("timeout", () => {
        console.log("This login attempt has timed out.");
    });

    session.on("error", err => {
        console.log(`ERROR: This login attempt has failed! ${err.message}`);
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
}

const getRefreshTokenFromFS = () => {
    const rawData = fs.readFileSync("./RefreshToken.json", "utf8", (err, data) => {
        if (err) {
            console.error(err);
        }
    });

    return JSON.parse(rawData);
};

const setRefreshTokenToFS = data => {
    fs.writeFileSync("./RefreshToken.json", JSON.stringify(data), err => {
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
            getLoginSessionWithQRCodeApproval().then(session => {
                logOnUserAndReturn(session.refreshToken);
                setRefreshTokenToFS({ refreshToken: session.refreshToken });
            });
        } else {
            logOnUserAndReturn(refreshToken);
        }
    });

export { getLoginSessionWithQRCodeApproval, getLoggedInSteamUser };
