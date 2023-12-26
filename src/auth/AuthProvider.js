import {useContext, createContext, useState, useEffect} from 'react';
import LoadingIcon from '../components/LoadingIcon';


const AuthContext = createContext({
    isAuthenticated: false,
    accessToken: null,
    getRefreshToken: () => {},
    saveSessionInfo: () => {},
    userInfo: null,
});

export function AuthProvider({children}) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [accessToken, setAccessToken] = useState();
    const [userInfo, setUserInfo] = useState();
    const [isLoading, setIsLoading] = useState(false);


    useEffect(() => {
        async function checkAuth() {
            if(accessToken) {
                // already logged in
                const newUserInfo = await requestUserInfo(accessToken);
                if (!newUserInfo) {
                    return
                }
                saveSessionInfo({access_token: accessToken, refresh_token: getRefreshToken()}, newUserInfo);
                return
            }
    
            const token = getRefreshToken();
            if (!token) {
                return
            }
            
            const newAccessToken =  await requestNewAccessToken(token);
            if (!newAccessToken) {
                return
            }
    
            const newUserInfo = await requestUserInfo(newAccessToken);
            if (!newUserInfo) {
                return
            }
            saveSessionInfo({access_token: newAccessToken, refresh_token: token}, newUserInfo);
        }
        setIsLoading(true);
        checkAuth();
        setIsLoading(false);
    }, [accessToken]);

    async function requestNewAccessToken(refreshToken) {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/token/refresh`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Authorization': `Bearer ${refreshToken}`
                }
            });
    
            const responseData = await response.json();
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status} \n details: ${responseData.detail}`);
            }

            return responseData.access_token;

        } catch (error) {
            console.log(error);
        }
        
    }

    async function requestUserInfo(accessToken) {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/users/me`, {
                'method': 'GET',
                'headers': {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                }
            });

            const responseData = await response.json();

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status} \n details: ${responseData.detail}`);
            }

            return responseData

        } catch(error) {
            console.log(error)
        }
    }

    function getRefreshToken() {
        const tokenData = localStorage.getItem("token");
        return tokenData ? JSON.parse(tokenData) : null;
    }

    function saveSessionInfo(loginResponse, newUserInfo) {
        setAccessToken(loginResponse.access_token);
        localStorage.setItem("token", JSON.stringify(loginResponse.refresh_token));
        setUserInfo(newUserInfo);
        setIsAuthenticated(true);
    }

    return (
    <AuthContext.Provider value={{isAuthenticated, accessToken, getRefreshToken, saveSessionInfo, userInfo}}>
        {isLoading ? 
        <div className="w-[100%] h-[100%] items-center flex flex-col align-middle justify-center
         text-zinc-300 text-5xl"><LoadingIcon /></div> : 
        children}
    </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);